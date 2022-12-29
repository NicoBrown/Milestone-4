import io
import os
from PIL import Image
from django.shortcuts import render
from django.contrib import messages
from django.db import models
from google.cloud import vision


class expense(models.Model):
    sku = models.CharField(max_length=254, null=True, blank=True)
    title = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    data = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    import base64


def homepage(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except error:
            messages.add_message(
                request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "home.html")
        lang = request.POST["language"]

        # Imports the Google Cloud client library
        # Instantiates a client
        client = vision.ImageAnnotatorClient()

        # The name of the image file to annotate
        file_name = os.path.abspath(
            '/workspace/Milestone-4/wakeupcat.jpg')

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        print('Labels:')
        for label in labels:
            print(label.description)

        # client = vision.ImageAnnotatorClient()
        # response = client.annotate_image({
        #     'image': {'source': {'image_uri': 'gs://my-test-bucket/image.jpg'}},
        #     'features': [{'type_': vision.Feature.Type.FACE_DETECTION}]
        # })

        # return text to html
        return render(request, "user_home.html", response)

    return render(request, "user_home.html")
