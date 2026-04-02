from django.contrib import admin
from .models import Autoriz, Professor, Student, Subjects, Courses_of_Students, balance_topcoins_and_topgems, All_payment_of_education, Students_payment_account, image_student, image_professor, Add_HW_Professor_to_course, Review_of_the_Academy, Appeals_to_the_educational_unit

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
    list_display = ('id', 'type_payment', 'amount', 'courses_of_Students', 'period_of_study', 'date')
    list_display_links = ('id', 'type_payment', 'amount', 'courses_of_Students', 'period_of_study', 'date')
    search_fields = ('type_payment', 'amount', 'courses_of_Students', 'period_of_study', 'date')
    list_filter = ('type_payment', 'amount', 'courses_of_Students', 'period_of_study', 'date')
    ordering = ('id',)

@admin.register(Students_payment_account)
class Students_payment_accountAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'all_payment_of_education', 'date')
    list_display_links = ('id', 'student')
    search_fields = ('student', 'all_payment_of_education', 'date')
    list_filter = ('student', 'all_payment_of_education', 'date')
    ordering = ('id',)
    readonly_fields = ('date',)

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

# @admin.register(Inform'ation_about_HW_for_students)
# class Information_about_HW_for_studentsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'issued', 'professor', 'add_hw_professor')
#     list_display_links = ('id', 'professor', 'add_hw_professor')
#     search_fields = ('issued', 'professor', 'add_hw_professor')
#     list_filter = ('professor', 'add_hw_professor')
#     ordering = ('id,)

@admin.register(Review_of_the_Academy)
class Review_of_the_AcademyAdmin(admin.ModelAdmin):
    list_display = ('id', 'student','confirmation_review', 'type_a_social_network')
    list_display_links = ('id', 'student', 'confirmation_review', 'type_a_social_network')
    search_fields = ('student', 'confirmation_review', 'type_a_social_network')
    list_filter = ('student', 'confirmation_review', 'type_a_social_network')
    ordering = ('id',)

@admin.register(Appeals_to_the_educational_unit)
class Appeals_to_the_educational_unitAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'question', 'Select_the_signal_type')
    list_display_links = ('id', 'student', 'question', 'Select_the_signal_type')
    search_fields = ('student', 'question', 'Select_the_signal_type')
    list_filter = ('student', 'question', 'Select_the_signal_type')
    ordering = ('id',)