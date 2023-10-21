from django.urls import path
from . import views

urlpatterns = [
    path("sms_callback/", views.index),
    path("smsadmin/", views.chart_view, name="stat")
]
