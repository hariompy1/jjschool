
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




@user_passes_test(is_principal, login_url='principal_login')
def list_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'principal/list_teachers.html', {'teachers': teachers})


@user_passes_test(is_principal, login_url='principal_login')
def edit_teacher(request, teacher_id):
    teacher_user = get_object_or_404(CustomUser, id=teacher_id)
    teacher = get_object_or_404(Teacher, user=teacher_user)
    
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=teacher_user)
        teacher_form = TeacherForm(request.POST, instance=teacher)
        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save()
            teacher_form.save()
            return redirect('list_teachers')
    else:
        user_form = CustomUserForm(instance=teacher_user)
        teacher_form = TeacherForm(instance=teacher)
    
    return render(request, 'principal/edit_teacher.html', {'user_form': user_form, 'teacher_form': teacher_form})


@user_passes_test(is_principal, login_url='principal_login')
def delete_teacher(request, teacher_id):
    teacher_user = get_object_or_404(CustomUser, id=teacher_id)
    teacher = get_object_or_404(Teacher, user=teacher_user)
    
    if request.method == 'POST':
        teacher_user.delete()
        return redirect('list_teachers')
    
    return render(request, 'principal/delete_teacher.html', {'teacher': teacher})


@user_passes_test(is_principal, login_url='principal_login')
def view_student_details(request, student_id):
    student = get_object_or_404(Student, user__id=student_id)
    return render(request, 'principal/view_student_details.html', {'student': student})


@user_passes_test(is_principal, login_url='principal_login')
def view_teacher_details(request, teacher_id):
    teacher = get_object_or_404(Teacher, user__id=teacher_id)
    return render(request, 'principal/view_teacher_details.html', {'teacher': teacher})


@user_passes_test(is_principal, login_url='principal_login')
def view_attendance_records(request):
    attendance_records = Attendance.objects.all()
    return render(request, 'principal/view_attendance_records.html', {'attendance_records': attendance_records})


@user_passes_test(is_principal, login_url='principal_login')
def view_performance_reports(request):
    students = Student.objects.all()
    return render(request, 'principal/view_performance_reports.html', {'students': students})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student, Attendance, Teacher
from .forms import AttendanceForm

def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Student, Attendance, Teacher
from django.contrib import messages

@login_required
def add_attendance(request):
    today = timezone.now().date()
    teacher = request.user.teacher
    students = Student.objects.filter(grade=teacher.class_teacher_of_grade).order_by('first_name', 'last_name')

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.pk}', '0')  # Default to '0' (Absent)
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                date=today,
                defaults={'status': status, 'class_teacher': teacher}
            )
            if not created:
                attendance.status = status
                attendance.save()

        messages.success(request, "Attendance has been recorded successfully.")
        return redirect('teachers_dashboard')

    attendance_exists = Attendance.objects.filter(student__in=students, date=today).exists()
    class_name = teacher.class_teacher_of_grade

    context = {
        'today': today,
        'class_name': class_name,
        'students': students,
        'attendance_exists': attendance_exists,
    }

    return render(request, 'teacher/add_attendance.html', context)

from django.shortcuts import render
from .models import Student, Attendance
from datetime import date
from django.utils.dateparse import parse_date

def list_attendance(request):
    class_teacher = request.user.teacher
    students = Student.objects.filter(grade=class_teacher.class_teacher_of_grade, is_deleted=False).order_by('first_name')
    
    # Get the selected date from the request or default to today
    selected_date = request.GET.get('attendance_date')
    if selected_date:
        selected_date = parse_date(selected_date)
    else:
        selected_date = date.today()

    # Get attendance records for the selected date
    attendance_records = {attendance.student.pk: attendance.status for attendance in Attendance.objects.filter(date=selected_date)}

    context = {
        'students': students,
        'attendance_records': attendance_records,
        'selected_date': selected_date,
        'class_name': class_teacher.class_teacher_of_grade,
    }

    return render(request, 'teacher/list_attendance.html', context)













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


