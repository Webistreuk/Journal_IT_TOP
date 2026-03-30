from django.contrib import admin
from .models import Autoriz, Professor, Student, Subjects, Courses_of_Students, balance_topcoins_and_topgems, All_payment_of_education, Students_payment_account

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
    list_display = ('id', 'topcoins', 'topgems')
    list_display_links = ('id',)
    search_fields = ('topcoins', 'topgems')
    list_filter = ('topcoins', 'topgems')
    ordering = ('id',)

@admin.register(All_payment_of_education)
class All_payment_of_educationAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'amount', 'courses_of_Students', 'period_of_study', 'month_of_payment', 'year_of_payment')
    list_display_links = ('id', 'type', 'amount', 'courses_of_Students', 'period_of_study', 'month_of_payment', 'year_of_payment')
    search_fields = ('type', 'amount', 'courses_of_Students', 'period_of_study', 'month_of_payment', 'year_of_payment')
    list_filter = ('type', 'amount', 'courses_of_Students', 'period_of_study', 'month_of_payment', 'year_of_payment')
    ordering = ('id',)

@admin.register(Students_payment_account)
class Students_payment_accountAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'all_payment_of_education', 'month_of_payment', 'year_of_payment')
    list_display_links = ('id', 'student')
    search_fields = ('student', 'all_payment_of_education', 'month_of_payment', 'year_of_payment')
    list_filter = ('student', 'all_payment_of_education', 'month_of_payment', 'year_of_payment')
    ordering = ('id',)