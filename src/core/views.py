from django.shortcuts import render
from core.model.main import MyVQAModel
import os
from django.http import JsonResponse
from django.views import View
import numpy as np
import cv2
from .forms import ImageForm
import tensorflow as tf

vqaModel = None
with tf.Graph().as_default():
    vqaModel = MyVQAModel()

# Create your views here.
class indexView(View):
    def get(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        imageform = ImageForm()
        # image_path = os.path.join(BASE_DIR, 'hat.jpg')
        # vqaModel.run(image_path, "What is color of hat?")
        return render(self.request, "index.html", {"form": imageform})

    def post(self, *args, **kwargs):
        print(self.request.POST)
        return JsonResponse({"abc": 133}, status = 200)

currentImage = None
def postImage(request):
    if request.method == "POST" and request.is_ajax():
        form = ImageForm(request.POST, request.FILES)
        streamData = request.FILES['image'].read()
        image = np.asarray(bytearray(streamData), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        global currentImage
        currentImage = image
        # currentImage = request.FILES
        # print(request.POST, request.FILES)
        return JsonResponse({"success":True}, status=200)
    return JsonResponse({"success":False}, status=400)



def postQuestion(request):
    if request.method == "POST" and request.is_ajax():

        question = request.POST["question"]
        global vqaModel
        answers = vqaModel.run(currentImage, question)
        print(answers)
        return JsonResponse({"answers":answers}, status=200)
    return JsonResponse({"success":False}, status=400)

# def django_image_and_file_upload_ajax(request):
#     if request.method == 'POST':
#        form = ImageFileUploadForm(request.POST, request.FILES)
#        if form.is_valid():
#            form.save()
#            return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
#        else:
#            return JsonResponse({'error': True, 'errors': form.errors})
#     else:
#         form = ImageFileUploadForm()
#         return render(request, 'django_image_upload_ajax.html', {'form': form})