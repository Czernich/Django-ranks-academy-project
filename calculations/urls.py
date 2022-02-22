from django.urls import path
from . import views

urlpatterns = [
    path('', views.frontSite, name='front_site'),
    path('create-project/', views.createProject, name='create_project'),
    path('show-project/<str:pk>/', views.showProjectResult, name='show_project')
]