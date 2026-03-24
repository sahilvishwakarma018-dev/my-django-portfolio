from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/chat/', views.chatbot_query, name='chatbot_query'),
]
