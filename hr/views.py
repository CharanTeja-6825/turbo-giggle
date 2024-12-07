from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import google.generativeai as ai
from .forms import CourseForm, MaterialForm
from .models import Course

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



from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        first_name = request.POST.get('firstname', '').strip()
        last_name = request.POST.get('lastname', '').strip()

        # Username validation
        if len(username) < 4:
            messages.error(request, "Username must be at least 4 characters long.")
        elif not (username.isalpha() or username.isdigit()):
            messages.error(request, "Username must contain only letters or only numbers.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Registration failed: {e}")

        # Redirect back to the register page if validation fails
        return redirect('register')  # Ensure 'register' is a named URL for this view.

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


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import FeedbackForm
from .models import Feedback  # Assuming you have a Feedback model to store feedback data


def feedback_create(request):
    trainers = User.objects.filter(username__regex=r'^\d{4}$')  # Filter trainers with username length of 4

    if request.method == 'POST':
        try:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your feedback has been submitted successfully!')
                return redirect('feedback_list')  # Redirect to feedback list page or other page
            messages.error(request, f"Form errors: {form.errors}")
        except Exception as e:
            messages.error(request, f"Error submitting feedback: {e}")

    return render(request, 'feedback/employee_feedback.html', {'form': FeedbackForm(),
                                                               'trainers': trainers})


def feedback_list(request):
    feedbacks = Feedback.objects.all()  # Assuming you have a Feedback model
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})