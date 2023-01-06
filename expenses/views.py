from typing import List as PyList
from PIL import Image
from .models import Expense
from profiles.models import UserProfile
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from google.protobuf.json_format import MessageToDict
from base64 import b64encode

# from .forms import UserProfileForm
# from checkout.models import Order

import json
import proto
import io
import os
import base64

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"kwik-split-0a449986ee26.json"

# TODO(developer): Uncomment these variables before running the sample.
project_id = 'kwik-split'
location = 'eu'  # Format is 'us' or 'eu'
processor_id = '8a4fbaeb2765405e'  # Create processor before running sample
# Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information


@login_required
def add_image(request):
    """ upload image to Google vision API """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        profiles = []

        if 'add_users' in request.POST:
            query = request.POST.getlist('add_users')
            for i in query:
                profiles.append(get_object_or_404(
                    UserProfile, pk=i))
    # try:
        opts = ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com")
        # lang = request.POST["language"]
        client = documentai.DocumentProcessorServiceClient(
            client_options=opts)
        name = client.processor_path(project_id, location, processor_id)

        # get posted image and encode image to in memory byte stream
        image = request.FILES['image']
        image_content = image.read()

        encoded = b64encode(image_content)
        # need to set mime type on image upload Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
        mime_type = image.content_type.split('.')[-1]
        mime = mime_type + ";" if mime_type else ";"

        # Load Binary Data into Document AI RawDocument Object
        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type)

        # Configure the process request
        process_request = documentai.ProcessRequest(
            name=name, raw_document=raw_document)

        result = client.process_document(request=process_request)

        # For a full list of Document object attributes, please reference this page:
        # https://cloud.google.com/python/docs/reference/documentai/latest/google.cloud.documentai_v1.types.Document

        document = result.document

        json_dump = [proto.Message.to_dict(
            entity) for entity in document.entities]

        line_items = {}
        line_item = {}
        normalized_item = {}
        normalized_items = {}

        # # # Grab each key/value pair and their corresponding confidence scores.
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

        for entity in json_dump:
            if len(entity['properties']) == 0:
                if entity.get('normalized_value') is not None:
                    normalized_items[entity["type_"]
                                     ] = entity['normalized_value']['text']
            if len(entity['properties']) == 1:
                if entity.get('properties') is not None:
                    normalized_items[entity["type_"]
                                     ] = entity['mention_text']

        context = {
            'profile': profile,
            'image_uri': encoded,
            'normalized_items': normalized_items,
            'line_items': line_items,
            'entities': json_dump,
            'profiles': profiles,
        }
        return render(request, "expenses/expense_overview.html", context)
        # except error:
        #     messages.add_message(
        #         request, messages.ERROR, "Problem with image, please try again"
        #     )
        #     return render(request, "home/user_home.html")
    else:
        template = 'expenses/upload_image.html'
        profile = get_object_or_404(UserProfile, user=request.user)

        context = {
            'profile': profile
        }
        return render(request, template, context)


@ login_required
def add_expense(request, product_id):
    """ add an expense after uploading an image """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           ('Failed to update product. '
                            'Please ensure the form is valid.'))
    else:
        # form = ProductForm(instance=product)
        messages.info(request, f'placeholder text')


def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document's text. This function converts
    offsets to a string.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in layout.text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response
