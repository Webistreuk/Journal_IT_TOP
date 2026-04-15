from .models import Autoriz, Student, Professor, AcademicStaff, Group, Subjects, Add_HW_Professor_to_course, HomeworkSubmission, Attendance, Estimation, Shop_add_products, PaymentInfo, Announcement, Event, Poll, PollOption, Message, Schedule, DailySchedule, Pair, LessonType, Add_Сlassroom, Semester, Vacation, ScheduleReplacement, Review_of_the_Academy, Appeals_to_the_educational_unit, Complaint_to_the_CEO, Student_Reviews, EducationalMaterial, PersonalAccount, Exam, ExamSession, ScheduledExam, LeaderboardEntry, Ranking, StudentStats, Reward, UserReward, AcademicDebt, GraduationWork, Internship, Topmoney_student, balance_topcoins_and_topgems, Type_work, Course, Direction, AcademicYear, Chat, PollVote, Notification, ScheduleReplacement, image_student, image_professor, Students_payment_account, All_payment_of_education, Debtor, Scholarship
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class AutorizForm(forms.ModelForm):
    user = forms.CharField(widget=forms.TextInput(attrs={'class': 'username_field', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'userpassword_field', 'placeholder': 'Пароль'}))

    class Meta:
        model = Autoriz
        fields = ['user', 'password']

class AutorizForm_remove_password(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'useremail_field', 'placeholder': 'E-mail'}))

    class Meta:
        model = Autoriz
        fields = ['email']

class AutorizRegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))
    
    class Meta:
        model = Autoriz
        fields = ['user', 'email', 'password']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'patronymic', 'group']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }

class ProfessorProfileForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['name', 'surname', 'patronymic', 'leads_the_subject']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
            'leads_the_subject': forms.Select(attrs={'class': 'form-control'}),
        }

class AcademicStaffProfileForm(forms.ModelForm):
    class Meta:
        model = AcademicStaff
        fields = ['name', 'surname', 'patronymic', 'position']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Должность'}),
        }

class HomeworkAddForm(forms.ModelForm):
    class Meta:
        model = Add_HW_Professor_to_course
        fields = ['group', 'subject', 'file', 'comment', 'date_final']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Комментарий'}),
            'date_final': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class HomeworkSubmitForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['file', 'comment', 'time_work', 'the_usefulness_of_knowledge']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Комментарий'}),
            'time_work': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Время выполнения (минуты)'}),
            'the_usefulness_of_knowledge': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Оценка полезности от 1 до 5'}),
        }

class HomeworkGradeForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['grade', 'professor_comment', 'is_checked']
        widgets = {
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Оценка'}),
            'professor_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Комментарий преподавателя'}),
            'is_checked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['type', 'student', 'schedule', 'pair']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'schedule': forms.Select(attrs={'class': 'form-control'}),
            'pair': forms.Select(attrs={'class': 'form-control'}),
        }

class EstimationForm(forms.ModelForm):
    class Meta:
        model = Estimation
        fields = ['student', 'subject', 'type_estimation']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'type_estimation': forms.Select(attrs={'class': 'form-control'}),
        }

class ShopProductForm(forms.ModelForm):
    class Meta:
        model = Shop_add_products
        fields = ['name_product', 'photo_product', 'product_quantity', 'price_product_topcoins', 'price_product_topgems']
        widgets = {
            'name_product': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название товара'}),
            'photo_product': forms.FileInput(attrs={'class': 'form-control'}),
            'product_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество'}),
            'price_product_topcoins': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена в топкоинах'}),
            'price_product_topgems': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена в топгемах'}),
        }

class PaymentInfoForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields = ['payment_account', 'paid_by', 'amount_paid', 'payment_date', 'period_start', 'period_end', 'part_number', 'total_parts', 'due_date', 'comment']
        widgets = {
            'payment_account': forms.Select(attrs={'class': 'form-control'}),
            'paid_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Кто оплатил'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сумма'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'part_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Номер части'}),
            'total_parts': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Всего частей'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Комментарий'}),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'photo', 'description', 'groups', 'is_for_all']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Описание'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_for_all': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'start_date', 'end_date', 'description', 'location', 'groups', 'is_for_all']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Место'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_for_all': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description', 'start_date', 'end_date', 'groups']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class PollOptionForm(forms.ModelForm):
    class Meta:
        model = PollOption
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вариант ответа'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'file']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Сообщение'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['group', 'semester', 'week_start_date', 'note']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'week_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Примечание'}),
        }

class DailyScheduleForm(forms.ModelForm):
    class Meta:
        model = DailySchedule
        fields = ['weekday', 'pair_order', 'group', 'pair']
        widgets = {
            'weekday': forms.Select(attrs={'class': 'form-control'}),
            'pair_order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Порядковый номер'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'pair': forms.Select(attrs={'class': 'form-control'}),
        }

class PairForm(forms.ModelForm):
    class Meta:
        model = Pair
        fields = ['pair_number', 'professor', 'subject', 'classroom', 'lesson_type']
        widgets = {
            'pair_number': forms.Select(attrs={'class': 'form-control'}),
            'professor': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'classroom': forms.Select(attrs={'class': 'form-control'}),
            'lesson_type': forms.Select(attrs={'class': 'form-control'}),
        }

class LessonTypeForm(forms.ModelForm):
    class Meta:
        model = LessonType
        fields = ['type', 'name']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
        }

class AddClassroomForm(forms.ModelForm):
    class Meta:
        model = Add_Сlassroom
        fields = ['name_classroom']
        widgets = {
            'name_classroom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название аудитории'}),
        }

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name', 'semester_type', 'academic_year', 'start_date', 'end_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'semester_type': forms.Select(attrs={'class': 'form-control'}),
            'academic_year': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = ['vacation_type', 'start_date', 'end_date', 'academic_year', 'semester', 'description', 'is_active']
        widgets = {
            'vacation_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'academic_year': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Описание'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ScheduleReplacementForm(forms.ModelForm):
    class Meta:
        model = ScheduleReplacement
        fields = ['schedule', 'original_date', 'new_date', 'original_pair', 'new_pair', 'reason']
        widgets = {
            'schedule': forms.Select(attrs={'class': 'form-control'}),
            'original_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'new_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'original_pair': forms.Select(attrs={'class': 'form-control'}),
            'new_pair': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Причина замены'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review_of_the_Academy
        fields = ['confirmation_review', 'type_a_social_network']
        widgets = {
            'confirmation_review': forms.FileInput(attrs={'class': 'form-control'}),
            'type_a_social_network': forms.Select(attrs={'class': 'form-control'}),
        }

class AppealForm(forms.ModelForm):
    class Meta:
        model = Appeals_to_the_educational_unit
        fields = ['Select_the_signal_type', 'question']
        widgets = {
            'Select_the_signal_type': forms.Select(attrs={'class': 'form-control'}),
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваш вопрос'}),
        }

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint_to_the_CEO
        fields = ['claim']
        widgets = {
            'claim': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Текст жалобы'}),
        }

class StudentReviewForm(forms.ModelForm):
    class Meta:
        model = Student_Reviews
        fields = ['student', 'professor', 'subject', 'comment']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'professor': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Отзыв о студенте'}),
        }

class EducationalMaterialForm(forms.ModelForm):
    class Meta:
        model = EducationalMaterial
        fields = ['title', 'file', 'description', 'groups', 'is_public', 'subject']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }

class PersonalAccountForm(forms.ModelForm):
    class Meta:
        model = PersonalAccount
        fields = ['role', 'student_profile', 'professor_profile', 'academic_staff_profile', 'school_certificate', 'health_certificate', 'diploma', 'employment_contract', 'internal_documents', 'additional_docs']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'student_profile': forms.Select(attrs={'class': 'form-control'}),
            'professor_profile': forms.Select(attrs={'class': 'form-control'}),
            'academic_staff_profile': forms.Select(attrs={'class': 'form-control'}),
            'school_certificate': forms.FileInput(attrs={'class': 'form-control'}),
            'health_certificate': forms.FileInput(attrs={'class': 'form-control'}),
            'diploma': forms.FileInput(attrs={'class': 'form-control'}),
            'employment_contract': forms.FileInput(attrs={'class': 'form-control'}),
            'internal_documents': forms.FileInput(attrs={'class': 'form-control'}),
            'additional_docs': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['student', 'subject', 'grade', 'professor', 'exam_date', 'semester']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'professor': forms.Select(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }

class ExamSessionForm(forms.ModelForm):
    class Meta:
        model = ExamSession
        fields = ['semester', 'name', 'start_date', 'end_date', 'is_active']
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название сессии'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ScheduledExamForm(forms.ModelForm):
    class Meta:
        model = ScheduledExam
        fields = ['exam_name', 'subject', 'preliminary_date', 'group', 'exam_session']
        widgets = {
            'exam_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название экзамена'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'preliminary_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'exam_session': forms.Select(attrs={'class': 'form-control'}),
        }

class AcademicDebtForm(forms.ModelForm):
    class Meta:
        model = AcademicDebt
        fields = ['student', 'subject', 'semester', 'exam_date', 'is_passed', 'retake_count', 'commission_date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_passed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'retake_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество пересдач'}),
            'commission_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class GraduationWorkForm(forms.ModelForm):
    class Meta:
        model = GraduationWork
        fields = ['student', 'title', 'supervisor', 'reviewer', 'defense_date', 'grade', 'file']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема работы'}),
            'supervisor': forms.Select(attrs={'class': 'form-control'}),
            'reviewer': forms.Select(attrs={'class': 'form-control'}),
            'defense_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Оценка'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['student', 'internship_type', 'organization', 'start_date', 'end_date', 'supervisor', 'report_file', 'grade']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'internship_type': forms.Select(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Организация'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'supervisor': forms.Select(attrs={'class': 'form-control'}),
            'report_file': forms.FileInput(attrs={'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Оценка'}),
        }

class AllPaymentOfEducationForm(forms.ModelForm):
    class Meta:
        model = All_payment_of_education
        fields = ['type_payment', 'amount', 'group', 'period_of_study', 'date']
        widgets = {
            'type_payment': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Стоимость'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'period_of_study': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Период обучения в месяцах'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class StudentsPaymentAccountForm(forms.ModelForm):
    class Meta:
        model = Students_payment_account
        fields = ['student', 'all_payment_of_education']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'all_payment_of_education': forms.Select(attrs={'class': 'form-control'}),
        }

class ImageStudentForm(forms.ModelForm):
    class Meta:
        model = image_student
        fields = ['photo', 'student']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
        }

class ImageProfessorForm(forms.ModelForm):
    class Meta:
        model = image_professor
        fields = ['photo', 'professor']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'professor': forms.Select(attrs={'class': 'form-control'}),
        }

class TypeWorkForm(forms.ModelForm):
    class Meta:
        model = Type_work
        fields = ['type']
        widgets = {'type': forms.Select(attrs={'class': 'form-control'})}

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['number']
        widgets = {'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Номер курса'})}

class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название направления'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Код направления'}),
        }

class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['name', 'start_date', 'end_date', 'is_current']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2024-2025'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'course', 'direction', 'academic_year']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название группы'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'academic_year': forms.Select(attrs={'class': 'form-control'}),
        }

class SubjectsForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = ['name_subject']
        widgets = {'name_subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название предмета'})}

class BalanceForm(forms.ModelForm):
    class Meta:
        model = balance_topcoins_and_topgems
        fields = ['topcoins', 'topgems', 'student']
        widgets = {
            'topcoins': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Топкоины'}),
            'topgems': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Топгемы'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
        }

class TopmoneyStudentForm(forms.ModelForm):
    class Meta:
        model = Topmoney_student
        fields = ['student', 'balance_student']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'balance_student': forms.Select(attrs={'class': 'form-control'}),
        }

class LeaderboardEntryForm(forms.ModelForm):
    class Meta:
        model = LeaderboardEntry
        fields = ['student', 'topmoney', 'group', 'semester', 'rank_in_group', 'rank_in_course']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'topmoney': forms.NumberInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'rank_in_group': forms.NumberInput(attrs={'class': 'form-control'}),
            'rank_in_course': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class RankingForm(forms.ModelForm):
    class Meta:
        model = Ranking
        fields = ['student', 'semester', 'group_rank', 'course_rank', 'average_grade']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'group_rank': forms.NumberInput(attrs={'class': 'form-control'}),
            'course_rank': forms.NumberInput(attrs={'class': 'form-control'}),
            'average_grade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class StudentStatsForm(forms.ModelForm):
    class Meta:
        model = StudentStats
        fields = ['student', 'total_attendance_days', 'consecutive_days_attended', 'consecutive_days_on_time']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'total_attendance_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'consecutive_days_attended': forms.NumberInput(attrs={'class': 'form-control'}),
            'consecutive_days_on_time': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'description', 'reward_type', 'topcoins_award', 'topgems_award', 'condition_attendance_streak', 'condition_on_time_streak', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название награды'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание'}),
            'reward_type': forms.Select(attrs={'class': 'form-control'}),
            'topcoins_award': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Топкоины'}),
            'topgems_award': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Топгемы'}),
            'condition_attendance_streak': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Дней посещения'}),
            'condition_on_time_streak': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Дней без опозданий'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserRewardForm(forms.ModelForm):
    class Meta:
        model = UserReward
        fields = ['student', 'reward', 'topcoins_given', 'topgems_given']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'reward': forms.Select(attrs={'class': 'form-control'}),
            'topcoins_given': forms.NumberInput(attrs={'class': 'form-control'}),
            'topgems_given': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'message', 'notification_type', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Сообщение'}),
            'notification_type': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }

class PollVoteForm(forms.ModelForm):
    class Meta:
        model = PollVote
        fields = ['poll', 'option', 'user']
        widgets = {
            'poll': forms.Select(attrs={'class': 'form-control'}),
            'option': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['participants']
        widgets = {'participants': forms.SelectMultiple(attrs={'class': 'form-control'})}

class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = ['student', 'payment_info', 'debt_amount', 'due_date', 'is_paid', 'notification_sent']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'payment_info': forms.Select(attrs={'class': 'form-control'}),
            'debt_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notification_sent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['student', 'amount', 'month', 'is_paid', 'paid_date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'month': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'paid_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }