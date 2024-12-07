from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from .forms import CourseForm, MaterialForm, TrainingInquiryForm
from .models import Course, Material

#=====================================================================================================================#

def HomePage(request):
    try:
        return render(request, 'project/project_homepage.html')
    except Exception as e:
        messages.error(request, f"Error loading homepage: {str(e)}")
        return redirect('error_page')

@login_required
def home_redirect(request):
    try:
        username = request.user.username
        if len(username) == 4:
            return redirect('trainer_homepage')
        elif len(username) == 10:
            return redirect('employee_homepage')
        else:
            return redirect('hr_homepage')
    except Exception as e:
        messages.error(request, f"Error redirecting user: {str(e)}")
        return redirect('error_page')

def hr_dashboard(request):
    try:
        return render(request, 'hr/hr_homepage.html')
    except Exception as e:
        messages.error(request, f"Error loading HR dashboard: {str(e)}")
        return redirect('error_page')

#==============================================Login & Register View==================================================#

def register(request):
    try:
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            return redirect('login')
        return render(request, 'project/login_register.html')
    except Exception as e:
        messages.error(request, f"Error during registration: {str(e)}")
        return redirect('error_page')

def login_view(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if username.isdigit() and len(username) == 4:
                    return redirect('trainer_homepage')
                elif username.isdigit() and len(username) == 10:
                    return redirect('employee_homepage')
                else:
                    return redirect('hr_homepage')
            else:
                messages.error(request, 'Invalid username or password')

        return render(request, 'project/login_register.html')
    except Exception as e:
        messages.error(request, f"Error during login: {str(e)}")
        return redirect('error_page')

def logout_view(request):
    try:
        logout(request)
        return redirect('homepage')
    except Exception as e:
        messages.error(request, f"Error during logout: {str(e)}")
        return redirect('error_page')

#==================================================Profile View=======================================================#

@login_required
def update_profile(request):
    try:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = request.user
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.email = email
            if password:
                user.set_password(password)
                update_session_auth_hash(request, user)

            user.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('home_redirect')
        else:
            context = {'user': request.user}
            return render(request, 'project/profile_update.html', context)
    except Exception as e:
        messages.error(request, f"Error updating profile: {str(e)}")
        return redirect('error_page')

#=====================================================Course View=====================================================#

def course_create(request):
    try:
        trainers = User.objects.filter(username__regex=r'^\d{4}$')
        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('course_list')
            else:
                print(form.errors)
        else:
            form = CourseForm()
        return render(request, 'courses/course_create.html', {'form': form, 'trainers': trainers})
    except Exception as e:
        messages.error(request, f"Error creating course: {str(e)}")
        return redirect('error_page')

def course_list(request):
    try:
        courses = Course.objects.all()
        return render(request, 'courses/course_list.html', {'courses': courses})
    except Exception as e:
        messages.error(request, f"Error fetching course list: {str(e)}")
        return redirect('error_page')

@require_POST
def course_delete(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect('course_list')
    except Exception as e:
        messages.error(request, f"Error deleting course: {str(e)}")
        return redirect('error_page')

def course_update(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)
        trainers = User.objects.filter(username__regex=r'^\d{4}$')
        if request.method == 'POST':
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
                return redirect('course_list')
        else:
            form = CourseForm(instance=course)
        return render(request, 'courses/edit_courses.html', {'form': form, 'trainers': trainers, 'course': course})
    except Exception as e:
        messages.error(request, f"Error updating course: {str(e)}")
        return redirect('error_page')

#=====================================================================================================================#

def upload_material(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        if request.method == 'POST':
            form = MaterialForm(request.POST, request.FILES)
            if form.is_valid():
                material = form.save(commit=False)
                material.course = course
                material.save()
                return redirect('course_list')
        else:
            form = MaterialForm()
        return render(request, 'hr/upload_material.html', {'form': form, 'course': course})
    except Exception as e:
        messages.error(request, f"Error uploading material: {str(e)}")
        return redirect('error_page')

def training_success(request):
    try:
        return render(request, 'project/mail_sent.html')
    except Exception as e:
        messages.error(request, f"Error displaying success message: {str(e)}")
        return redirect('error_page')

