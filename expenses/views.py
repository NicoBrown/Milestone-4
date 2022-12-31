from dataclass_wizard import fromdict, asdict
from typing import List as PyList
from dataclasses import dataclass
from google.protobuf.json_format import MessageToJson
from PIL import Image
from .models import Expense
from django.shortcuts import render, get_object_or_404
from django import forms
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from google.cloud import documentai, vision_helpers
from google.api_core.client_options import ClientOptions
from google.protobuf.json_format import MessageToDict

# from .forms import UserProfileForm
# from checkout.models import Order

import json
import proto
import io
import os
import base64

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"kwik-split-0a449986ee26.json"


@dataclass
class line_element:
    id: int
    amount: str
    quantity: int
    unit_price: int
    description: str


# TODO(developer): Uncomment these variables before running the sample.
project_id = 'kwik-split'
location = 'eu'  # Format is 'us' or 'eu'
processor_id = '8a4fbaeb2765405e'  # Create processor before running sample
# Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information


@login_required
def add_image(request):
    """ upload image to Google vision API """
    # profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        try:
            opts = ClientOptions(
                api_endpoint=f"{location}-documentai.googleapis.com")
            # lang = request.POST["language"]
            client = documentai.DocumentProcessorServiceClient(
                client_options=opts)
            name = client.processor_path(project_id, location, processor_id)

            # get posted image and encode image to in memory byte stream
            image = request.FILES['image']
            image_content = image.read()

            # need to set mime type on image upload Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
            mime_type = image.content_type.split('.')[-1]

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

            entities = []
            line = {}

            # # # Grab each key/value pair and their corresponding confidence scores.
            # for entity in json_dump:
            #     if entity.type == "line_item":
            #         for key, value in entity.items():
            #             line.update({key: value})

            #         entities.append(line)
            #         line.clear()

            context = {
                'entities': json_dump,
            }

            return render(request, "expense_overview.html", context)
        except error:
            messages.add_message(
                request, messages.ERROR, "Problem with image, please try again"
            )
            return render(request, "home/user_home.html")
    else:

        profiles = Profile.objects.exclude(user=request.user)
        template = 'expenses/upload_image.html'
        context = {
            # 'on_profile_page': True,
            "profiles": profiles
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
            messages.success(request, 'Successfully updated product!')
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
