from django.urls import path

from . import views

urlpatterns = [
    path('choose/', views.choose, name='choose'),
    path('clist/',views.clist,name='clist'),
    path('add/',views.add,name='add'),
    path('delete/',views.delete,name='delete'),
    path('modify/',views.modify,name='modify'),
]