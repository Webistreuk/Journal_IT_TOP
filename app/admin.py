from django.contrib import admin
from .models import Autoriz, Professor, Student, Subjects, Courses_of_Students, balance_topcoins_and_topgems, All_payment_of_education, Students_payment_account, image_student, image_professor, Add_HW_Professor_to_course

@admin.register(Autoriz)
class AutorizAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'email')
    list_filter = ('user',)
    ordering = ('id',)

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic', 'leads_the_subject')
    list_display_links = ('id', 'name', 'surname')
    search_fields = ('name', 'surname', 'patronymic', 'leads_the_subject')
    list_filter = ('name',)
    ordering = ('id',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic')
    list_display_links = ('id', 'name', 'surname')
    search_fields = ('name', 'surname', 'patronymic')
    list_filter = ('name',)
    ordering = ('id',)

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_subject')
    list_display_links = ('id', 'name_subject')
    search_fields = ('name_subject',)
    list_filter = ('name_subject',)
    ordering = ('id',)

@admin.register(Courses_of_Students)
class Courses_of_StudentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'course')
    list_display_links = ('id', 'course')
    search_fields = ('course',)
    list_filter = ('course',)
    ordering = ('id',)

@admin.register(balance_topcoins_and_topgems)
class balance_topcoins_and_topgemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'topcoins', 'topgems', 'student')
    list_display_links = ('id', 'student')
    search_fields = ('topcoins', 'topgems', 'student')
    list_filter = ('topcoins', 'topgems', 'student')
    ordering = ('id',)

@admin.register(All_payment_of_education)
class All_payment_of_educationAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'amount', 'courses_of_Students', 'period_of_study', 'date')
    list_display_links = ('id', 'type', 'amount', 'courses_of_Students', 'period_of_study', 'date')
    search_fields = ('type', 'amount', 'courses_of_Students', 'period_of_study', 'date')
    list_filter = ('type', 'amount', 'courses_of_Students', 'period_of_study', 'date')
    ordering = ('id',)

@admin.register(Students_payment_account)
class Students_payment_accountAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'all_payment_of_education', 'date')
    list_display_links = ('id', 'student')
    search_fields = ('student', 'all_payment_of_education', 'date')
    list_filter = ('student', 'all_payment_of_education', 'date')
    ordering = ('id',)

@admin.register(image_student)
class image_studentAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'student')
    list_display_links = ('id', 'student')
    search_fields = ('student',)
    list_filter = ('student',)
    ordering = ('id',)

@admin.register(image_professor)
class image_professorAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'professor')
    list_display_links = ('id', 'professor')
    search_fields = ('professor',)
    list_filter = ('professor',)
    ordering = ('id',)

@admin.register(Add_HW_Professor_to_course)
class Add_HW_Professor_to_courseAdmin(admin.ModelAdmin):
    list_display = ('id', 'professor', 'course', 'file', 'comment', 'date_start', 'date_final')
    list_display_links = ('id', 'course', 'comment', 'date_start', 'date_final')
    search_fields = ('comment', 'course', 'date_start', 'date_final')
    list_filter = ('comment', 'course', 'date_start', 'date_final')
    ordering = ('id',)

# @admin.register(Information_about_HW_for_students)
# class Information_about_HW_for_studentsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'issued', 'professor', 'add_hw_professor')
#     list_display_links = ('id', 'professor', 'add_hw_professor')
#     search_fields = ('issued', 'professor', 'add_hw_professor')
#     list_filter = ('professor', 'add_hw_professor')
#     ordering = ('id',)