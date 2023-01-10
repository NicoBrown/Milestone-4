from PIL import Image
from .models import Expense, OrderLineItem
from django.forms import modelformset_factory, Form
from profiles.models import UserProfile
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from custom_storages import MediaStorage
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from base64 import b64encode, b64decode
from io import BytesIO, TextIOWrapper

import proto
import os
import uuid


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"kwik-split-0a449986ee26.json"

# TODO(developer): Uncomment these variables before running the sample.
project_id = 'kwik-split'
location = 'eu'  # Format is 'us' or 'eu'
processor_id = '8a4fbaeb2765405e'  # Create processor before running sample
# Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information


def expense_detail(request, expense_id):
    """ A view to show individual product details """

    expense = get_object_or_404(Expense, pk=expense_id)

    context = {
        'expense': expense,
    }

    return render(request, 'expense/expense_detail.html', context)


@login_required
def add_expense(request, expense_id=""):
    """ upload image to Google vision API """
    profile = get_object_or_404(UserProfile, user=request.user)
    profiles = []
    tip_split = False
    current_user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST" and request.FILES != {}:
        # try:
        expense_id = uuid.uuid4().hex.upper()
        image = request.FILES['image']
        content = image.read()
        image_url = ""

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
        # avoid overwriting existing file
        if not media_storage.exists(file_path_within_bucket):
            media_storage.save(file_path_within_bucket, image)
            image_url = media_storage.url(file_path_within_bucket)

        result_dict = upload_to_Document_AI(mime_type, content)
        line_items = update_line_items(result_dict)
        normalized_items = update_normalized_items(result_dict)

        context = {
            'expense_id': expense_id,
            'image_url': image_url,
            'profile': profile,
            'normalized_items': normalized_items,
            'line_items': line_items,
        }

        return render(request, 'expenses/edit_expense.html', context)
        # except error:
        #     messages.add_message(
        #         request, messages.ERROR, "Problem with image, please try again"
        #     )
        #     return render(request, "home/user_home.html")

    elif request.method == 'POST' and request.FILES == {}:

        print(request.POST.items)

        line_items = [v for k, v in request.POST.items()
                      if k.startswith('line_item ')]
        expense = Expense(
            image_url=request.POST.get('image_url', ''),
            expense_id=request.POST.get('expense_id', ''),
            supplier_name=request.POST.get('supplier_name', ''),
            supplier_address=request.POST.get('supplier_address', ''),
            supplier_phone=request.POST.get('supplier_phone', ''),
            user_profile=current_user_profile,
            total_amount=float(request.POST.get('total_amount', 0)),
            total_tax_amount=float(request.POST.get('total_tax_amount', 0)),
            tip_amount=float(request.POST.get('tip_amount', 0)),
            net_amount=float(request.POST.get('net_amount', 0)),
            line_item_count=line_items.__len__(),
            paid_amount=0
        )

        tip_split = request.POST.get('tip_split', False)

        expense.save()

        line_items = [v for k, v in request.POST.items()
                      if k.startswith('line_item ')]

        for line_item in line_items:
            items = line_item.split(" % ")
            user_profile = get_object_or_404(UserProfile, pk=int(items[3]))

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
            order_line_item.save()

        expense.update_totals()

        messages.info(request, 'Successfully Saved Expense!')
        return redirect(reverse("user_home"))

    else:
        template = 'expenses/upload_image.html'
        profile = get_object_or_404(UserProfile, user=request.user)

        context = {
            'profile': profile
        }
        return render(request, template, context)


@ login_required
def edit_expense(request, expense_id):
    """ add an expense after uploading an image """

    current_user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':

        messages.info(request, 'Successfully Saved Expense!')
        return render(request, "home/user_home.html", {"profile": current_user_profile}, args=[expense_id])

        # else:
        #     messages.error(request,
        #                    ('Failed to update product. '
        #                     'Please ensure the form is valid.'))
    else:
        # form = ProductForm(instance=product)
        messages.info(request, f'placeholder text')
        return render(request, "expense/edit_expense.html", {"profile": current_user_profile})


@ login_required
def delete_expense(request, expense_id):
    """ Delete a product from the store """
    if not request.user:
        messages.error(request, 'Sorry, only expense owners can do that.')
        return redirect(reverse('home/user_home.html'))

    expense = get_object_or_404(Expense, pk=expense_id)
    expense.delete()
    messages.success(request, 'Expense deleted!')
    return redirect(reverse('home/user_home.html'))


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
