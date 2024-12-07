from django.conf.urls.static import static
from django.shortcuts import render
from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.HomePage, name='homepage'),
    path('home/', views.home_redirect, name='home_redirect'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('hr_homepage/', views.hr_dashboard, name='hr_homepage'),
    path('logout/', views.logout_view, name='logout'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('create-course/', views.course_create, name='course_create'),
    path('courses/', views.course_list, name='course_list'),  # List all courses
    path('courses/delete/<int:course_id>/', views.course_delete, name='course_delete'),
    path('courses/<int:course_id>/edit/', views.course_update, name='course_update'),
    path('course/<int:course_id>/upload/', views.upload_material, name='upload_material'),
    path('chatbot_view/',views.chatbot_view,name='chatbot_view'),
    path('feedback/', views.feedback_create, name='feedback'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)