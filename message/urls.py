



from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_list, name='message_list'),
    path('send/<int:receiver_id>/', views.send_message, name='send_message'),
    path('read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('message_list/', views.message_list, name='message_list'),
    path('send_message/', views.send_message, name='send_message'),
     path('chat_interface/', views.chat_interface, name='chat_interface'),


]


