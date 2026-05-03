from django.urls import path
from . import views

urlpatterns = [
    # Mission-based chat
    path('<int:mission_pk>/', views.conversation, name='conversation'),
    path('<int:mission_pk>/send/', views.send_message, name='send_message'),
    path('<int:mission_pk>/poll/', views.poll_messages, name='poll_messages'),
    # Direct inbox
    path('', views.inbox, name='inbox'),
    path('new/', views.new_conversation, name='new_conversation'),
    path('<int:pk>/chat/', views.direct_conversation, name='direct_conversation'),
    path('<int:pk>/chat/send/', views.direct_send, name='direct_send'),
    path('<int:pk>/chat/poll/', views.direct_poll, name='direct_poll'),
    path('<int:pk>/delete/', views.delete_conversation, name='delete_conversation'),
]
