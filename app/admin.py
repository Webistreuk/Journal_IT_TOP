from django.contrib import admin
from .models import Autoriz, Professor, Student, Subjects, Courses_of_Students

# admin.site.register(Autoriz)
@admin.register(Autoriz)
class AutorizAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'email')
    list_filter = ('user',)
    ordering = ('id',)
    save_on_top = True

# admin.site.register(Professor)
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic', 'leads_the_subject')
    list_display_links = ('id', 'name', 'surname')
    search_fields = ('name', 'surname', 'patronymic', 'leads_the_subject')
    list_filter = ('name',)
    ordering = ('id',)
    save_on_top = True

# admin.site.register(Student)
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic')
    list_display_links = ('id', 'name', 'surname')
    search_fields = ('name', 'surname', 'patronymic')
    list_filter = ('name',)
    ordering = ('id',)
    save_on_top = True



# admin.site.register(Subjects)
@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_subject')
    list_display_links = ('id', 'name_subject')
    search_fields = ('name_subject',)
    list_filter = ('name_subject',)
    ordering = ('id',)
    save_on_top = True



# admin.site.register(Courses_of_Students)
@admin.register(Courses_of_Students)
class Courses_of_StudentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'course')
    list_display_links = ('id', 'course')
    search_fields = ('course',)
    list_filter = ('course',)
    ordering = ('id',)
    save_on_top = True