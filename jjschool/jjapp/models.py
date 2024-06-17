from django.db import models
from django.utils import timezone
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
    grade = models.CharField(max_length=10)
    performance = models.TextField(blank=True)
    attendance_records = models.TextField(blank=True)
    disciplinary_actions = models.TextField(blank=True)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_fee = models.DecimalField(max_digits=10, decimal_places=2)
    attendance_percentage = models.FloatField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.roll_number:
            last_student = Student.objects.filter(grade=self.grade).order_by('-roll_number').first()
            if last_student and last_student.roll_number:
                next_roll_number = int(last_student.roll_number[-2:]) + 1
            else:
                next_roll_number = 1
            self.roll_number = f"{self.grade}{str(next_roll_number).zfill(2)}"
        super().save(*args, **kwargs)

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








class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        (0, 'Absent'),
        (1, 'Present'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_attendances')
    date = models.DateField(default=timezone.now)
    status = models.IntegerField(choices=ATTENDANCE_STATUS)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.class_teacher:
            self.class_teacher = Teacher.objects.filter(class_teacher_of_grade=self.student.grade).first()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"












