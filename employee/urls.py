from django.urls import path
from . import views

urlpatterns = [
    path('employee_homepage/', views.employee_dashboard, name='employee_homepage'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/delete/<int:user_id>/', views.delete_employee, name='delete_employee'),
    path('available_courses/', views.available_courses, name='available_courses'),
    path('register_course/<int:course_id>/', views.register_course, name='register_course'),
    path('dashboard/', views.course_dashboard, name='employee_dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('request-enrollment/', views.request_enrollment, name='request_enrollment'),
]
