from PIL import Image
from .models import Expense
from django.shortcuts import render, get_object_or_404
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from google.cloud import vision
import io
import os
import base64

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"kwik-split-0a449986ee26.json"

# from .forms import UserProfileForm
# from checkout.models import Order


@login_required
def add_image(request):
    """ upload image to Google vision API """
    # profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        # try:

        image = request.FILES['image']
        # lang = request.POST["language"]

        # Instantiates a client
        client = vision.ImageAnnotatorClient()

        # encode image to bytes
        content = image.read()

        image = vision.Image(content=content)

        # Performs label detection on the image file
        response = client.text_detection(image=image)
        labels = response.text_annotations

        print(response)

        context = {
            'labels': labels,
            'text_labels': response.text_annotations,
        }

        # return text to html
        return render(request, "expense_overview.html", context)
        # except error:
        #     messages.add_message(
        #         request, messages.ERROR, "No image selected or uploaded"
        #     )
        #     return render(request, "home/user_home.html")
    else:
        # form = ProductForm(instance=product)
        messages.info(request, f'placeholder text')

    template = 'expenses/upload_image.html'

    context = {
        # 'form': form,
        # 'orders': orders,
        # 'on_profile_page': True
    }

    return render(request, template, context)


@login_required
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
