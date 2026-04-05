from django.contrib import admin
from .models import (
    Autoriz, Professor, Student, Subjects, Group, Course, Direction, AcademicYear,
    balance_topcoins_and_topgems, All_payment_of_education, 
    Students_payment_account, image_student, image_professor, 
    Add_HW_Professor_to_course, Review_of_the_Academy, 
    Appeals_to_the_educational_unit, Shop_add_products, 
    Topmoney_student, Complaint_to_the_CEO, Schedule, Estimation,
    Semester, Vacation, LessonType, Pair, DailySchedule,
    ScheduleReplacement, Attendance, Exam, ExamSession, ScheduledExam, Announcement,
    LeaderboardEntry, StudentStats, Reward, UserReward,
    PaymentInfo, Ranking, EducationalMaterial, PersonalAccount,
    Debtor, Scholarship, AcademicDebt, GraduationWork, Internship,
    Event, Notification, Poll, PollOption, PollVote, Chat, Message
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
    list_display = ('id', 'name', 'surname', 'patronymic', 'group')
    list_display_links = ('id', 'name', 'surname')
    search_fields = ('name', 'surname', 'patronymic')
    list_filter = ('name', 'group')
    ordering = ('id',)

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_subject')
    list_display_links = ('id', 'name_subject')
    search_fields = ('name_subject',)
    list_filter = ('name_subject',)
    ordering = ('id',)

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    list_display_links = ('id', 'code')
    search_fields = ('code', 'name')
    ordering = ('code',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'number')
    list_display_links = ('id', 'number')
    ordering = ('number',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course', 'direction', 'academic_year')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('course', 'direction', 'academic_year')
    ordering = ('course', 'direction', 'name')

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'is_current')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('is_current',)
    ordering = ('-start_date',)
    list_editable = ('is_current',)

@admin.register(balance_topcoins_and_topgems)
class balance_topcoins_and_topgemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'topcoins', 'topgems', 'student')
    list_display_links = ('id', 'student')
    search_fields = ('topcoins', 'topgems', 'student__name', 'student__surname')
    list_filter = ('topcoins', 'topgems')
    ordering = ('id',)

@admin.register(All_payment_of_education)
class All_payment_of_educationAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_payment', 'amount', 'group', 'period_of_study', 'date')
    list_display_links = ('id', 'type_payment')
    search_fields = ('type_payment', 'amount', 'group__name')
    list_filter = ('type_payment', 'group')
    ordering = ('id',)

@admin.register(Students_payment_account)
class Students_payment_accountAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'all_payment_of_education', 'date')
    list_display_links = ('id', 'student')
    search_fields = ('student__name', 'student__surname', 'all_payment_of_education__group__name')
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
    list_display = ('id', 'professor', 'group', 'subject', 'comment', 'date_start', 'date_final')
    list_display_links = ('id', 'group')
    search_fields = ('comment', 'group__name', 'professor__name', 'subject__name_subject')
    list_filter = ('group', 'subject', 'date_start', 'date_final')
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

@admin.register(Estimation)
class EstimationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'type_estimation', 'date')
    list_display_links = ('id', 'student')
    search_fields = ('student__name', 'student__surname', 'subject__name_subject')
    list_filter = ('type_estimation', 'date')
    ordering = ('-date',)

@admin.register(LessonType)
class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('type',)
    ordering = ('name',)

@admin.register(Pair)
class PairAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_pair_number_display', 'subject', 'professor', 'classroom', 'lesson_type')
    list_display_links = ('id',)
    search_fields = ('subject__name_subject', 'professor__surname')
    list_filter = ('pair_number', 'lesson_type', 'classroom')
    ordering = ('pair_number',)

@admin.register(DailySchedule)
class DailyScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_weekday_display', 'pair_order', 'group', 'pair')
    list_display_links = ('id',)
    search_fields = ('group__name',)
    list_filter = ('weekday', 'group')
    ordering = ('weekday', 'pair_order')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_semester_type_display', 'academic_year', 'start_date', 'end_date', 'is_active')
    list_display_links = ('id',)
    search_fields = ('academic_year__name',)
    list_filter = ('semester_type', 'academic_year', 'is_active')
    ordering = ('-start_date',)
    list_editable = ('is_active',)

@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_vacation_type_display', 'academic_year', 'start_date', 'end_date', 'semester', 'is_active')
    list_display_links = ('id',)
    search_fields = ('academic_year__name', 'description')
    list_filter = ('vacation_type', 'academic_year', 'is_active', 'semester')
    ordering = ('-start_date',)
    list_editable = ('is_active',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'semester', 'week_start_date', 'week_end_date', 'is_active', 'is_current_week')
    list_display_links = ('id', 'group')
    search_fields = ('group__name', 'note', 'semester__academic_year__name')
    list_filter = ('is_active', 'is_current_week', 'group', 'semester')
    ordering = ('-week_start_date',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ScheduleReplacement)
class ScheduleReplacementAdmin(admin.ModelAdmin):
    list_display = ('id', 'schedule', 'original_date', 'new_date', 'reason', 'created_by')
    list_display_links = ('id',)
    search_fields = ('reason',)
    list_filter = ('original_date', 'new_date')
    ordering = ('-created_at',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'type', 'data_created', 'schedule', 'pair')
    list_display_links = ('id', 'student')
    search_fields = ('student__name', 'student__surname')
    list_filter = ('type', 'data_created')
    ordering = ('-data_created',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'grade', 'professor', 'exam_date', 'semester')
    list_filter = ('grade', 'exam_date', 'subject', 'semester')
    search_fields = ('student__surname', 'subject__name_subject', 'professor__surname')
    ordering = ('-exam_date',)

@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'semester', 'start_date', 'end_date', 'is_active')
    list_filter = ('semester', 'is_active')
    search_fields = ('name',)
    ordering = ('-start_date',)
    list_editable = ('is_active',)

@admin.register(ScheduledExam)
class ScheduledExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam_name', 'subject', 'preliminary_date', 'group', 'exam_session', 'created_by')
    list_filter = ('preliminary_date', 'group', 'exam_session')
    search_fields = ('exam_name', 'subject__name_subject')
    ordering = ('-preliminary_date',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_added', 'is_active', 'is_for_all')
    list_filter = ('date_added', 'is_active', 'is_for_all')
    search_fields = ('title', 'description')
    ordering = ('-date_added',)
    list_editable = ('is_active',)
    filter_horizontal = ('groups',)

@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'topmoney', 'group', 'semester', 'rank_in_group', 'rank_in_course', 'date')
    list_filter = ('group', 'semester', 'date')
    search_fields = ('student__surname', 'group__name')
    ordering = ('-date', 'rank_in_group')
    readonly_fields = ('topmoney', 'rank_in_group', 'rank_in_course', 'date')

@admin.register(StudentStats)
class StudentStatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'total_attendance_days', 'consecutive_days_attended', 'consecutive_days_on_time')
    list_filter = ('student',)
    search_fields = ('student__surname',)
    readonly_fields = ('total_attendance_days', 'consecutive_days_attended', 'consecutive_days_on_time', 'last_attendance_date', 'topcoins_awarded_total', 'topgems_awarded_total')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'reward_type', 'topcoins_award', 'topgems_award', 'is_active')
    list_filter = ('reward_type', 'is_active')
    search_fields = ('name',)

@admin.register(UserReward)
class UserRewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'reward', 'awarded_at', 'topcoins_given', 'topgems_given')
    list_filter = ('awarded_at',)
    search_fields = ('student__surname', 'reward__name')
    readonly_fields = ('awarded_at',)

@admin.register(PaymentInfo)
class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'payment_account', 'amount_paid', 'payment_date', 'period_start', 'period_end', 'part_number', 'due_date')
    list_filter = ('payment_date', 'due_date')
    search_fields = ('student__surname', 'paid_by')
    ordering = ('-payment_date',)

@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'semester', 'group_rank', 'course_rank', 'average_grade', 'date')
    list_filter = ('semester', 'date')
    search_fields = ('student__surname',)
    ordering = ('-date', 'group_rank')
    readonly_fields = ('date',)

@admin.register(EducationalMaterial)
class EducationalMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'professor', 'upload_date', 'is_public', 'subject')
    list_filter = ('upload_date', 'is_public', 'subject')
    search_fields = ('title', 'professor__surname')
    filter_horizontal = ('groups',)

@admin.register(PersonalAccount)
class PersonalAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'student_profile', 'professor_profile')
    list_filter = ('role',)
    search_fields = ('user__user', 'student_profile__surname', 'professor_profile__surname')
    fieldsets = (
        ('Основное', {
            'fields': ('user', 'role', 'student_profile', 'professor_profile')
        }),
        ('Документы студента', {
            'fields': ('school_certificate', 'health_certificate')
        }),
        ('Документы преподавателя', {
            'fields': ('diploma', 'employment_contract')
        }),
        ('Документы учебной части', {
            'fields': ('internal_documents',)
        }),
        ('Общие', {
            'fields': ('additional_docs',)
        }),
    )

@admin.register(Debtor)
class DebtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'debt_amount', 'due_date', 'is_paid', 'notification_sent')
    list_filter = ('is_paid', 'notification_sent', 'due_date')
    search_fields = ('student__surname',)
    ordering = ('due_date',)
    list_editable = ('is_paid', 'notification_sent')

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'amount', 'month', 'is_paid')
    list_filter = ('is_paid', 'month')
    search_fields = ('student__surname',)
    ordering = ('-month',)
    list_editable = ('is_paid',)

@admin.register(AcademicDebt)
class AcademicDebtAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'semester', 'exam_date', 'is_passed', 'retake_count')
    list_filter = ('is_passed', 'semester', 'exam_date')
    search_fields = ('student__surname', 'subject__name_subject')
    ordering = ('exam_date',)
    list_editable = ('is_passed',)

@admin.register(GraduationWork)
class GraduationWorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'title', 'supervisor', 'defense_date', 'grade')
    list_filter = ('defense_date', 'grade')
    search_fields = ('student__surname', 'title', 'supervisor__surname')
    ordering = ('-defense_date',)

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'internship_type', 'organization', 'start_date', 'end_date', 'grade')
    list_filter = ('internship_type', 'start_date', 'end_date')
    search_fields = ('student__surname', 'organization')
    ordering = ('-start_date',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'event_type', 'start_date', 'end_date', 'location', 'is_for_all')
    list_filter = ('event_type', 'start_date', 'is_for_all')
    search_fields = ('title', 'description', 'location')
    ordering = ('start_date',)
    filter_horizontal = ('groups',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'notification_type', 'created_at', 'is_read')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__user')
    ordering = ('-created_at',)
    list_editable = ('is_read',)

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    ordering = ('-start_date',)
    filter_horizontal = ('groups',)

@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'poll', 'text', 'votes')
    list_filter = ('poll',)
    search_fields = ('text',)
    ordering = ('poll',)

@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'poll', 'option', 'user', 'voted_at')
    list_filter = ('voted_at',)
    search_fields = ('user__user',)
    ordering = ('-voted_at',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    filter_horizontal = ('participants',)
    ordering = ('-updated_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('text', 'sender__user')
    ordering = ('-created_at',)
    list_editable = ('is_read',)