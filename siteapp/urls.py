from django.urls import path

from . import views

urlpatterns = [
    path('', views.choose),
    path('select.html',views.choose),
    path('list.html',views.clist),
    path('add.html',views.add,name='add'),
    path('delete.html',views.delete,name='delete'),
    path('update.html',views.modify,name='modify'),
]