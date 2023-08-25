from django.urls import path
from . import api

urlpatterns = [
    path('', api.notifications, name='notification'),
    path('read/<uuid:id>/', api.read_notification, name='notification'),
]
