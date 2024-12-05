from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

#from ..hr.models import Course


#=========================================Employee Dashboard View=====================================================#

def employee_dashboard(request):
    return render(request, 'employee/employee_homepage.html')

def employee_list(request):
    # Filter users with 10-digit usernames (assuming this signifies employees)
    employees = User.objects.filter(username__regex=r'^\d{10}$')
    return render(request, 'employee/employee_details.html', {'employees': employees})

def delete_employee(request, user_id):
    # Retrieve the user by ID
    employee = get_object_or_404(User, id=user_id, username__regex=r'^\d{10}$')
    # Delete the employee
    employee.delete()
    messages.success(request, "Employee deleted successfully.")
    # Redirect to the employee list page
    return redirect('employee_list')

#=====================================================================================================================#

#Course Registration Employee

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hr.models import Course
from .models import EmployeeCourse

@login_required
def available_courses(request):
    courses = Course.objects.all()
    registered_courses = EmployeeCourse.objects.filter(employee=request.user).values_list('course_id', flat=True)
    available_courses = courses.exclude(id__in=registered_courses)
    return render(request, 'employee/course_list_for_employee.html', {'courses': available_courses})

@login_required
def register_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        EmployeeCourse.objects.create(employee=request.user, course=course)
        messages.success(request, f"You have successfully registered for {course.course_name}.")
        return redirect('available_courses')

    return render(request, 'employee/select_course.html', {'course': course})

#######################################################################################################################
#Course Dashboard

from hr.models import Course
from django.contrib.auth.models import User  # Assuming User model for employees

from django.shortcuts import render, get_object_or_404
from .models import EmployeeCourse

def course_dashboard(request):
    # Assuming the logged-in user is the employee
    employee = request.user

    # Fetch courses assigned to the employee using the EmployeeCourse model
    assigned_courses = Course.objects.filter(registrations__employee=employee)

    context = {
        'employee_name': employee.get_full_name(),
        'courses': assigned_courses,
    }
    return render(request, 'employee/employee_dashboard.html', context)

def request_enrollment(request):
    # Handle course enrollment requests
    if request.method == 'POST':
        # Logic to process the course request
        pass
    return render(request, 'employee/request_enrollment.html')

##########  COURSE DETAILS ##########

from django.shortcuts import render
from hr.models import Course

def course_overview(request, course_id):
    # Retrieve the course by ID
    course = Course.objects.get(id=course_id)

    # Pass the course object to the template
    return render(request, 'courses/course_overview.html', {'course': course})
