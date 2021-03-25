from django.urls import path

from .views import PostViews

app_name = 'django_ocr_tutorial'

urlpatterns = [
    path('', PostViews.as_view(), name='file-upload')
]