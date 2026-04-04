from django.contrib import admin
from .models import (
    Autoriz, Professor, Student, Subjects, Courses_of_Students, 
    balance_topcoins_and_topgems, All_payment_of_education, 
    Students_payment_account, image_student, image_professor, 
    Add_HW_Professor_to_course, Review_of_the_Academy, 
    Appeals_to_the_educational_unit, Shop_add_products, 
    Topmoney_student, Complaint_to_the_CEO, Schedule,
    First_pair, Second_pair, Third_pair, Fourth_pair, 
    Fifth_pair, Sixth_pair, Seventh_pair,
    Mondays_schedule, Tuesdays_schedule, Wednesdays_schedule,
    Thursdays_schedule, Fridays_schedule, Saturdays_schedule, 
    Sundays_schedule
)

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
    search_fields = ('name', 'surname', 'patronymic', 'leads_the_subject__name_subject')
    list_filter = ('name',)
    ordering = ('id',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic', 'courses_of_students')
    list_display_links = ('id', 'name', 'surname')
    search_fields = ('name', 'surname', 'patronymic')
    list_filter = ('name', 'courses_of_students')
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
    search_fields = ('topcoins', 'topgems', 'student__name', 'student__surname')
    list_filter = ('topcoins', 'topgems')
    ordering = ('id',)

@admin.register(All_payment_of_education)
class All_payment_of_educationAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_payment', 'amount', 'courses_of_Students', 'period_of_study', 'date')
    list_display_links = ('id', 'type_payment')
    search_fields = ('type_payment', 'amount', 'courses_of_Students__course')
    list_filter = ('type_payment', 'courses_of_Students')
    ordering = ('id',)

@admin.register(Students_payment_account)
class Students_payment_accountAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'all_payment_of_education', 'date')
    list_display_links = ('id', 'student')
    search_fields = ('student__name', 'student__surname', 'all_payment_of_education__courses_of_Students__course')
    list_filter = ('all_payment_of_education',)
    ordering = ('id',)
    readonly_fields = ('date',)

@admin.register(image_student)
class image_studentAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'student')
    list_display_links = ('id', 'student')
    search_fields = ('student__name', 'student__surname')
    list_filter = ('student',)
    ordering = ('id',)

@admin.register(image_professor)
class image_professorAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'professor')
    list_display_links = ('id', 'professor')
    search_fields = ('professor__name', 'professor__surname')
    list_filter = ('professor',)
    ordering = ('id',)

@admin.register(Add_HW_Professor_to_course)
class Add_HW_Professor_to_courseAdmin(admin.ModelAdmin):
    list_display = ('id', 'professor', 'course', 'comment', 'date_start', 'date_final')
    list_display_links = ('id', 'course')
    search_fields = ('comment', 'course__course', 'professor__name')
    list_filter = ('course', 'date_start', 'date_final')
    ordering = ('-date_start',)

@admin.register(Review_of_the_Academy)
class Review_of_the_AcademyAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'confirmation_review', 'type_a_social_network')
    list_display_links = ('id', 'student')
    search_fields = ('student__name', 'student__surname', 'type_a_social_network')
    list_filter = ('type_a_social_network',)
    ordering = ('id',)

@admin.register(Appeals_to_the_educational_unit)
class Appeals_to_the_educational_unitAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'Select_the_signal_type', 'question')
    list_display_links = ('id', 'student')
    search_fields = ('student__name', 'student__surname', 'question', 'Select_the_signal_type')
    list_filter = ('Select_the_signal_type',)
    ordering = ('id',)

@admin.register(Shop_add_products)
class Shop_add_productsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_product', 'product_quantity', 'price_product_topcoins', 'price_product_topgems')
    list_display_links = ('id', 'name_product')
    search_fields = ('name_product',)
    list_filter = ('name_product',)
    ordering = ('id',)

@admin.register(Topmoney_student)
class Topmoney_studentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'topmoney', 'balance_student')
    list_display_links = ('id', 'student')
    search_fields = ('student__name', 'student__surname')
    list_filter = ('balance_student',)
    ordering = ('id',)
    readonly_fields = ('topmoney',)

@admin.register(Complaint_to_the_CEO)
class Complaint_to_the_CEOAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'claim', 'date')
    list_display_links = ('id', 'student')
    search_fields = ('student__name', 'student__surname', 'claim')
    list_filter = ('date',)
    ordering = ('-date',)
    readonly_fields = ('date',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'week_start_date', 'week_end_date', 'is_active', 'is_current_week', 'get_pairs_count')
    list_display_links = ('id', 'course')
    search_fields = ('course__course', 'note')
    list_filter = ('is_active', 'is_current_week', 'course')
    ordering = ('-week_start_date',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Расписание по дням', {
            'fields': ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
        }),
        ('Информация о расписании', {
            'fields': ('course', 'week_start_date', 'week_end_date', 'is_active', 'is_current_week', 'note')
        }),
        ('Метаданные', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    def get_pairs_count(self, obj):
        return obj.get_pairs_count()
    get_pairs_count.short_description = 'Количество пар'

@admin.register(First_pair)
class FirstPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_pair_time_display', 'professor_surname', 'professor_name', 'professor_patronymic', 'subject', 'classroom_name')
    list_display_links = ('id', 'professor_surname')
    search_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    list_filter = ('type_pair', 'professor', 'classroom')
    readonly_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    fields = ('type_pair', 'professor', 'classroom')
    
    def get_pair_time_display(self, obj):
        return obj.get_type_pair_display()
    get_pair_time_display.short_description = 'Время пары'

@admin.register(Second_pair)
class SecondPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_pair_time_display', 'professor_surname', 'professor_name', 'professor_patronymic', 'subject', 'classroom_name')
    list_display_links = ('id', 'professor_surname')
    search_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    list_filter = ('type_pair', 'professor', 'classroom')
    readonly_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    fields = ('type_pair', 'professor', 'classroom')
    
    def get_pair_time_display(self, obj):
        return obj.get_type_pair_display()
    get_pair_time_display.short_description = 'Время пары'

@admin.register(Third_pair)
class ThirdPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_pair_time_display', 'professor_surname', 'professor_name', 'professor_patronymic', 'subject', 'classroom_name')
    list_display_links = ('id', 'professor_surname')
    search_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    list_filter = ('type_pair', 'professor', 'classroom')
    readonly_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    fields = ('type_pair', 'professor', 'classroom')
    
    def get_pair_time_display(self, obj):
        return obj.get_type_pair_display()
    get_pair_time_display.short_description = 'Время пары'

@admin.register(Fourth_pair)
class FourthPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_pair_time_display', 'professor_surname', 'professor_name', 'professor_patronymic', 'subject', 'classroom_name')
    list_display_links = ('id', 'professor_surname')
    search_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    list_filter = ('type_pair', 'professor', 'classroom')
    readonly_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    fields = ('type_pair', 'professor', 'classroom')
    
    def get_pair_time_display(self, obj):
        return obj.get_type_pair_display()
    get_pair_time_display.short_description = 'Время пары'

@admin.register(Fifth_pair)
class FifthPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_pair_time_display', 'professor_surname', 'professor_name', 'professor_patronymic', 'subject', 'classroom_name')
    list_display_links = ('id', 'professor_surname')
    search_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    list_filter = ('type_pair', 'professor', 'classroom')
    readonly_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    fields = ('type_pair', 'professor', 'classroom')
    
    def get_pair_time_display(self, obj):
        return obj.get_type_pair_display()
    get_pair_time_display.short_description = 'Время пары'

@admin.register(Sixth_pair)
class SixthPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_pair_time_display', 'professor_surname', 'professor_name', 'professor_patronymic', 'subject', 'classroom_name')
    list_display_links = ('id', 'professor_surname')
    search_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    list_filter = ('type_pair', 'professor', 'classroom')
    readonly_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    fields = ('type_pair', 'professor', 'classroom')
    
    def get_pair_time_display(self, obj):
        return obj.get_type_pair_display()
    get_pair_time_display.short_description = 'Время пары'

@admin.register(Seventh_pair)
class SeventhPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_pair_time_display', 'professor_surname', 'professor_name', 'professor_patronymic', 'subject', 'classroom_name')
    list_display_links = ('id', 'professor_surname')
    search_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    list_filter = ('type_pair', 'professor', 'classroom')
    readonly_fields = ('professor_name', 'professor_surname', 'professor_patronymic', 'subject', 'classroom_name')
    fields = ('type_pair', 'professor', 'classroom')
    
    def get_pair_time_display(self, obj):
        return obj.get_type_pair_display()
    get_pair_time_display.short_description = 'Время пары'

@admin.register(Mondays_schedule)
class MondaysScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    list_display_links = ('id',)
    search_fields = ('first_pair__professor_surname', 'second_pair__professor_surname', 'third_pair__professor_surname')
    list_filter = ('first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    ordering = ('id',)

@admin.register(Tuesdays_schedule)
class TuesdaysScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    list_display_links = ('id',)
    search_fields = ('first_pair__professor_surname', 'second_pair__professor_surname', 'third_pair__professor_surname')
    list_filter = ('first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    ordering = ('id',)

@admin.register(Wednesdays_schedule)
class WednesdaysScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    list_display_links = ('id',)
    search_fields = ('first_pair__professor_surname', 'second_pair__professor_surname', 'third_pair__professor_surname')
    list_filter = ('first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    ordering = ('id',)

@admin.register(Thursdays_schedule)
class ThursdaysScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    list_display_links = ('id',)
    search_fields = ('first_pair__professor_surname', 'second_pair__professor_surname', 'third_pair__professor_surname')
    list_filter = ('first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    ordering = ('id',)

@admin.register(Fridays_schedule)
class FridaysScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    list_display_links = ('id',)
    search_fields = ('first_pair__professor_surname', 'second_pair__professor_surname', 'third_pair__professor_surname')
    list_filter = ('first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    ordering = ('id',)

@admin.register(Saturdays_schedule)
class SaturdaysScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    list_display_links = ('id',)
    search_fields = ('first_pair__professor_surname', 'second_pair__professor_surname', 'third_pair__professor_surname')
    list_filter = ('first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    ordering = ('id',)

@admin.register(Sundays_schedule)
class SundaysScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    list_display_links = ('id',)
    search_fields = ('first_pair__professor_surname', 'second_pair__professor_surname', 'third_pair__professor_surname')
    list_filter = ('first_pair', 'second_pair', 'third_pair', 'fourth_pair', 'fifth_pair', 'sixth_pair', 'seventh_pair')
    ordering = ('id',)