from django.urls import path
from django.views.generic import TemplateView
from .views import ConvertImageView

urlpatterns = [
    path('convert/', ConvertImageView.as_view(), name='convert-image'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]