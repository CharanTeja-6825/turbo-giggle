from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from hr.models import Course


#===============================================Trainer Dashboard View================================================#

@login_required
def trainer_dashboard(request):
    # Ensure the logged-in user is a trainer (username is 4 digits)
    trainer = request.user
    if not trainer.username.isdigit() or len(trainer.username) != 4:
        return render(request, 'error.html', {'message': 'You are not authorized to view this page.'})

    # Fetch courses assigned to this trainer
    courses = Course.objects.filter(trainer=trainer)

    return render(request, 'trainer/trainer_homepage.html', {
        'trainer': trainer,
        'courses': courses,
    })

def trainer_list(request):
    trainers = User.objects.filter(username__regex=r'^\d{4}$')
    return render(request, 'trainer/trainer_details.html', {'trainers': trainers})

def delete_trainer(request, user_id):
    # Retrieve the user by ID
    trainer = get_object_or_404(User, id=user_id, username__regex=r'^\d{4}$')
    trainer.delete()
    messages.success(request, "Trainer deleted successfully.")
    return redirect('trainer_list')


def assigned_courses(request):
    # Filter courses where the trainer matches the logged-in user
    trainer_courses = Course.objects.filter(trainer=request.user)
    context = {
        'trainer': request.user,
        'courses': trainer_courses,
    }
    return render(request, 'trainer/assigned_courses.html', context)
#=====================================================================================================================#

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hr.models import Course
from employee.models import EmployeeCourse

@login_required
def trainer_employee_view(request):
    # Get the currently logged-in trainer
    trainer = request.user

    # Get the courses assigned to the trainer
    trainer_courses = Course.objects.filter(trainer=trainer)

    # Retrieve employees registered for these courses
    registrations = EmployeeCourse.objects.filter(course__in=trainer_courses).select_related('employee', 'course')

    # Structure the data to pass to the template
    context = {
        'trainer': trainer,
        'trainer_courses': trainer_courses,
        'registrations': registrations,
    }
    return render(request, 'trainer/trainer_employee.html', context)
