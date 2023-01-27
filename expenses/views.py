from PIL import Image
from .models import Expense, OrderLineItem
from django.forms import modelformset_factory, Form
from profiles.models import UserProfile

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from custom_storages import MediaStorage
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from base64 import b64encode, b64decode
from io import BytesIO, TextIOWrapper
from home.forms import Image_form
from expenses.forms import Expense_form, Order_form

import stripe
import proto
import os
import uuid

# set google document AI variables
project_id = os.environ["DOCUMENT_AI_PROJECT_ID"]
location = os.environ["DOCUMENT_AI_LOCATION"]  # Format is 'us' or 'eu'
# Create processor before running sample, Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
processor_id = os.environ["DOCUMENT_AI_PROCESSOR_ID"]


@login_required
def add_image(request, expense_id=""):
    """ upload image to Google vision API """

    if request.method == "POST" and request.FILES != {}:
        form = Image_form({}, request.FILES)
        if form.is_valid():

            image = request.FILES['image']
            expense_id = uuid.uuid4().hex.upper()
            content = image.read()

            # process image and process results for template
            # need to set mime type on image upload Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
            mime_type = image.content_type.split('.')[-1]
            mime = mime_type + ";" if mime_type else ";"

            file_directory_within_bucket = f"user_upload_files/{expense_id}"

            # synthesize a full file path; note that we included the filename
            file_path_within_bucket = os.path.join(
                file_directory_within_bucket,
                image.name
            )

            media_storage = MediaStorage()
            media_storage.save(file_path_within_bucket, image)
            image_url = media_storage.url(
                file_path_within_bucket)

            expense = Expense(
                image_url=image_url,
                expense_id=expense_id,
                user_profile=request.profile,
                paid_amount=0
            )
            expense.save()

            result_dict = upload_to_Document_AI(mime_type, content)
            line_items = update_line_items(result_dict)
            normalized_items = update_normalized_items(result_dict)
            net_amount = line_items['net_amount']

            context = {
                'net_amount': net_amount,
                'expense': expense,
                'normalized_items': normalized_items,
                'line_items': line_items,
            }

            return render(request, 'expenses/add_expense.html', context)
        else:
            messages.error(request, form.errors.as_text())
    return render(request, 'expenses/upload_image.html')


@login_required
def add_expense(request):

    if request.method == 'POST':
        form = Expense_form(request.POST, {})
        if form.is_valid():

            line_items = [v for k, v in request.POST.items()
                          if k.startswith('line_item ')]
            expense = Expense(
                supplier_name=request.POST.get('supplier_name', ''),
                supplier_address=request.POST.get('supplier_address', ''),
                supplier_phone=request.POST.get('supplier_phone', ''),
                total_amount=float(request.POST.get('total_amount', 0)),
                total_tax_amount=float(
                    request.POST.get('total_tax_amount', 0)),
                tip_amount=float(request.POST.get('tip_amount', 0)),
                net_amount=float(request.POST.get('net_amount', 0)),
                line_item_count=line_items.__len__(),
            )

            tip_split = request.POST.get('tip_split', False)
            expense.save()

            line_items = [v for k, v in request.POST.items()
                          if k.startswith('line_item ')]
            if line_items:
                for line_item in line_items:
                    items = line_item.split(" % ")
                    user_profile = get_object_or_404(
                        UserProfile, pk=int(items[3]))

                    order_line_item = OrderLineItem(
                        order=expense,
                        user_profile=user_profile,
                        description=items[0],
                        quantity=float(items[1]),
                        amount=float(items[2]),
                        lineitem_total=float(items[1]) * float(items[2]),
                        tax_amount=0,
                        is_paid=False,
                    )

                    order_line_item.tax_amount = (float(expense.total_tax_amount) / float(expense.total_amount)) * float(
                        order_line_item.lineitem_total)

                    order_line_item.lineitem_total = float(
                        order_line_item.lineitem_total) + float(order_line_item.tax_amount)

                    if user_profile == request.profile:
                        order_line_item.is_paid = True
                        expense.paid_amount += order_line_item.lineitem_total
                        expense.save()

                    order_line_item.save()

            messages.info(request, 'Successfully Saved Expense!')
            return redirect(reverse("user_home"))
        else:
            messages.error(request, form.errors.as_text())

    return redirect(request, 'expenses/upload_image.html')


@ login_required
def delete_expense(request, expense_id):
    """ Delete a product from the store """

    expense = Expense.objects.filter(pk=expense_id).first()
    media_storage = MediaStorage()
    media_storage.delete(expense.image_url)
    expense.delete()

    messages.success(request, 'Expense deleted!')
    return redirect(reverse('user_home'))


def update_line_items(json_dump):
    line_items = {}
    line_item = {}

    # Grab each key/value pair by entity and group the values up.
    for entity in json_dump:
        if len(entity['properties']) > 2:
            line_item = {}
            for property in entity['properties']:
                if property['type_'] == "line_item/description":
                    line_item['description'
                              ] = property['mention_text']
                elif property['type_'] == "line_item/quantity":
                    line_item['quantity'
                              ] = property['mention_text']
                elif property['type_'] == "line_item/amount":
                    line_item['amount'
                              ] = property['mention_text']
                else:
                    line_item[entity["type_"]] = property["mention_text"]
            line_items.update({entity['id']: line_item})

    net_amount = 0
    for line_item in line_items.values():
        quantity = int(line_item['quantity'])
        amount = float(line_item['amount'])
        net_amount += quantity * amount

    line_items.update({'net_amount': net_amount})
    return line_items


def update_normalized_items(json_dump):
    normalized_items = {}
    normalized_item = {}

    for entity in json_dump:
        if len(entity['properties']) == 0:
            if entity.get('normalized_value') is not None:
                normalized_items[entity["type_"]
                                 ] = entity['normalized_value']['text']
            if len(entity['properties']) == 1:
                if entity.get('properties') is not None:
                    normalized_items[entity["type_"]
                                     ] = entity['mention_text']
    return normalized_items


def upload_to_Document_AI(mime, image_content):
    """ Upload document to Google DocumnetAI servece through client library and return document """

    opts = ClientOptions(
        api_endpoint=f"{location}-documentai.googleapis.com")
    # lang = request.POST["language"]
    client = documentai.DocumentProcessorServiceClient(
        client_options=opts)
    name = client.processor_path(project_id, location, processor_id)

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(
        content=image_content, mime_type=mime)

    # Configure the process request
    process_request = documentai.ProcessRequest(
        name=name, raw_document=raw_document)

    result = client.process_document(request=process_request)

    # For a full list of Document object attributes, please reference this page:
    # https://cloud.google.com/python/docs/reference/documentai/latest/google.cloud.documentai_v1.types.Document
    document = result.document

    result_dict = [proto.Message.to_dict(
        entity) for entity in document.entities]

    return result_dict
