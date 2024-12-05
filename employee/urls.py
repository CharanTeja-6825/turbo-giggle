from django.conf.urls.static import static
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('employee_homepage/', views.employee_dashboard, name='employee_homepage'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/delete/<int:user_id>/', views.delete_employee, name='delete_employee'),
    path('available_courses/', views.available_courses, name='available_courses'),
    path('register_course/<int:course_id>/', views.register_course, name='register_course'),
    path('dashboard/', views.course_dashboard, name='employee_dashboard'),
    path('course/<int:course_id>/', views.course_overview, name='course_overview'),
    path('request-enrollment/', views.request_enrollment, name='request_enrollment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)