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

# Create your views here.
vqaModel = None
class indexView(View):
    def get(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        imageform = ImageForm()
        return render(self.request, "index.html", {"form": imageform})


def postImage(request):
    if request.method == "POST" and request.is_ajax():
        instance = ImageForm(request.POST, request.FILES)
        instance = instance.save()
        global vqaModel
        vqaModel = get_tfa_model()
        # instance.user = request.user
        return JsonResponse({"success":True, "image_id": instance.id}, status=200)
    return JsonResponse({"success":False}, status=400)


def get_tfa_model(retry = 3):
    vqaModel = None
    if not retry:
        return None

    with tf.Graph().as_default():
        try:
            vqaModel = MyVQAModel()
        except Exception as e:
            print("Retrying!!")
            get_tfa_model(retry-1)

    return vqaModel


def postQuestion(request):
    if request.method == "GET" and request.is_ajax():
        instance = Question()
        question = request.GET.get("question", None)
        image_id = request.GET.get("image_id", None)
        question_no = int(request.GET.get("question_no", None))
        print(question)
        if question and image_id:
            instance.question = question
            instance.image = VQAImage.objects.get(id = image_id)
            try:
                answers = vqaModel.run(instance.image.image.url, question, question_no)
            except Exception as e:
                return JsonResponse({"errors":e}, status=400)
            print(answers)
            instance.answer = answers[0]["label"]
            instance.save()
            return JsonResponse({"answers":answers}, status=200)

    return JsonResponse({"success":False}, status=400)

