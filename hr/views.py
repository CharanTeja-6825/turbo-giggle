from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from .forms import CourseForm
from .models import Course

#=====================================================================================================================#
def HomePage(request):
    return render(request, 'project/project_homepage.html')

@login_required
def home_redirect(request):
    username = request.user.username
    if len(username) == 4:  # Trainer (4-digit username)
        return redirect('trainer_homepage')
    elif len(username) == 10:  # Employee (10-digit username)
        return redirect('employee_homepage')
    else:  # HR or others
        return redirect('hr_homepage')

def hr_dashboard(request):
    return render(request, 'hr/hr_homepage.html')

#==============================================Login & Register View==================================================#

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        # Redirect based on username format
        if username.isdigit() and len(username) == 4:
            return redirect('login')  # Replace with your URL
        elif username.isdigit() and len(username) == 10:
            return redirect('login')  # Replace with your URL
        else:
            return redirect('login')  # Replace with your URL

    return render(request, 'project/login_register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user using the default User model
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Redirect based on username format
            if username.isdigit() and len(username) == 4:
                return redirect('trainer_homepage')  # Replace with your URL
            elif username.isdigit() and len(username) == 10:
                return redirect('employee_homepage')  # Replace with your URL
            else:
                return redirect('hr_homepage')  # Replace with your URL
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'project/login_register.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')

#==================================================Profile View=======================================================#
@login_required
def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Get the current user
        user = request.user

        # Update user information
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)  # Keep user logged in after password change

        # Save changes to the user
        user.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('home_redirect')  # Redirect to home page or another appropriate page

    else:
        context = {
            'user': request.user
        }
        return render(request, 'project/profile_update.html', context)

#=====================================================Course View=====================================================#

from django.shortcuts import render, redirect
from .forms import CourseForm
from django.contrib.auth.models import User

def course_create(request):
    # Filter trainers: users with a 4-character username
    trainers = User.objects.filter(username__regex=r'^\d{4}$')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Update this to your actual course list URL name
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = CourseForm()

    # Render the form template
    return render(request, 'courses/course_create.html', {'form': form, 'trainers': trainers})

def course_list(request):
    # Fetch all courses from the database
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@require_POST
def course_delete(request, course_id):
    # Get the course by ID or return a 404 if not found
    course = get_object_or_404(Course, id=course_id)

    # Delete the course and show a success message
    course.delete()
    messages.success(request, "Course deleted successfully.")

    # Redirect to the course list view after deletion
    return redirect('course_list')

def course_update(request, course_id):
    # Fetch the course object or return a 404 if not found
    course = get_object_or_404(Course, id=course_id)
    trainers = User.objects.filter(username__regex=r'^\d{4}$')

    # Handle form submission
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Ensure 'course_list' URL is defined in your urls.py
    else:
        form = CourseForm(instance=course)

    # Pass the form and trainers to the template
    return render(request, 'courses/edit_courses.html', {'form': form, 'trainers': trainers,
                                                         'course': course})
#=====================================================================================================================#

#COURSE MATERIAL UPLOAD

from django.shortcuts import render, redirect
from .models import Course, Material
from .forms import MaterialForm

def upload_material(request, course_id):
    course = Course.objects.get(id=course_id)  # Get the course to which the material belongs
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)  # Include `request.FILES` to handle file uploads
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course  # Associate the material with the course
            material.save()  # Save the material to the database
            return redirect('course_list')  # Redirect to course details page after upload
    else:
        form = MaterialForm()

    return render(request, 'hr/upload_material.html', {'form': form, 'course': course})


# views.py
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import TrainingInquiryForm


# views.py
def training_success(request):
    return render(request, 'project/mail_sent.html')

############# CHATBOT ##########################3

# views.py
from django.http import JsonResponse
from django.shortcuts import render
import google.generativeai as ai

# Configure the API
API_KEY = 'AIzaSyBerItDJLRgdSL6z7dDqXH_ggEsmp6m12I'
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()

def chatbot_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        if user_message.lower() == 'bye':
            return JsonResponse({'response': 'Goodbye!'})
        response = chat.send_message(user_message)
        return JsonResponse({'response': response.text})
    return render(request, 'project/chatbot.html')