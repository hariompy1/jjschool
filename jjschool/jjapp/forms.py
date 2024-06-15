from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

from django import forms
from .models import Teacher, CustomUser

class CustomUserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'role', 'password1', 'password2', 'first_name', 'last_name', 'email')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class PrincipalForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')



class TeacherLogForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']




class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher 
        fields = [ 'phone_number', 'class_teacher_of_grade',"main_subject","extra_subjects", 'address',  'date_of_birth']


class SudentForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')



class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'status']



class TeacherPriForm(AuthenticationForm):
    class Meta:
        model = Teacher
        fields = ['username', 'password', 'name', 'email', 'class_teacher_of_grade', 'main_subject', 'extra_subjects']
       
       

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'first_name', 'last_name', 'date_of_birth', 'admission_date', 'grade',  'total_fee', 'remaining_fee']

