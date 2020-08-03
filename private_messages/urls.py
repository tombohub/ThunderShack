from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('send/', views.send, name='messages-send'),
    path('send_ajax/', views.send_ajax, name='messages-send-ajax'),
    path('inbox/', views.inbox, name='messages-inbox'),
    path('conversation/<int:pk>/', views.conversation, name='messages-conversation'),
    path('conversation_json/<int:pk>/', views.conversation_json, name='messages-conversation-json'),
    path('conversation_html/<int:pk>/', views.conversation_html, name='messages-conversation-html'),
    path('converation/start/', views.conversation_start, name='messages-conversation-start'),
    #path('sent/', views.sent, name='messages-sent'),
]