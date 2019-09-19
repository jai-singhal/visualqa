from django.shortcuts import render
from core.model.main import MyVQAModel
import os
from django.http import JsonResponse
from django.views import View
import numpy as np
import cv2
from .forms import ImageForm
import tensorflow as tf
from .models import Question, VQAImage


vqaModel = None
with tf.Graph().as_default():
    vqaModel = MyVQAModel()

# Create your views here.
class indexView(View):
    def get(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        imageform = ImageForm()
        return render(self.request, "index.html", {"form": imageform})


def postImage(request):
    if request.method == "POST" and request.is_ajax():
        instance = ImageForm(request.POST, request.FILES)
        instance = instance.save()
        # instance.user = request.user
        return JsonResponse({"success":True, "image_id": instance.id}, status=200)
    return JsonResponse({"success":False}, status=400)


def postQuestion(request):
    if request.method == "POST" and request.is_ajax():
        instance = Question()
        question = request.POST["question"]
        image_id = request.POST["image_id"]

        instance.question = question
        instance.image = VQAImage.objects.get(id = image_id)
        answers = vqaModel.run(instance.image.image.url, question)
        instance.answer = answers[0]["label"]
        instance.save()
        return JsonResponse({"answers":answers}, status=200)
    return JsonResponse({"success":False}, status=400)

