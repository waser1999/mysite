from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index),
    path('login.html', views.index),
    path('register.html',views.register),
    path('select.html',views.choose,name='select'),
    path('list.html',views.clist,name='list'),
    path('add.html',views.add,name='add'),
    path('delete.html',views.delete,name='delete'),
    path('update.html',views.modify,name='modify'),
    path('jsonAPI',views.api,name='api'),
]