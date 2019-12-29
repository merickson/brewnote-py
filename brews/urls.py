from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:brew_id>/addfermentation/', views.addfermentation, name='addfermentation'),
    path('<int:brew_id>/', views.brewdetail, name='brewdetail'),
    path('addbatch/', views.addbatch, name='addbatch'),
]
