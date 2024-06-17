from django.urls import path
from .views import *

urlpatterns = [
     path('', home_page, name='home_page'),
     path('login', principal_login, name='principal_login'),
     path('principal/dashboard/', principal_dashboard, name='principal_dashboard'),
     path('logout/', logout_view, name='logout'),
     path('principal/manage-notifications/', manage_notifications, name='manage_notifications'),
     path('principal/edit-notification/<int:notification_id>/', edit_notification, name='edit_notification'),
     path('principal/delete-notification/<int:notification_id>/', delete_notification, name='delete_notification'),
     path('principal/list-students/', list_students, name='list_students'),
     path('principal/deleted-students/', deleted_students, name='deleted_students'),
     path('principal/soft-delete-student/<int:student_id>/', soft_delete_student, name='soft_delete_student'),
     path('principal/restore-student/<int:student_id>/', restore_student, name='restore_student'),
     path('principal/add-student/', add_student, name='add_student'),
     path('principal/edit-student/<int:student_id>/', edit_student, name='edit_student'),
     path('principal/delete-student/<int:student_id>/', delete_student, name='delete_student'),
     path('principal/add_teacher/', add_teacher, name='add_teacher'),
     path('teacher/login/', teacher_login, name='teacher_login'),
     path('teacher/dashboard/', teachers_dashboard, name='teachers_dashboard'),
     # path('', test)
     path("student/login", student_login , name= "student_login"),
     path("student/dashboard", student_dashboard, name ="student_dashboard"),
     path('teacher/add-attendance/', add_attendance, name='add_attendance'),
     path('teacher/list-attendance/', list_attendance, name='list_attendance'),


     path('chatbot/chat/', chatbot_view, name='chatbot_view'),






     path('principal/list-teachers/', list_teachers, name='list_teachers'),
     path('principal/edit-teacher/<int:teacher_id>/', edit_teacher, name='edit_teacher'),
     path('principal/delete-teacher/<int:teacher_id>/', delete_teacher, name='delete_teacher'),
     path('principal/view-teacher-details/<int:teacher_id>/', view_teacher_details, name='view_teacher_details'),
     path('principal/view-student-details/<int:student_id>/', view_student_details, name='view_student_details'),
     path('principal/view-attendance-records/', view_attendance_records, name='view_attendance_records'),
     path('principal/view-performance-reports/', view_performance_reports, name='view_performance_reports'),

]



# urlpatterns = [
#     
#     path('teachers/', teachers_page, name='teachers_page'),
#     path('manager/', manager_page, name='manager_page'),
#     path('principal/list-students/', list_students, name='list_students'),
#     path('principal/deleted-students/', deleted_students, name='deleted_students'),
#     path('principal/soft-delete-student/<int:student_id>/', soft_delete_student, name='soft_delete_student'),
#     path('principal/restore-student/<int:student_id>/', restore_student, name='restore_student'),
#     path('principal/add-student/', add_student, name='add_student'),
#     path('principal/edit-student/<int:student_id>/', edit_student, name='edit_student'),
#     path('principal/delete-student/<int:student_id>/', delete_student, name='delete_student'),
#     path('logout/', logout_view, name='logout'),
#     path('teacher/login/', teacher_login, name='teacher_login'),
#     path('teacher/dashboard/', teachers_dashboard, name='teachers_dashboard'),
#     path('principal/add_teacher/', add_teacher, name='add_teacher'),

# ]
