from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import Student
from .forms import StudentForm

# 🔹 Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username  # store in session
            response = redirect('student_list')
            response.set_cookie('last_login', username)  # store in cookie
            return response
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'login.html')

# 🔹 Logout View
def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('last_login')
    return response

# 🔹 Student List (View + Filter + Sort)
def student_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    students = Student.objects.all()

    search = request.GET.get('search')
    sort_by = request.GET.get('sort_by')

    if search:
        students = students.filter(name__icontains=search)

    if sort_by:
        students = students.order_by(sort_by)

    return render(request, 'student_list.html', {'students': students})

# 🔹 Add Student
def add_student(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

# 🔹 Edit Student
def edit_student(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

# 🔹 Delete Student
def delete_student(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('student_list')
