from django.urls import path
from . import views


urlpatterns = [
    path('<int:list_id>/', views.view_list, name='view_list'),
    path('new', views.new_list, name='new_list')
]
