from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('principal', 'Principal'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(blank=True)  # Allow email to be blank
    REQUIRED_FIELDS = []

  # Adjust the import as needed

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    admission_date = models.DateField()
    grade = models.CharField(max_length=10 )
    performance = models.TextField(blank=True)
    attendance_records = models.TextField(blank=True)
    disciplinary_actions = models.TextField(blank=True)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_fee = models.DecimalField(max_digits=10, decimal_places=2)
    attendance_percentage = models.FloatField(blank=True ,null=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.grade}"

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    class_teacher_of_grade = models.CharField(max_length=10)  # New field
    main_subject = models.CharField(max_length=100)  # New field
    extra_subjects = models.CharField(max_length=200, blank=True, null=True)
    # Add more fields specific to teachers here

class Principal(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)





class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        (0, 'Absent'),
        (1, 'Present'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)  # Automatically sets the date to the current date
    status = models.IntegerField(choices=ATTENDANCE_STATUS)  # Use choices for 0 and 1
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"



class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class Class(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

