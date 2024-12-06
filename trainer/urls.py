from django.urls import path
from . import views

urlpatterns = [
    path('trainer_homepage/', views.trainer_dashboard, name='trainer_homepage'),
    path('trainers/', views.trainer_list, name='trainer_list'),
    path('trainers/delete/<int:user_id>/', views.delete_trainer, name='delete_trainer'),
    path('trainer/courses/', views.assigned_courses, name='trainer_courses'),
    path('assigned_employees', views.trainer_employee_view, name='trainer_employees'),
]
