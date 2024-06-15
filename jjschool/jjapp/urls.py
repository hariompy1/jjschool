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
