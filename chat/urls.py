from django.urls import path
from . import api

urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('<uuid:id>/', api.conversation_detail, name='conversation_detail'),
    path('<uuid:id>/send/', api.conversation_send_message,
         name='conversation_send_message'),
    path('<uuid:id>/get_or_create/', api.conversation_get_or_create,
         name='conversation_get_or_create'),
]
