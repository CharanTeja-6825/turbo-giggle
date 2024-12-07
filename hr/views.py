from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import google.generativeai as ai
from .forms import CourseForm, MaterialForm, TrainingInquiryForm
from .models import Course, Material

# Configure chatbot API
try:
    API_KEY = 'AIzaSyBerItDJLRgdSL6z7dDqXH_ggEsmp6m12I'
    ai.configure(api_key=API_KEY)
    model = ai.GenerativeModel("gemini-pro")
    chat = model.start_chat()
except Exception as e:
    chat = None
    print(f"Error configuring chatbot: {e}")

def HomePage(request):
    return render(request, 'project/project_homepage.html')

@login_required
def home_redirect(request):
    return redirect('trainer_homepage' if len(request.user.username) == 4 else
                    'employee_homepage' if len(request.user.username) == 10 else
                    'hr_homepage')

def hr_dashboard(request):
    return render(request, 'hr/hr_homepage.html')

def register(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST['firstname'],
                last_name=request.POST['lastname']
            )
            user.save()
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Registration failed: {e}")
    return render(request, 'project/login_register.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return home_redirect(request)
        messages.error(request, 'Invalid username or password')
    return render(request, 'project/login_register.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')

@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            if (password := request.POST.get('password')):
                user.set_password(password)
                update_session_auth_hash(request, user)
            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('home_redirect')
        except Exception as e:
            messages.error(request, f"Error updating profile: {e}")
    return render(request, 'project/profile_update.html', {'user': request.user})

@login_required
def course_create(request):
    trainers = User.objects.filter(username__regex=r'^\d{4}$')
    if request.method == 'POST':
        try:
            form = CourseForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('course_list')
            messages.error(request, f"Form errors: {form.errors}")
        except Exception as e:
            messages.error(request, f"Error creating course: {e}")
    return render(request, 'courses/course_create.html', {'form': CourseForm(), 'trainers': trainers})

def course_list(request):
    return render(request, 'courses/course_list.html', {'courses': Course.objects.all()})

@require_POST
def course_delete(request, course_id):
    try:
        get_object_or_404(Course, id=course_id).delete()
        messages.success(request, "Course deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting course: {e}")
    return redirect('course_list')

@login_required
def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    trainers = User.objects.filter(username__regex=r'^\d{4}$')
    if request.method == 'POST':
        try:
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
                return redirect('course_list')
            messages.error(request, f"Form errors: {form.errors}")
        except Exception as e:
            messages.error(request, f"Error updating course: {e}")
    return render(request, 'courses/edit_courses.html', {'form': CourseForm(instance=course), 'trainers': trainers, 'course': course})

@login_required
def upload_material(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        try:
            form = MaterialForm(request.POST, request.FILES)
            if form.is_valid():
                material = form.save(commit=False)
                material.course = course
                material.save()
                return redirect('course_list')
            messages.error(request, f"Form errors: {form.errors}")
        except Exception as e:
            messages.error(request, f"Error uploading material: {e}")
    return render(request, 'hr/upload_material.html', {'form': MaterialForm(), 'course': course})

def chatbot_view(request):
    if request.method == 'POST':
        if not chat:
            return JsonResponse({'response': 'Chatbot service is unavailable.'})
        user_message = request.POST.get('message', '')
        if user_message.lower() == 'bye':
            return JsonResponse({'response': 'Goodbye!'})
        try:
            response = chat.send_message(user_message)
            return JsonResponse({'response': response.text})
        except Exception as e:
            return JsonResponse({'response': f"Error: {e}"})
    return render(request, 'project/chatbot.html')
