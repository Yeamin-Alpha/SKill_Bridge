#url:

from django.urls import path
from community import views

urlpatterns = [
    path('add-post/', views.Posts, name='add_post'),
    path('community/', views.Posts, name='community'),

]
