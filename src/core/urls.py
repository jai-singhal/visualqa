from django.contrib import admin
from django.urls import path, include
from .views import indexView, postImage, postQuestion

urlpatterns = [
    path('', indexView.as_view()),
    path('ajax/upload/image', postImage),
    path('ajax/upload/question', postQuestion),


]
