
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import *
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import user_passes_test




# def test(request):
#     return render(request, 'index.html')

def home_page(request):
    notifications = Notification.objects.all().order_by('-created_at')
    information = "Welcome to Our School's Website! Here you'll find all the latest updates and announcements."
    return render(request, 'home.html', {'notifications': notifications, 'information': information})



def logout_view(request):
    user_role = request.user.role if request.user.is_authenticated else None
    logout(request)

    if user_role == 'student':
        return redirect('student_login')
    elif user_role == 'teacher':
        return redirect('teacher_login')
    elif user_role == 'principal':
        return redirect('principal_login')
    else:
        return redirect('home_page')
    
    



def teachers_page(request):
    return render(request, 'teachers_page.html')

def manager_page(request):
    return render(request, 'manager_page.html')













#principal thinks 

def principal_login(request):
    if request.method == 'POST':
        form = PrincipalForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('principal_dashboard')

    else:
        form = PrincipalForm()
    return render(request, 'principal/login.html', {'form': form})




@user_passes_test(is_principal, login_url='principal_login')
def principal_dashboard(request):
    notifications = Notification.objects.all()
    return render(request, 'principal/dashboard.html', {'notifications': notifications})




@user_passes_test(is_principal, login_url='principal_login')
def manage_notifications(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Notification.objects.create(title=title, content=content)
        return redirect('manage_notifications')
    notifications = Notification.objects.all()
    return render(request, 'principal/manage_notifications.html', {'notifications': notifications})


@user_passes_test(is_principal, login_url='principal_login')
def edit_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if request.method == 'POST':
        notification.title = request.POST.get('title')
        notification.content = request.POST.get('content')
        notification.save()
        return redirect('manage_notifications')
    return render(request, 'principal/edit_notification.html', {'notification': notification})


@user_passes_test(is_principal, login_url='principal_login')
def delete_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.delete()
    return redirect('manage_notifications')

@user_passes_test(is_principal, login_url='principal_login')
def edit_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if request.method == 'POST':
        notification.title = request.POST.get('title')
        notification.content = request.POST.get('content')
        notification.save()
        return redirect('manage_notifications')
    return render(request, 'principal/edit_notification.html', {'notification': notification})




def list_students(request):
    students = Student.objects.filter(is_deleted=False)
    return render(request, 'principal/list_students.html', {'students': students})


@user_passes_test(is_principal, login_url='principal_login')
def deleted_students(request):
        students = Student.objects.filter(is_deleted=True)
        return render(request, 'principal/deleted_students.html', {'students': students})


def soft_delete_student(request, student_id):
    student = get_object_or_404(Student, user__id=student_id)
    student.is_deleted = True
    student.save()
    return redirect('list_students')


@user_passes_test(is_principal, login_url='principal_login')
def restore_student(request, student_id):
    student = get_object_or_404(Student, user_id=student_id)
    student.is_deleted = False
    student.save()
    return redirect('deleted_students')


def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            user = request.user  
            student = form.save(commit=False)
            student.user = user  
            student.save()  
            return redirect('principal_dashboard')
    else:
        form = StudentForm()
    return render(request, 'principal/add_student.html', {'form': form})



@user_passes_test(is_principal, login_url='principal_login')
def edit_student(request, student_id):
    student_user = get_object_or_404(CustomUser, id=student_id)
    student = get_object_or_404(Student, user=student_user)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('list_students') 
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'principal/edit_student.html', {'form': form, 'student': student})


@login_required
@user_passes_test(is_principal, login_url='principal_login')
def delete_student(request, student_id):
    # Fetch the CustomUser instance associated with the student_id
    student_user = get_object_or_404(CustomUser, id=student_id)
    # Fetch the Student instance related to the CustomUser instance
    student = get_object_or_404(Student, user=student_user)
    
    if request.method == 'POST':
        student.delete()
        return redirect('list_students')
    
    return render(request, 'principal/delete_student.html', {'student': student})



@user_passes_test(is_principal, login_url='principal_login')
def add_teacher(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'teacher'
            user.set_password(user_form.cleaned_data['password'])  # Set the password correctly
            user.save()
            
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            
            return redirect('principal_dashboard')  # Redirect to principal dashboard after successful addition
        else:
            error = "Please correct the errors below."
            return render(request, 'principal/add_teacher.html', {'user_form': user_form, 'teacher_form': teacher_form, 'error': error})
    else:
        user_form = CustomUserForm()
        teacher_form = TeacherForm()
    return render(request, 'principal/add_teacher.html', {'user_form': user_form, 'teacher_form': teacher_form})








def teacher_login(request):
    if request.method == 'POST':
        form = TeacherLogForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.role == 'teacher':  # Ensure the user is a teacher
                login(request, user)
                return redirect('teachers_dashboard')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = TeacherLogForm()
    return render(request, 'teacher/login.html', {'form': form})


@user_passes_test(is_teacher, login_url='teacher_login')
def teachers_dashboard(request):
    return render(request, 'teacher/dashboard.html')



def student_login(request):
    if request.method == 'POST':
        form = StudentForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.role == 'teacher':  # Ensure the user is a teacher
                login(request, user)
                return redirect('student_dashboard')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = TeacherLogForm()
    return render(request, 'student/login.html', {'form': form})


from django.http import HttpResponse


@user_passes_test(is_student, login_url='teacher_login')
def student_dashboard(request):
    return HttpResponse("hey this is student dashboard")






