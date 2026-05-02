from django.urls import path
from . import views

urlpatterns = [
    path('<int:mission_pk>/', views.conversation, name='conversation'),
    path('<int:mission_pk>/send/', views.send_message, name='send_message'),
    path('<int:mission_pk>/poll/', views.poll_messages, name='poll_messages'),
]
