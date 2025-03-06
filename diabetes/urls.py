from django.urls import path
from . import views

""" urlpatterns = [
    path('', views.home, name='home'),
    path("bloodcheck/", views.bloodcheckView, name='bloodcheck'),
    path('bloodcheck_list/', views.bloodcheck_list, name='bloodcheck_list'),
    path('insulin/', views.insulin_food_entry, name='insulin_food_entry'),
    path('insulin-food-list/', views.insulin_food_list, name='insulin-food-list'),
] """

urlpatterns = [
    path('', views.home, name='home'),
    path('bloodcheck_list/', views.bloodcheck_list, name='bloodcheck_list'),
    path('insulin-food-list/', views.insulin_food_list, name='insulin-food-list'),
    path('insulin/<int:id>/', views.insulin_detail, name='insulin_detail'),
    path('food/<int:id>/', views.food_detail, name='food_detail'),
    path('bloodcheck/<int:id>/', views.bloodcheck_detail, name='bloodcheck_detail'),
    path('insulin/<int:id>/edit/', views.insulin_edit, name='insulin_edit'),
    path('food/<int:id>/edit/', views.food_edit, name='food_edit'),
    path('bloodcheck/<int:id>/edit/',
         views.bloodcheck_edit, name='bloodcheck_edit'),
    path('insulin/<int:id>/delete/', views.insulin_delete, name='insulin_delete'),
    path('food/<int:id>/delete/', views.food_delete, name='food_delete'),
    path('bloodcheck/<int:id>/delete/',
         views.bloodcheck_delete, name='bloodcheck_delete'),
]
