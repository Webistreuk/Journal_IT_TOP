from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from datetime import datetime, timedelta, date
from django.db.models import Count, Sum, Q
from django.utils import timezone
from .models import Autoriz, Subjects, Student, Professor, AcademicStaff, Group, Add_HW_Professor_to_course, HomeworkSubmission, Attendance, Estimation, balance_topcoins_and_topgems, Shop_add_products, PaymentInfo, Announcement, Event, Poll, PollOption, PollVote, Chat, Message, Schedule, DailySchedule, Pair, LessonType, Add_Сlassroom, Semester, Vacation, ScheduleReplacement, LeaderboardEntry, Ranking, StudentStats, Reward, UserReward, AcademicDebt, GraduationWork, Internship, EducationalMaterial, PersonalAccount, Review_of_the_Academy, Appeals_to_the_educational_unit, Complaint_to_the_CEO, Student_Reviews, Exam, ExamSession, ScheduledExam, Topmoney_student, Type_work, Course, Direction, AcademicYear, image_student, image_professor, Students_payment_account, All_payment_of_education, Notification, Debtor, Scholarship, ChatProfile, Story
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json
import pytz
import os

def update_student_rankings(student):
    if not student or not student.group:
        return
    
    semester = Semester.objects.filter(is_active=True).first()
    if not semester:
        semester = Semester.objects.first()
    if not semester:
        return
    
    group = student.group
    course = group.course
    
    group_students = list(Student.objects.filter(group=group))
    course_students = list(Student.objects.filter(group__course=course))
    
    for s in group_students:
        topmoney_obj = Topmoney_student.objects.filter(student=s).first()
        topmoney = topmoney_obj.topmoney if topmoney_obj else 0
        
        group_rank = 1
        for other in group_students:
            if other.id != s.id:
                other_tm = Topmoney_student.objects.filter(student=other).first()
                other_topmoney = other_tm.topmoney if other_tm else 0
                if other_topmoney > topmoney:
                    group_rank += 1
        
        course_rank = 1
        for other in course_students:
            if other.id != s.id:
                other_tm = Topmoney_student.objects.filter(student=other).first()
                other_topmoney = other_tm.topmoney if other_tm else 0
                if other_topmoney > topmoney:
                    course_rank += 1
        
        Ranking.objects.update_or_create(
            student=s,
            semester=semester,
            defaults={
                'group_rank': group_rank,
                'course_rank': course_rank,
                'average_grade': None
            }
        )

def update_topmoney_for_student(student):
    balance = balance_topcoins_and_topgems.objects.filter(student=student).first()
    if balance:
        topmoney, created = Topmoney_student.objects.get_or_create(
            student=student,
            defaults={'balance_student': balance}
        )
        topmoney.balance_student = balance
        topmoney.save()
        update_student_rankings(student)

def get_user_context(request):
    context = {}
    if 'user_id' in request.session:
        try:
            user = Autoriz.objects.get(id=request.session['user_id'])
            context['user'] = user
            
            try:
                chat_profile = ChatProfile.objects.get(user=user)
                if chat_profile.avatar and chat_profile.avatar.url:
                    context['user_avatar'] = chat_profile.avatar.url
            except ChatProfile.DoesNotExist:
                pass
            
            try:
                student = Student.objects.get(autoriz=user)
                context['user_role'] = 'student'
                if student.group:
                    context['student_info'] = {
                        'course': student.group.course.number,
                        'direction': student.group.direction.name,
                        'group': student.group.name
                    }
                else:
                    context['student_info'] = {
                        'course': '-',
                        'direction': '-',
                        'group': '-'
                    }
                
                balance_obj = balance_topcoins_and_topgems.objects.filter(student=student).first()
                if balance_obj:
                    context['topcoins'] = balance_obj.topcoins
                    context['topgems'] = balance_obj.topgems
                else:
                    context['topcoins'] = 0
                    context['topgems'] = 0
                    
            except Student.DoesNotExist:
                try:
                    professor = Professor.objects.get(autoriz=user)
                    context['user_role'] = 'professor'
                    context['professor_info'] = {
                        'subject': professor.leads_the_subject.name_subject if professor.leads_the_subject else '-'
                    }
                except Professor.DoesNotExist:
                    try:
                        staff = AcademicStaff.objects.get(autoriz=user)
                        context['user_role'] = 'academic_staff'
                        context['staff_info'] = {
                            'position': staff.position
                        }
                    except AcademicStaff.DoesNotExist:
                        context['user_role'] = 'unknown'
        except Autoriz.DoesNotExist:
            pass
    return context

def autoriz_view(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        if not username or not password:
            return render(request, 'Authorize.html', {'error': 'Заполните все поля!'})
        try:
            user = Autoriz.objects.get(user=username)
            if user.password == password:
                request.session['user_id'] = user.id
                return redirect('main_view')
            else:
                return render(request, 'Authorize.html', {'error': 'Неправильный пароль!'})
        except Autoriz.DoesNotExist:
            return render(request, 'Authorize.html', {'error': 'Пользователь не найден!'})
    else:
        return render(request, 'Authorize.html')

def autoriz_remove_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return render(request, 'Authorize.html', {'error': 'Введите email!'})
        try:
            user = Autoriz.objects.get(email=email)
            return render(request, 'reset_password.html', {'user': user})
        except Autoriz.DoesNotExist:
            return render(request, 'Authorize.html', {'error': 'Пользователь с таким email не найден!'})
    return redirect('autoriz_view')

def register_view(request):
    if request.method == 'POST':
        form = AutorizRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
            messages.success(request, 'Регистрация успешна! Заполните профиль.')
            return redirect('profile_edit_view')
    else:
        form = AutorizRegistrationForm()
    return render(request, 'register.html', {'form': form})

def main_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    check_homework_bonuses()
    
    context = get_user_context(request)
    user = context.get('user')
    
    if not user:
        return redirect('autoriz_view')
    
    try:
        student = Student.objects.get(autoriz=user)
        context['student'] = student
        balance_obj = getattr(student, 'balance_topcoins_and_topgems', None)
        context['balance'] = balance_obj
        
        if balance_obj:
            topmoney_obj = Topmoney_student.objects.filter(student=student).first()
            if topmoney_obj:
                context['topmoney'] = topmoney_obj.topmoney
            else:
                context['topmoney'] = balance_obj.topcoins + balance_obj.topgems
            
            context['topcoins'] = balance_obj.topcoins
            context['topgems'] = balance_obj.topgems
        
        from datetime import datetime, timedelta
        today = datetime.now().date()
        month_start = today.replace(day=1)
        
        month_estimations = Estimation.objects.filter(student=student, date__gte=month_start, date__lte=today)
        grades = [e.type_estimation for e in month_estimations if e.type_estimation]
        if grades:
            context['avg_grade'] = round(sum(grades) / len(grades), 1)
        else:
            context['avg_grade'] = 0
        
        month_attendances = Attendance.objects.filter(student=student, data_created__gte=month_start, data_created__lte=today)
        context['attendance_total'] = month_attendances.count()
        
        presence_count = month_attendances.filter(type='presence').count()
        late_count = month_attendances.filter(type='late').count()
        context['attendance_present'] = presence_count + late_count
        
        if context['attendance_total'] > 0:
            context['attendance_percent'] = round((context['attendance_present'] / context['attendance_total']) * 100)
        else:
            context['attendance_percent'] = 0
        
        all_homeworks = Add_HW_Professor_to_course.objects.filter(group=student.group)
        context['homework_total'] = all_homeworks.count()
        
        submissions = HomeworkSubmission.objects.filter(student=student)
        context['homework_completed'] = submissions.filter(is_checked=True, grade__isnull=False).count()
        context['homework_pending'] = submissions.filter(is_checked=False).count()
        
        expired_count = 0
        for hw in all_homeworks:
            if hw.date_final < today:
                try:
                    submission = HomeworkSubmission.objects.get(homework=hw, student=student)
                    if not submission.is_checked:
                        expired_count += 1
                except HomeworkSubmission.DoesNotExist:
                    expired_count += 1
        context['homework_expired'] = expired_count
        
        if student.group:
            group_students = Student.objects.filter(group=student.group)
            context['group_students_count'] = group_students.count()
            
            course_students = Student.objects.filter(group__course=student.group.course)
            context['course_students_count'] = course_students.count()
            
            ranking_entry = Ranking.objects.filter(student=student, semester__is_active=True).first()
            if not ranking_entry:
                ranking_entry = Ranking.objects.filter(student=student).first()
            
            if ranking_entry:
                context['group_rank'] = ranking_entry.group_rank
                context['course_rank'] = ranking_entry.course_rank
            else:
                update_student_rankings(student)
                ranking_entry = Ranking.objects.filter(student=student).first()
                if ranking_entry:
                    context['group_rank'] = ranking_entry.group_rank
                    context['course_rank'] = ranking_entry.course_rank
                else:
                    context['group_rank'] = '-'
                    context['course_rank'] = '-'
        
        scheduled_exams = ScheduledExam.objects.filter(group=student.group, preliminary_date__gte=today).order_by('preliminary_date')[:5]
        context['scheduled_exams'] = scheduled_exams
        
        context['announcements'] = Announcement.objects.filter(Q(is_for_all=True) | Q(groups=student.group)).distinct()[:5]
        context['homeworks'] = Add_HW_Professor_to_course.objects.filter(group=student.group).order_by('-date_start')[:5]
        context['events'] = Event.objects.filter(Q(is_for_all=True) | Q(groups=student.group), start_date__gte=timezone.now()).order_by('start_date')[:5]
        context['polls'] = Poll.objects.filter(Q(is_active=True), Q(groups=student.group) | Q(groups__isnull=True), start_date__lte=timezone.now(), end_date__gte=timezone.now()).distinct()
        
    except Student.DoesNotExist:
        try:
            professor = Professor.objects.get(autoriz=user)
            context['professor'] = professor
            context['unchecked_homeworks'] = HomeworkSubmission.objects.filter(homework__professor=professor, is_checked=False).count()
            context['my_subjects'] = Subjects.objects.filter(professor=professor)
        except Professor.DoesNotExist:
            try:
                staff = AcademicStaff.objects.get(autoriz=user)
                context['staff'] = staff
                context['pending_payments'] = PaymentInfo.objects.filter(period_end__gte=timezone.now().date()).count()
                context['total_students'] = Student.objects.count()
                context['total_professors'] = Professor.objects.count()
            except AcademicStaff.DoesNotExist:
                pass
    
    return render(request, 'main.html', context)

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('autoriz_view')

def profile_edit_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    chat_profile, _ = ChatProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user.birth_date = request.POST.get('birth_date') or None
        user.gender = request.POST.get('gender', '')
        user.phone = request.POST.get('phone', '')
        user.hide_phone = request.POST.get('hide_phone') == 'on'
        user.save()
        
        if request.FILES.get('avatar'):
            chat_profile.avatar = request.FILES['avatar']
        chat_profile.interests = request.POST.get('interests', '')
        chat_profile.about = request.POST.get('about', '')
        chat_profile.city = request.POST.get('city', '')
        chat_profile.save()
        
        return redirect('main_view')
    
    context['chat_profile'] = chat_profile
    return render(request, 'profile_edit.html', context)

def homework_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        all_homeworks = Add_HW_Professor_to_course.objects.filter(group=student.group).order_by('-date_start')
        
        homework_data = []
        today = timezone.now().date()
        
        for hw in all_homeworks:
            try:
                submission = HomeworkSubmission.objects.get(homework=hw, student=student)
                if submission.is_checked:
                    if submission.grade is not None:
                        status = 'checked'
                    else:
                        status = 'on_check'
                else:
                    status = 'submitted'
            except HomeworkSubmission.DoesNotExist:
                if hw.date_final < today:
                    status = 'expired'
                else:
                    status = 'pending'
            
            homework_data.append({
                'homework': hw,
                'submission': submission if 'submission' in locals() else None,
                'status': status,
                'grade': submission.grade if 'submission' in locals() and submission.grade else None
            })
        
        context['pending_homeworks'] = [h for h in homework_data if h['status'] == 'pending']
        context['expired_homeworks'] = [h for h in homework_data if h['status'] == 'expired']
        context['on_check_homeworks'] = [h for h in homework_data if h['status'] == 'on_check']
        context['checked_homeworks'] = [h for h in homework_data if h['status'] == 'checked']
        context['submitted_homeworks'] = [h for h in homework_data if h['status'] == 'submitted']
        context['student'] = student
        context['user_role'] = 'student'
        
    except Student.DoesNotExist:
        try:
            professor = Professor.objects.get(autoriz=user)
            submissions = HomeworkSubmission.objects.filter(homework__professor=professor).order_by('-submitted_at')
            
            submissions_data = []
            for sub in submissions:
                submissions_data.append({
                    'submission': sub,
                    'homework': sub.homework,
                    'student': sub.student,
                    'grade': sub.grade,
                    'is_checked': sub.is_checked
                })
            
            context['submissions_data'] = submissions_data
            context['user_role'] = 'professor'
            
        except Professor.DoesNotExist:
            return redirect('main_view')
    
    return render(request, 'homework_list.html', context)

def homework_add_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        professor = Professor.objects.get(autoriz=user)
        if request.method == 'POST':
            form = HomeworkAddForm(request.POST, request.FILES)
            if form.is_valid():
                hw = form.save(commit=False)
                hw.professor = professor
                hw.save()
                messages.success(request, 'Домашнее задание создано')
                return redirect('homework_list_view')
        else:
            form = HomeworkAddForm()
        context['form'] = form
        return render(request, 'homework_add.html', context)
    except Professor.DoesNotExist:
        return redirect('main_view')

def homework_submit_view(request, homework_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    homework = get_object_or_404(Add_HW_Professor_to_course, id=homework_id)
    
    try:
        student = Student.objects.get(autoriz=user)
        if student.group != homework.group:
            return redirect('homework_list_view')
        submission, created = HomeworkSubmission.objects.get_or_create(homework=homework, student=student)
        if request.method == 'POST':
            form = HomeworkSubmitForm(request.POST, request.FILES, instance=submission)
            if form.is_valid():
                form.save()
                messages.success(request, 'Домашнее задание сдано')
                return redirect('homework_list_view')
        else:
            form = HomeworkSubmitForm(instance=submission)
        context['form'] = form
        context['homework'] = homework
        return render(request, 'homework_submit.html', context)
    except Student.DoesNotExist:
        return redirect('main_view')

def homework_check_view(request, submission_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    submission = get_object_or_404(HomeworkSubmission, id=submission_id)
    
    try:
        professor = Professor.objects.get(autoriz=user)
        if submission.homework.professor != professor:
            return redirect('homework_list_view')
        if request.method == 'POST':
            form = HomeworkGradeForm(request.POST, instance=submission)
            if form.is_valid():
                homework_submission = form.save(commit=False)
                homework_submission.is_checked = True
                homework_submission.save()
                
                if homework_submission.grade:
                    try:
                        student = homework_submission.student
                        balance = balance_topcoins_and_topgems.objects.filter(student=student).first()
                        if balance:
                            topcoins_to_add = homework_submission.grade * 10
                            balance.topcoins += topcoins_to_add
                            balance.save()
                            update_topmoney_for_student(student)
                    except:
                        pass
                
                check_homework_bonuses()
                
                messages.success(request, f'Работа проверена! Оценка: {homework_submission.grade}')
                return redirect('homework_list_view')
        else:
            form = HomeworkGradeForm(instance=submission)
        context['form'] = form
        context['submission'] = submission
        return render(request, 'homework_check.html', context)
    except Professor.DoesNotExist:
        return redirect('main_view')

def schedule_view(request, group_id=None):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    group = None
    schedules = []
    
    try:
        student = Student.objects.get(autoriz=user)
        group = student.group
        context['user_role'] = 'student'
        schedules = Schedule.objects.filter(group=group, is_active=True).order_by('-week_start_date')
        weekdays = [(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота'), (7, 'Воскресенье')]
        context['schedules'] = schedules
        context['group'] = group
        context['weekdays'] = weekdays
        return render(request, 'schedule.html', context)
        
    except Student.DoesNotExist:
        try:
            professor = Professor.objects.get(autoriz=user)
            context['user_role'] = 'professor'
            return render(request, 'schedule_professor.html', context)
            
        except Professor.DoesNotExist:
            try:
                staff = AcademicStaff.objects.get(autoriz=user)
                context['user_role'] = 'academic_staff'
                if group_id:
                    group = get_object_or_404(Group, id=group_id)
                else:
                    groups = Group.objects.all()
                    if groups.exists():
                        group = groups.first()
                if group:
                    schedules = Schedule.objects.filter(group=group, is_active=True).order_by('-week_start_date')
                weekdays = [(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота'), (7, 'Воскресенье')]
                context['schedules'] = schedules
                context['group'] = group
                context['weekdays'] = weekdays
                return render(request, 'schedule.html', context)
                
            except AcademicStaff.DoesNotExist:
                return redirect('main_view')

def schedule_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    if context.get('user_role') not in ['academic_staff', 'professor']:
        return redirect('main_view')
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Расписание создано')
            return redirect('schedule_view')
    else:
        form = ScheduleForm()
    
    context['form'] = form
    context['subjects'] = Subjects.objects.all()
    context['professors'] = Professor.objects.all()
    context['classrooms'] = Add_Сlassroom.objects.all()
    
    return render(request, 'schedule_create.html', context)

def daily_schedule_add_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = DailyScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Занятие добавлено в расписание')
            return redirect('schedule_view')
    else:
        form = DailyScheduleForm()
    
    context['form'] = form
    return render(request, 'daily_schedule_add.html', context)

def pair_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = PairForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пара создана')
            return redirect('pair_list_view')
    else:
        form = PairForm()
    
    context['form'] = form
    return render(request, 'pair_create.html', context)

def pair_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['pairs'] = Pair.objects.all().order_by('pair_number')
    
    return render(request, 'pair_list.html', context)

def lesson_type_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = LessonTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип занятия создан')
            return redirect('lesson_type_list_view')
    else:
        form = LessonTypeForm()
    
    context['form'] = form
    return render(request, 'lesson_type_create.html', context)

def lesson_type_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['lesson_types'] = LessonType.objects.all()
    
    return render(request, 'lesson_type_list.html', context)

def add_classroom_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = AddClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аудитория добавлена')
            return redirect('classroom_list_view')
    else:
        form = AddClassroomForm()
    
    context['form'] = form
    return render(request, 'add_classroom.html', context)

def classroom_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['classrooms'] = Add_Сlassroom.objects.all()
    
    return render(request, 'classroom_list.html', context)

def semester_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Семестр создан')
            return redirect('semester_list_view')
    else:
        form = SemesterForm()
    
    context['form'] = form
    return render(request, 'semester_create.html', context)

def semester_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['semesters'] = Semester.objects.all().order_by('-start_date')
    
    return render(request, 'semester_list.html', context)

def vacation_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = VacationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Каникулы добавлены')
            return redirect('vacation_list_view')
    else:
        form = VacationForm()
    
    context['form'] = form
    return render(request, 'vacation_create.html', context)

def vacation_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['vacations'] = Vacation.objects.all().order_by('start_date')
    
    return render(request, 'vacation_list.html', context)

def schedule_replacement_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = ScheduleReplacementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Замена создана')
            return redirect('schedule_replacement_list_view')
    else:
        form = ScheduleReplacementForm()
    
    context['form'] = form
    return render(request, 'schedule_replacement_create.html', context)

def schedule_replacement_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['replacements'] = ScheduleReplacement.objects.all().order_by('-created_at')
    
    return render(request, 'schedule_replacement_list.html', context)

def attendance_mark_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    user = Autoriz.objects.get(id=request.session['user_id'])
    
    try:
        professor = Professor.objects.get(autoriz=user)
        today = datetime.now().date()
        weekday = today.isoweekday()
        
        daily_schedules = DailySchedule.objects.filter(
            weekday=weekday,
            pair__professor=professor,
            schedule__isnull=False
        ).select_related('pair', 'pair__subject', 'pair__classroom', 'group')
        
        today_pairs = []
        for ds in daily_schedules:
            time_display = ds.pair.get_pair_number_display()
            time_parts = time_display.split('-') if time_display else ['--:--', '--:--']
            
            status = 'pending'
            if ds.is_completed:
                status = 'completed'
            elif ds.is_missed:
                status = 'missed'
            
            print(f"Pair {ds.id}: is_completed={ds.is_completed}, is_missed={ds.is_missed}, status={status}")
            
            today_pairs.append({
                'id': ds.id,
                'pair_number': ds.pair_order,
                'time_start': time_parts[0].strip(),
                'time_end': time_parts[1].strip() if len(time_parts) > 1 else '--:--',
                'subject': ds.pair.subject.name_subject,
                'group': ds.group.name,
                'classroom': ds.pair.classroom.name_classroom if ds.pair.classroom else None,
                'status': status,
                'topic': ds.topic or ''
            })
        
        context = get_user_context(request)
        context['today_pairs'] = today_pairs
        context['current_date'] = today
        context['weekday_name'] = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'][weekday - 1]
        
    except Professor.DoesNotExist:
        context = get_user_context(request)
        context['today_pairs'] = []
    
    return render(request, 'attendance_mark.html', context)

def attendance_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        attendances = Attendance.objects.filter(student=student).order_by('-data_created')
        
        attendance_data = []
        for att in attendances:
            subject_name = '-'
            professor_name = '-'
            pair_number = '-'
            
            if att.pair:
                subject_name = att.pair.subject.name_subject if att.pair.subject else '-'
                professor_name = str(att.pair.professor) if att.pair.professor else '-'
                pair_number = att.pair.get_pair_number_display() if att.pair.pair_number else '-'
            elif att.schedule:
                daily = DailySchedule.objects.filter(schedule=att.schedule, group=student.group).first()
                if daily and daily.pair:
                    subject_name = daily.pair.subject.name_subject if daily.pair.subject else '-'
                    professor_name = str(daily.pair.professor) if daily.pair.professor else '-'
                    pair_number = daily.pair.get_pair_number_display() if daily.pair.pair_number else '-'
            
            attendance_data.append({
                'attendance': att,
                'subject_name': subject_name,
                'professor_name': professor_name,
                'pair_number': pair_number,
            })
        
        context['attendance_data'] = attendance_data
        context['present_count'] = attendances.filter(type='presence').count()
        context['late_count'] = attendances.filter(type='late').count()
        context['absent_count'] = attendances.filter(type='absence').count()
        context['total_count'] = attendances.count()
        context['subjects'] = Subjects.objects.all()
        
    except Student.DoesNotExist:
        return redirect('main_view')
    
    return render(request, 'attendance_list.html', context)

def estimation_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        professor = Professor.objects.get(autoriz=user)
        context['estimations'] = Estimation.objects.filter(subject=professor.leads_the_subject).order_by('-date')
        context['subjects'] = Subjects.objects.filter(id=professor.leads_the_subject.id)
        context['user_role'] = 'professor'
        context['professor_subject'] = professor.leads_the_subject.name_subject
        context['groups'] = Group.objects.all()
        return render(request, 'estimation.html', context)
    except Professor.DoesNotExist:
        try:
            student = Student.objects.get(autoriz=user)
            context['estimations'] = Estimation.objects.filter(student=student).order_by('-date')
            context['subjects'] = Subjects.objects.all()
            context['user_role'] = 'student'
            return render(request, 'estimation.html', context)
        except Student.DoesNotExist:
            return redirect('main_view')

def shop_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    context['products'] = Shop_add_products.objects.all()
    
    try:
        student = Student.objects.get(autoriz=user)
        balance = getattr(student, 'balance_topcoins_and_topgems', None)
        context['balance'] = balance
        
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Shop_add_products, id=product_id)
            
            if product.product_quantity <= 0:
                messages.error(request, f'Товар "{product.name_product}" закончился на складе!')
                return redirect('shop_view')
            
            if balance and balance.topcoins >= product.price_product_topcoins:
                balance.topcoins -= product.price_product_topcoins
                balance.save()
                
                product.product_quantity -= 1
                product.save()
                
                update_topmoney_for_student(student)
                
                messages.success(request, f'🎉 Поздравляем с покупкой "{product.name_product}"!')
            else:
                messages.error(request, 'Недостаточно топкоинов для покупки!')
            return redirect('shop_view')
    except Student.DoesNotExist:
        pass
    
    return render(request, 'shop.html', context)

def shop_product_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = ShopProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар добавлен в магазин')
            return redirect('shop_view')
    else:
        form = ShopProductForm()
    
    context['form'] = form
    return render(request, 'shop_product_create.html', context)

def leaderboard_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    try:
        student = Student.objects.get(autoriz=context['user'])
        current_group = student.group
        current_course = current_group.course if current_group else None
        
        if current_group:
            group_students = Student.objects.filter(group=current_group)
            group_leaderboard = []
            
            for s in group_students:
                topmoney_obj = Topmoney_student.objects.filter(student=s).first()
                topmoney = topmoney_obj.topmoney if topmoney_obj else 0
                group_leaderboard.append({
                    'student': s,
                    'topmoney': topmoney,
                    'rank': 0
                })
            
            group_leaderboard.sort(key=lambda x: x['topmoney'], reverse=True)
            
            for idx, item in enumerate(group_leaderboard):
                item['rank'] = idx + 1
            
            context['group_leaderboard'] = group_leaderboard
            context['group_name'] = current_group.name
            
            if current_course:
                course_students = Student.objects.filter(group__course=current_course)
                course_leaderboard = []
                
                for s in course_students:
                    topmoney_obj = Topmoney_student.objects.filter(student=s).first()
                    topmoney = topmoney_obj.topmoney if topmoney_obj else 0
                    course_leaderboard.append({
                        'student': {
                            'id': s.id,
                            'surname': s.surname,
                            'name': s.name,
                            'patronymic': s.patronymic,
                            'group': {
                                'name': s.group.name if s.group else '-'
                            }
                        },
                        'topmoney': topmoney,
                        'rank': 0
                    })
                
                course_leaderboard.sort(key=lambda x: x['topmoney'], reverse=True)
                
                for idx, item in enumerate(course_leaderboard):
                    item['rank'] = idx + 1
                
                context['course_leaderboard'] = course_leaderboard
                context['course_name'] = current_course.number
            
        else:
            context['group_leaderboard'] = []
            context['course_leaderboard'] = []
            context['student'] = None
        
    except Student.DoesNotExist:
        context['group_leaderboard'] = []
        context['course_leaderboard'] = []
        context['student'] = None
    
    return render(request, 'leaderboard.html', context)

def polls_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        polls = Poll.objects.filter(
            Q(groups=student.group) | Q(groups__isnull=True),
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).distinct()
    except Student.DoesNotExist:
        polls = Poll.objects.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
    
    context['polls'] = polls
    return render(request, 'polls.html', context)

def poll_detail_view(request, poll_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    poll = get_object_or_404(Poll, id=poll_id)
    
    if request.method == 'POST':
        option_id = request.POST.get('option')
        option = get_object_or_404(PollOption, id=option_id)
        PollVote.objects.get_or_create(poll=poll, user=user, defaults={'option': option})
        messages.success(request, 'Голос учтён')
        return redirect('polls_view')
    
    options = poll.options.all()
    user_vote = PollVote.objects.filter(poll=poll, user=user).first()
    total_votes = sum(opt.votes for opt in options)
    
    context['poll'] = poll
    context['options'] = options
    context['user_vote'] = user_vote
    context['total_votes'] = total_votes
    
    return render(request, 'poll_detail.html', context)

def poll_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save()
            messages.success(request, 'Опрос создан. Теперь добавьте варианты ответов.')
            return redirect('poll_option_add_view', poll_id=poll.id)
    else:
        form = PollForm()
    
    context['form'] = form
    return render(request, 'poll_create.html', context)

def poll_option_add_view(request, poll_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    poll = get_object_or_404(Poll, id=poll_id)
    
    if request.method == 'POST':
        form = PollOptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.poll = poll
            option.save()
            messages.success(request, 'Вариант ответа добавлен')
            return redirect('poll_option_add_view', poll_id=poll.id)
    else:
        form = PollOptionForm()
    
    context['form'] = form
    context['poll'] = poll
    context['options'] = poll.options.all()
    
    return render(request, 'poll_option_add.html', context)

def announcements_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        announcements = Announcement.objects.filter(
            Q(is_for_all=True) | Q(groups=student.group)
        ).distinct().order_by('-date_added')
    except Student.DoesNotExist:
        announcements = Announcement.objects.all().order_by('-date_added')
    
    context['announcements'] = announcements
    return render(request, 'announcements.html', context)

def announcement_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление создано')
            return redirect('announcements_view')
    else:
        form = AnnouncementForm()
    
    context['form'] = form
    context['groups'] = Group.objects.all()
    
    return render(request, 'announcement_create.html', context)

def events_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        events = Event.objects.filter(
            Q(is_for_all=True) | Q(groups=student.group),
            start_date__gte=timezone.now()
        ).order_by('start_date')
    except Student.DoesNotExist:
        events = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')
    
    context['events'] = events
    return render(request, 'events.html', context)

def event_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Событие создано')
            return redirect('events_view')
    else:
        form = EventForm()
    
    context['form'] = form
    context['groups'] = Group.objects.all()
    
    return render(request, 'event_create.html', context)

def payment_info_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = PaymentInfoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Платёж добавлен')
            return redirect('payment_info_view')
    else:
        form = PaymentInfoForm()
    
    payments = PaymentInfo.objects.all().order_by('-payment_date')
    total_paid = sum(p.amount_paid for p in payments)
    from datetime import datetime
    monthly_paid = sum(p.amount_paid for p in payments if p.payment_date.month == datetime.now().month)
    
    context['form'] = form
    context['payments'] = payments
    context['total_paid'] = total_paid
    context['monthly_paid'] = monthly_paid
    
    return render(request, 'payment_info.html', context)

def educational_materials_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        materials = EducationalMaterial.objects.filter(
            Q(is_public=True) | Q(groups=student.group)
        ).distinct().order_by('-upload_date')
        context['subjects'] = Subjects.objects.all()
        context['user_role'] = 'student'
    except Student.DoesNotExist:
        try:
            professor = Professor.objects.get(autoriz=user)
            materials = EducationalMaterial.objects.filter(professor=professor).order_by('-upload_date')
            context['subjects'] = Subjects.objects.filter(id=professor.leads_the_subject.id)
            context['user_role'] = 'professor'
        except Professor.DoesNotExist:
            materials = EducationalMaterial.objects.all().order_by('-upload_date')
            context['subjects'] = Subjects.objects.all()
            context['user_role'] = 'unknown'
    
    context['materials'] = materials
    return render(request, 'materials.html', context)

def educational_material_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        professor = Professor.objects.get(autoriz=user)
        if request.method == 'POST':
            form = EducationalMaterialForm(request.POST, request.FILES)
            if form.is_valid():
                material = form.save(commit=False)
                material.professor = professor
                material.save()
                form.save_m2m()
                messages.success(request, 'Материал загружен')
                return redirect('educational_materials_view')
        else:
            form = EducationalMaterialForm()
            form.fields['subject'].queryset = Subjects.objects.filter(id=professor.leads_the_subject.id)
            form.fields['subject'].initial = professor.leads_the_subject
        
        context['form'] = form
        context['groups'] = Group.objects.all()
        context['subjects'] = Subjects.objects.filter(id=professor.leads_the_subject.id)
        return render(request, 'educational_material_create.html', context)
    except Professor.DoesNotExist:
        return redirect('main_view')

def appeal_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        if request.method == 'POST':
            form = AppealForm(request.POST)
            if form.is_valid():
                appeal = form.save(commit=False)
                appeal.student = student
                appeal.save()
                messages.success(request, 'Ваш вопрос отправлен')
                return redirect('main_view')
        else:
            form = AppealForm()
        
        context['form'] = form
        return render(request, 'appeal.html', context)
    except Student.DoesNotExist:
        return redirect('main_view')

def review_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.student = student
                review.save()
                messages.success(request, 'Спасибо за отзыв!')
                return redirect('main_view')
        else:
            form = ReviewForm()
        
        context['form'] = form
        context['my_reviews'] = Review_of_the_Academy.objects.filter(student=student)
        return render(request, 'review.html', context)
    except Student.DoesNotExist:
        return redirect('main_view')

def complaint_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        if request.method == 'POST':
            form = ComplaintForm(request.POST)
            if form.is_valid():
                complaint = form.save(commit=False)
                complaint.student = student
                complaint.save()
                messages.success(request, 'Жалоба отправлена')
                return redirect('main_view')
        else:
            form = ComplaintForm()
        
        context['form'] = form
        return render(request, 'complaint.html', context)
    except Student.DoesNotExist:
        return redirect('main_view')

def student_review_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        professor = Professor.objects.get(autoriz=user)
        reviews = Student_Reviews.objects.filter(professor=professor).order_by('-date')
        groups = Group.objects.all()
        context['reviews'] = reviews
        context['groups'] = groups
        context['user_role'] = 'professor'
    except Professor.DoesNotExist:
        try:
            staff = AcademicStaff.objects.get(autoriz=user)
            reviews = Student_Reviews.objects.all().order_by('-date')
            groups = Group.objects.all()
            context['reviews'] = reviews
            context['groups'] = groups
            context['user_role'] = 'academic_staff'
        except AcademicStaff.DoesNotExist:
            return redirect('main_view')
    
    return render(request, 'student_review_list.html', context)

def student_review_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        professor = Professor.objects.get(autoriz=user)
        
        if request.method == 'POST':
            form = StudentReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.professor = professor
                review.save()
                messages.success(request, 'Отзыв о студенте добавлен')
                return redirect('student_review_create_view')
        else:
            form = StudentReviewForm()
            form.fields['subject'].queryset = Subjects.objects.filter(id=professor.leads_the_subject.id)
            form.fields['professor'].initial = professor
            form.fields['professor'].widget = forms.HiddenInput()
        
        all_students = Student.objects.select_related('group').all()
        students_data = []
        for s in all_students:
            students_data.append({
                'id': s.id,
                'full_name': f"{s.surname} {s.name} {s.patronymic}".strip(),
                'group': s.group.name if s.group else None
            })
        
        context['form'] = form
        context['professor'] = professor
        context['recent_reviews'] = Student_Reviews.objects.filter(professor=professor).order_by('-date')[:3]
        context['students_json'] = json.dumps(students_data)
        context['user_role'] = 'professor'
        
    except Professor.DoesNotExist:
        return redirect('main_view')
    
    return render(request, 'student_review_create.html', context)

def chat_list_view(request, chat_id=None):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    user = Autoriz.objects.get(id=request.session['user_id'])
    
    topcoins = 0
    topgems = 0
    user_avatar = None
    student_info = None
    professor_info = None
    user_full_name = user.get_full_name() or user.user
    
    try:
        student = Student.objects.get(autoriz=user)
        user_full_name = f"{student.surname} {student.name} {student.patronymic}".strip()
        
        if student.group:
            student_info = {
                'direction': student.group.direction.name if student.group.direction else '-',
                'course': student.group.course.number if student.group.course else '-',
                'group': student.group.name
            }
        else:
            student_info = {
                'direction': '-',
                'course': '-',
                'group': '-'
            }
        
        balance = balance_topcoins_and_topgems.objects.filter(student=student).first()
        if balance:
            topcoins = balance.topcoins
            topgems = balance.topgems
            
    except Student.DoesNotExist:
        try:
            professor = Professor.objects.get(autoriz=user)
            user_full_name = f"{professor.surname} {professor.name} {professor.patronymic}".strip()
            if professor.leads_the_subject:
                professor_info = {
                    'subject': professor.leads_the_subject.name_subject
                }
        except Professor.DoesNotExist:
            try:
                staff = AcademicStaff.objects.get(autoriz=user)
                user_full_name = f"{staff.surname} {staff.name} {staff.patronymic}".strip()
            except AcademicStaff.DoesNotExist:
                pass
    
    try:
        chat_profile = ChatProfile.objects.get(user=user)
        if chat_profile.avatar and chat_profile.avatar.url:
            user_avatar = chat_profile.avatar.url
    except ChatProfile.DoesNotExist:
        pass
    
    user_role = None
    if Student.objects.filter(autoriz=user).exists():
        user_role = 'student'
    elif Professor.objects.filter(autoriz=user).exists():
        user_role = 'professor'
    elif AcademicStaff.objects.filter(autoriz=user).exists():
        user_role = 'academic_staff'
    
    chats = Chat.objects.filter(participants=user)
    
    all_participants = []
    for chat in chats:
        for p in chat.participants.all():
            if p != user:
                all_participants.append(p)
    
    students = {s.autoriz_id: s for s in Student.objects.filter(autoriz_id__in=[p.id for p in all_participants])}
    professors = {p.autoriz_id: p for p in Professor.objects.filter(autoriz_id__in=[p.id for p in all_participants])}
    academic_staffs = {a.autoriz_id: a for a in AcademicStaff.objects.filter(autoriz_id__in=[p.id for p in all_participants])}
    
    for participant in all_participants:
        if participant.id in students:
            participant.student = students[participant.id]
        elif participant.id in professors:
            participant.professor = professors[participant.id]
        elif participant.id in academic_staffs:
            participant.academicstaff = academic_staffs[participant.id]
    
    selected_chat = None
    messages_list = []
    
    if chat_id:
        selected_chat = get_object_or_404(Chat, id=chat_id, participants=user)
        for p in selected_chat.participants.all():
            if p != user:
                if p.id in students:
                    p.student = students[p.id]
                elif p.id in professors:
                    p.professor = professors[p.id]
                elif p.id in academic_staffs:
                    p.academicstaff = academic_staffs[p.id]
        Message.objects.filter(chat=selected_chat, sender__in=selected_chat.participants.exclude(id=user.id), is_delivered=False).update(is_delivered=True)
        messages_list = selected_chat.messages.all().order_by('created_at')
    
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        delete_id = request.POST.get('delete_id')
        text = request.POST.get('text')
        file = request.FILES.get('file')
        reply_to_id = request.POST.get('reply_to')
        
        if delete_id:
            try:
                msg = Message.objects.get(id=delete_id, sender=user)
                msg.delete()
                return JsonResponse({'success': True})
            except Message.DoesNotExist:
                return JsonResponse({'success': False})
        
        if edit_id:
            try:
                msg = Message.objects.get(id=edit_id, sender=user)
                msg.text = text
                msg.save()
                return JsonResponse({'success': True})
            except Message.DoesNotExist:
                return JsonResponse({'success': False})
        
        if selected_chat and (text or file):
            original_filename = None
            saved_path = None
            if file:
                original_filename = file.name
                saved_path = default_storage.save(f'chat_files/chat_{selected_chat.id}/{file.name}', file)
            
            reply_to_msg = None
            if reply_to_id:
                try:
                    reply_to_msg = Message.objects.get(id=reply_to_id)
                except Message.DoesNotExist:
                    pass
            
            Message.objects.create(
                chat=selected_chat,
                sender=user,
                text=text or '',
                file=saved_path,
                original_filename=original_filename,
                is_delivered=False,
                is_read=False,
                reply_to=reply_to_msg
            )
            return JsonResponse({'success': True})
        
        return JsonResponse({'success': False})
    
    from datetime import date, timedelta
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    return render(request, 'chat_list.html', {
        'chats': chats,
        'selected_chat': selected_chat,
        'messages': messages_list,
        'user': user,
        'user_role': user_role,
        'user_avatar': user_avatar,
        'user_full_name': user_full_name,
        'student_info': student_info,
        'professor_info': professor_info,
        'topcoins': topcoins,
        'topgems': topgems,
        'today': today.strftime('%Y-%m-%d'),
        'yesterday': yesterday.strftime('%Y-%m-%d'),
    })

def create_chat_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    current_user = context.get('user')
    
    if request.method == 'POST':
        target_user_id = request.POST.get('target_user')
        target_user = get_object_or_404(Autoriz, id=target_user_id)
        existing_chats = Chat.objects.filter(participants=current_user).filter(participants=target_user)
        if existing_chats.exists():
            return redirect('chat_detail_view', chat_id=existing_chats.first().id)
        chat = Chat.objects.create()
        chat.participants.add(current_user, target_user)
        return redirect('chat_detail_view', chat_id=chat.id)
    
    users_with_details = []
    for u in Autoriz.objects.exclude(id=current_user.id):
        full_name = u.user
        role = ''
        try:
            student = Student.objects.get(autoriz=u)
            full_name = f"{student.surname} {student.name} {student.patronymic}"
            role = 'Студент'
        except Student.DoesNotExist:
            try:
                professor = Professor.objects.get(autoriz=u)
                full_name = f"{professor.surname} {professor.name} {professor.patronymic}"
                role = 'Преподаватель'
            except Professor.DoesNotExist:
                try:
                    staff = AcademicStaff.objects.get(autoriz=u)
                    full_name = f"{staff.surname} {staff.name} {staff.patronymic}"
                    role = 'Учебная часть'
                except AcademicStaff.DoesNotExist:
                    full_name = u.user
                    role = 'Пользователь'
        
        users_with_details.append({
            'id': u.id,
            'username': u.user,
            'full_name': full_name,
            'email': u.email,
            'role': role
        })
    
    context['users'] = users_with_details
    return render(request, 'create_chat.html', context)

def exam_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        exams = Exam.objects.filter(student=student).order_by('-exam_date')
        passed_count = exams.filter(grade__gte=3).count()
        grades = [e.grade for e in exams if e.grade]
        avg_grade = round(sum(grades) / len(grades), 1) if grades else None
    except Student.DoesNotExist:
        try:
            professor = Professor.objects.get(autoriz=user)
            exams = Exam.objects.filter(professor=professor).order_by('-exam_date')
            passed_count = exams.filter(grade__gte=3).count()
            grades = [e.grade for e in exams if e.grade]
            avg_grade = round(sum(grades) / len(grades), 1) if grades else None
        except Professor.DoesNotExist:
            exams = Exam.objects.all().order_by('-exam_date')
            passed_count = exams.filter(grade__gte=3).count()
            grades = [e.grade for e in exams if e.grade]
            avg_grade = round(sum(grades) / len(grades), 1) if grades else None
    
    context['exams'] = exams
    context['passed_count'] = passed_count
    context['avg_grade'] = avg_grade
    
    return render(request, 'exam_list.html', context)

def exam_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = ExamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Экзамен добавлен')
            return redirect('exam_list_view')
    else:
        form = ExamForm()
    
    context['form'] = form
    context['students'] = Student.objects.all()
    context['subjects'] = Subjects.objects.all()
    context['professors'] = Professor.objects.all()
    context['semesters'] = Semester.objects.all()
    
    return render(request, 'exam_create.html', context)

def exam_session_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = ExamSessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Экзаменационная сессия создана')
            return redirect('exam_session_list_view')
    else:
        form = ExamSessionForm()
    
    context['form'] = form
    return render(request, 'exam_session_create.html', context)

def exam_session_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['sessions'] = ExamSession.objects.all().order_by('-start_date')
    
    return render(request, 'exam_session_list.html', context)

def scheduled_exam_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    if request.method == 'POST':
        form = ScheduledExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = user.professor if hasattr(user, 'professor') else None
            exam.save()
            messages.success(request, 'Экзамен назначен')
            return redirect('scheduled_exam_list_view')
    else:
        form = ScheduledExamForm()
    
    context['form'] = form
    return render(request, 'scheduled_exam_create.html', context)

def scheduled_exam_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['exams'] = ScheduledExam.objects.all().order_by('preliminary_date')
    
    return render(request, 'scheduled_exam_list.html', context)

def academic_debt_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = AcademicDebtForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задолженность добавлена')
            return redirect('academic_debt_list_view')
    else:
        form = AcademicDebtForm()
    
    context['form'] = form
    return render(request, 'academic_debt_create.html', context)

def academic_debt_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['debts'] = AcademicDebt.objects.all().order_by('exam_date')
    
    return render(request, 'academic_debt_list.html', context)

def graduation_work_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = GraduationWorkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Дипломная работа добавлена')
            return redirect('graduation_work_list_view')
    else:
        form = GraduationWorkForm()
    
    context['form'] = form
    return render(request, 'graduation_work_create.html', context)

def graduation_work_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['works'] = GraduationWork.objects.all().order_by('-defense_date')
    
    return render(request, 'graduation_work_list.html', context)

def internship_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = InternshipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Практика добавлена')
            return redirect('internship_list_view')
    else:
        form = InternshipForm()
    
    context['form'] = form
    return render(request, 'internship_create.html', context)

def internship_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['internships'] = Internship.objects.all().order_by('-start_date')
    
    return render(request, 'internship_list.html', context)

def group_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['groups'] = Group.objects.all()
    
    return render(request, 'group_list.html', context)

def group_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Группа создана')
            return redirect('group_list_view')
    else:
        form = GroupForm()
    
    context['form'] = form
    return render(request, 'group_create.html', context)

def subject_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    subjects = Subjects.objects.all()
    
    context['subjects'] = subjects
    context['subjects_with_professors'] = subjects.filter(professor__isnull=False).count()
    context['groups'] = Group.objects.all()
    
    return render(request, 'subject_list.html', context)

def subject_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = SubjectsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Предмет добавлен')
            return redirect('subject_list_view')
    else:
        form = SubjectsForm()
    
    context['form'] = form
    return render(request, 'subject_create.html', context)

def course_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    courses = Course.objects.all()
    for c in courses:
        c.student_count = Student.objects.filter(group__course=c).count()
    
    context['courses'] = courses
    return render(request, 'course_list.html', context)

def course_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс добавлен')
            return redirect('course_list_view')
    else:
        form = CourseForm()
    
    context['form'] = form
    return render(request, 'course_create.html', context)

def direction_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    directions = Direction.objects.all()
    for d in directions:
        d.student_count = Student.objects.filter(group__direction=d).count()
    
    context['directions'] = directions
    context['active_directions'] = directions.filter(group__isnull=False).distinct().count()
    
    return render(request, 'direction_list.html', context)

def direction_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = DirectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Направление добавлено')
            return redirect('direction_list_view')
    else:
        form = DirectionForm()
    
    context['form'] = form
    return render(request, 'direction_create.html', context)

def academic_year_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['years'] = AcademicYear.objects.all().order_by('-start_date')
    
    return render(request, 'academic_year_list.html', context)

def academic_year_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    
    if request.method == 'POST':
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Учебный год добавлен')
            return redirect('academic_year_list_view')
    else:
        form = AcademicYearForm()
    
    context['form'] = form
    return render(request, 'academic_year_create.html', context)

def notification_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    context['notifications'] = Notification.objects.filter(user=user).order_by('-created_at')
    
    return render(request, 'notification_list.html', context)

def notification_mark_read_view(request, notification_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('notification_list_view')

def debtor_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    debtors = Debtor.objects.filter(is_paid=False).order_by('due_date')
    
    context['debtors'] = debtors
    context['total_debt'] = sum(d.debt_amount for d in debtors)
    context['groups'] = Group.objects.all()
    
    return render(request, 'debtor_list.html', context)

def scholarship_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['scholarships'] = Scholarship.objects.all().order_by('-month')
    
    return render(request, 'scholarship_list.html', context)

def personal_account_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        context['personal_account'] = PersonalAccount.objects.get(user=user)
    except PersonalAccount.DoesNotExist:
        context['personal_account'] = None
    
    return render(request, 'personal_account.html', context)

def personal_account_edit_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        personal_account = PersonalAccount.objects.get(user=user)
    except PersonalAccount.DoesNotExist:
        personal_account = None
    
    if request.method == 'POST':
        form = PersonalAccountForm(request.POST, request.FILES, instance=personal_account)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = user
            account.save()
            messages.success(request, 'Личный кабинет обновлён')
            return redirect('personal_account_view')
    else:
        form = PersonalAccountForm(instance=personal_account)
    
    context['form'] = form
    return render(request, 'personal_account_edit.html', context)

def student_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['students'] = Student.objects.all()
    
    return render(request, 'student_list.html', context)

def professor_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['professors'] = Professor.objects.all()
    
    return render(request, 'professor_list.html', context)

def academic_staff_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['staff'] = AcademicStaff.objects.all()
    
    return render(request, 'academic_staff_list.html', context)

def student_detail_view(request, student_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['student'] = get_object_or_404(Student, id=student_id)
    
    return render(request, 'student_detail.html', context)

def professor_detail_view(request, professor_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['professor'] = get_object_or_404(Professor, id=professor_id)
    
    return render(request, 'professor_detail.html', context)

def balance_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['balances'] = balance_topcoins_and_topgems.objects.all()
    
    return render(request, 'balance_list.html', context)

def topmoney_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['topmoney_list'] = Topmoney_student.objects.all().order_by('-topmoney')
    
    return render(request, 'topmoney_list.html', context)

def ranking_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['rankings'] = Ranking.objects.filter(semester__is_active=True).order_by('group_rank')[:50]
    
    return render(request, 'ranking_list.html', context)

def reward_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['rewards'] = Reward.objects.filter(is_active=True)
    
    return render(request, 'reward_list.html', context)

def user_reward_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        user_rewards = UserReward.objects.filter(student=student).order_by('-awarded_at')
        context['user_rewards'] = user_rewards
        context['total_topcoins'] = sum(ur.topcoins_given for ur in user_rewards)
        context['total_topgems'] = sum(ur.topgems_given for ur in user_rewards)
        return render(request, 'user_reward_list.html', context)
    except Student.DoesNotExist:
        return redirect('main_view')

def type_work_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['types'] = Type_work.objects.all()
    
    return render(request, 'type_work_list.html', context)

def image_student_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['images'] = image_student.objects.all()
    
    return render(request, 'image_student_list.html', context)

def image_professor_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['images'] = image_professor.objects.all()
    
    return render(request, 'image_professor_list.html', context)

def students_payment_account_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['accounts'] = Students_payment_account.objects.all()
    
    return render(request, 'students_payment_account_list.html', context)

def all_payment_of_education_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['payments'] = All_payment_of_education.objects.all()
    
    return render(request, 'all_payment_of_education_list.html', context)

def student_stats_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    context['stats'] = StudentStats.objects.all()
    
    return render(request, 'student_stats_list.html', context)

def api_get_pairs(request):
    schedule_id = request.GET.get('schedule_id')
    if not schedule_id:
        return JsonResponse({'success': False, 'error': 'No schedule_id'})
    try:
        schedule = Schedule.objects.get(id=schedule_id)
        pairs = []
        for daily in schedule.dailyschedule_set.all().order_by('pair_order'):
            pairs.append({
                'id': daily.pair.id,
                'number': daily.pair_order,
                'subject': daily.pair.subject.name_subject,
                'professor': str(daily.pair.professor)
            })
        return JsonResponse({'success': True, 'pairs': pairs})
    except Schedule.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Schedule not found'})

def api_get_students(request):
    schedule_id = request.GET.get('schedule_id')
    pair_id = request.GET.get('pair_id')
    if not schedule_id or not pair_id:
        return JsonResponse({'success': False, 'error': 'Missing parameters'})
    try:
        schedule = Schedule.objects.get(id=schedule_id)
        pair = Pair.objects.get(id=pair_id)
        students = schedule.group.student_set.all()
        students_data = []
        for student in students:
            students_data.append({
                'id': student.id,
                'name': str(student)
            })
        return JsonResponse({
            'success': True,
            'group_name': schedule.group.name,
            'schedule_date': schedule.week_start_date.strftime('%d.%m.%Y'),
            'pair_info': f'{pair.get_pair_number_display()} пара: {pair.subject.name_subject} ({pair.professor})',
            'students': students_data
        })
    except (Schedule.DoesNotExist, Pair.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Not found'})

def api_delete_chat(request, chat_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    user = Autoriz.objects.get(id=request.session['user_id'])
    chat = get_object_or_404(Chat, id=chat_id, participants=user)
    chat.participants.remove(user)
    if chat.participants.count() == 0:
        chat.delete()
    return JsonResponse({'success': True})

def api_chat_messages(request, chat_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    user = Autoriz.objects.get(id=request.session['user_id'])
    chat = get_object_or_404(Chat, id=chat_id, participants=user)
    last_id = request.GET.get('last_id', 0)
    
    Message.objects.filter(chat=chat, sender__in=chat.participants.exclude(id=user.id), is_delivered=False).update(is_delivered=True)
    
    if request.GET.get('mark_read') == 'true':
        Message.objects.filter(chat=chat, sender__in=chat.participants.exclude(id=user.id), is_delivered=True, is_read=False).update(is_read=True)
    
    all_messages = chat.messages.filter(id__gt=last_id).order_by('created_at')
    data = []
    local_tz = pytz.timezone('Europe/Moscow')
    for msg in all_messages:
        local_time = msg.created_at.astimezone(local_tz)
        file_url = None
        if msg.file:
            file_url = msg.file.url
        data.append({
            'id': msg.id,
            'text': msg.text,
            'file': file_url,
            'filename': msg.display_filename,
            'time': local_time.strftime('%H:%M'),
            'created_at': msg.created_at.isoformat(),
            'sender_id': msg.sender.id,
            'is_read': msg.is_read,
            'is_delivered': msg.is_delivered,
            'reply_to': {
                'id': msg.reply_to.id,
                'text': msg.reply_to.text,
                'sender_name': msg.reply_to.sender.get_full_name()
            } if msg.reply_to else None,
            'forwarded_from': msg.forwarded_from.id if msg.forwarded_from else None,
            'reactions': msg.reactions
        })
    return JsonResponse({'messages': data})

def api_delete_chat_for_me(request, chat_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    user = Autoriz.objects.get(id=request.session['user_id'])
    chat = get_object_or_404(Chat, id=chat_id, participants=user)
    chat.participants.remove(user)
    if chat.participants.count() == 0:
        chat.delete()
    return JsonResponse({'success': True})

def api_delete_chat_for_both(request, chat_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    user = Autoriz.objects.get(id=request.session['user_id'])
    chat = get_object_or_404(Chat, id=chat_id, participants=user)
    chat.delete()
    return JsonResponse({'success': True})

def api_chat_order(request):
    if request.method != 'POST' or 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    data = json.loads(request.body)
    order = data.get('order', [])
    request.session['chat_order'] = order
    return JsonResponse({'success': True})

def api_user_profile(request, user_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    current_user = Autoriz.objects.get(id=request.session['user_id'])
    target_user = get_object_or_404(Autoriz, id=user_id)
    
    chat_profile, _ = ChatProfile.objects.get_or_create(user=target_user)
    
    role = 'user'
    student_info = None
    try:
        student = Student.objects.get(autoriz=target_user)
        role = 'student'
        student_info = {
            'group': student.group.name if student.group else None,
            'course': student.group.course.number if student.group else None,
            'direction': student.group.direction.name if student.group else None,
        }
    except Student.DoesNotExist:
        try:
            professor = Professor.objects.get(autoriz=target_user)
            role = 'professor'
        except Professor.DoesNotExist:
            try:
                staff = AcademicStaff.objects.get(autoriz=target_user)
                role = 'staff'
            except AcademicStaff.DoesNotExist:
                pass
    
    data = {
        'id': target_user.id,
        'full_name': target_user.get_full_name(),
        'birth_date': target_user.birth_date.strftime('%d.%m.%Y') if target_user.birth_date else None,
        'gender': target_user.get_gender_display(),
        'phone': target_user.phone if not target_user.hide_phone else None,
        'interests': chat_profile.interests,
        'avatar': chat_profile.avatar.url if chat_profile.avatar else None,
        'about': chat_profile.about,
        'city': chat_profile.city,
        'is_self': target_user.id == current_user.id,
        'role': role,
        'student_info': student_info,
    }
    
    return JsonResponse(data)

def api_chat_participant(request, chat_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    user = Autoriz.objects.get(id=request.session['user_id'])
    chat = get_object_or_404(Chat, id=chat_id, participants=user)
    other = chat.participants.exclude(id=user.id).first()
    if other:
        role = 'Пользователь'
        try:
            Student.objects.get(autoriz=other)
            role = 'Студент'
        except Student.DoesNotExist:
            try:
                Professor.objects.get(autoriz=other)
                role = 'Преподаватель'
            except Professor.DoesNotExist:
                try:
                    AcademicStaff.objects.get(autoriz=other)
                    role = 'Учебная часть'
                except AcademicStaff.DoesNotExist:
                    pass
        return JsonResponse({'user_id': other.id, 'role': role})
    return JsonResponse({'error': 'no participant'}, status=404)

def api_schedule(request, group_id):
    offset = int(request.GET.get('offset', 0))
    
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Group not found'})
    
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    target_week_start = week_start + timedelta(weeks=offset)
    
    schedule = Schedule.objects.filter(
        group=group,
        week_start_date=target_week_start,
        is_active=True
    ).first()
    
    schedules_data = []
    if schedule:
        daily_schedules = DailySchedule.objects.filter(schedule=schedule).select_related('pair', 'pair__subject', 'pair__professor', 'pair__classroom')
        for ds in daily_schedules:
            schedules_data.append({
                'weekday': ds.weekday,
                'pair_order': ds.pair_order,
                'pair_time': ds.pair.get_pair_number_display(),
                'subject': ds.pair.subject.name_subject,
                'professor': str(ds.pair.professor),
                'classroom': ds.pair.classroom.name_classroom if ds.pair.classroom else None
            })
    
    dates = {}
    for i in range(7):
        current_date = target_week_start + timedelta(days=i)
        dates[i + 1] = current_date.strftime('%d.%m.%y')
    
    return JsonResponse({
        'success': True,
        'schedules': schedules_data,
        'dates': dates,
        'week_start': target_week_start.strftime('%d.%m.%Y'),
        'week_end': (target_week_start + timedelta(days=6)).strftime('%d.%m.%Y')
    })

@csrf_exempt
def forward_message(request):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    user = Autoriz.objects.get(id=request.session['user_id'])
    data = json.loads(request.body)
    message_id = data.get('message_id')
    target_chat_id = data.get('chat_id')
    
    if not message_id or not target_chat_id:
        return JsonResponse({'error': 'missing parameters'}, status=400)
    
    original_msg = get_object_or_404(Message, id=message_id)
    target_chat = get_object_or_404(Chat, id=target_chat_id, participants=user)
    
    new_msg = Message.objects.create(
        chat=target_chat,
        sender=user,
        text=original_msg.text,
        file=original_msg.file,
        original_filename=original_msg.original_filename,
        forwarded_from=original_msg,
        is_delivered=False,
        is_read=False
    )
    
    return JsonResponse({'success': True, 'message_id': new_msg.id})

@csrf_exempt
def add_reaction(request, message_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    user = Autoriz.objects.get(id=request.session['user_id'])
    msg = get_object_or_404(Message, id=message_id)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        new_emoji = data.get('emoji')
    except:
        return JsonResponse({'error': 'invalid json'}, status=400)
    
    if not new_emoji:
        return JsonResponse({'error': 'no emoji'}, status=400)
    
    reactions = msg.reactions if msg.reactions else {}
    
    current_user_emoji = None
    for emoji, users in reactions.items():
        if user.id in users:
            current_user_emoji = emoji
            break
    
    if current_user_emoji == new_emoji:
        reactions[current_user_emoji].remove(user.id)
        if not reactions[current_user_emoji]:
            del reactions[current_user_emoji]
    else:
        if current_user_emoji:
            reactions[current_user_emoji].remove(user.id)
            if not reactions[current_user_emoji]:
                del reactions[current_user_emoji]
        
        if new_emoji not in reactions:
            reactions[new_emoji] = []
        
        if user.id not in reactions[new_emoji]:
            reactions[new_emoji].append(user.id)
    
    msg.reactions = reactions
    msg.save()
    
    return JsonResponse({'success': True, 'reactions': reactions})

def unread_counts(request):
    if 'user_id' not in request.session:
        return JsonResponse({}, status=401)
    
    user = Autoriz.objects.get(id=request.session['user_id'])
    chats = Chat.objects.filter(participants=user)
    counts = {}
    
    for chat in chats:
        unread = Message.objects.filter(chat=chat, sender__in=chat.participants.exclude(id=user.id), is_read=False).count()
        counts[chat.id] = unread
    
    return JsonResponse(counts)

def profile_settings_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    chat_profile, _ = ChatProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user.birth_date = request.POST.get('birth_date') or None
        user.gender = request.POST.get('gender', '')
        user.phone = request.POST.get('phone', '')
        user.hide_phone = request.POST.get('hide_phone') == 'on'
        user.save()
        
        if request.FILES.get('avatar'):
            chat_profile.avatar = request.FILES['avatar']
        chat_profile.interests = request.POST.get('interests', '')
        chat_profile.about = request.POST.get('about', '')
        chat_profile.city = request.POST.get('city', '')
        chat_profile.save()
        
        return redirect('profile_settings_view')
    
    context['chat_profile'] = chat_profile
    return render(request, 'profile_settings.html', context)

def saved_messages_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    context['saved_messages'] = Message.objects.filter(sender=user, is_saved=True).order_by('-created_at')
    
    return render(request, 'saved_messages.html', context)

def archived_chats_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    archived = request.session.get('archived_chats', [])
    context['archived_chats'] = Chat.objects.filter(id__in=archived, participants=user)
    
    return render(request, 'archived_chats.html', context)

def my_stories_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    stories = []
    try:
        student = Student.objects.get(autoriz=user)
        stories = Story.objects.filter(student=student, expires_at__gt=timezone.now()).order_by('-created_at')
    except Student.DoesNotExist:
        pass
    
    context['stories'] = stories
    return render(request, 'my_stories.html', context)

def contacts_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    contacts = []
    for u in Autoriz.objects.exclude(id=user.id):
        full_name = u.get_full_name()
        initials = full_name[0].upper() if full_name else u.user[0].upper()
        chat = Chat.objects.filter(participants=user).filter(participants=u).first()
        contacts.append({
            'id': u.id,
            'full_name': full_name,
            'initials': initials,
            'has_chat': chat is not None,
            'chat_id': chat.id if chat else None,
        })
    
    context['contacts'] = contacts
    return render(request, 'contacts.html', context)

def wallet_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    topcoins = 0
    topgems = 0
    topmoney = 0
    transactions = []
    try:
        student = Student.objects.get(autoriz=user)
        balance = balance_topcoins_and_topgems.objects.filter(student=student).first()
        if balance:
            topcoins = balance.topcoins
            topgems = balance.topgems
        topmoney_obj = Topmoney_student.objects.filter(student=student).first()
        if topmoney_obj:
            topmoney = topmoney_obj.topmoney
        rewards = UserReward.objects.filter(student=student).order_by('-awarded_at')[:10]
        for reward in rewards:
            transactions.append({
                'name': f'Reward: {reward.reward.name}',
                'date': reward.awarded_at.strftime('%d.%m.%Y'),
                'amount': reward.topcoins_given,
                'type': 'coins'
            })
    except Student.DoesNotExist:
        pass
    
    context['topcoins'] = topcoins
    context['topgems'] = topgems
    context['topmoney'] = topmoney
    context['transactions'] = transactions[:20]
    
    return render(request, 'wallet.html', context)

def settings_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    return render(request, 'settings.html', context)

@csrf_exempt
def api_create_story(request):
    if request.method != 'POST' or 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        student = Student.objects.get(autoriz=user)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'not student'}, status=400)
    
    file = request.FILES.get('file')
    caption = request.POST.get('caption', '')
    is_video = file.content_type.startswith('video/') if file else False
    
    if file:
        story = Story.objects.create(
            student=student,
            file=file,
            caption=caption,
            is_video=is_video
        )
        return JsonResponse({
            'success': True,
            'story_id': story.id,
            'file_url': story.file.url
        })
    
    return JsonResponse({'error': 'no file'}, status=400)

@csrf_exempt
def api_delete_story(request, story_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        student = Student.objects.get(autoriz=user)
        story = Story.objects.get(id=story_id, student=student)
        story.delete()
        return JsonResponse({'success': True})
    except (Student.DoesNotExist, Story.DoesNotExist):
        return JsonResponse({'error': 'not found'}, status=404)

def api_message_info(request, message_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    msg = get_object_or_404(Message, id=message_id)
    
    return JsonResponse({
        'id': msg.id,
        'text': msg.text,
        'forwarded_from_user_id': msg.forwarded_from.sender.id if msg.forwarded_from else None,
        'forwarded_from_user_name': msg.forwarded_from.sender.get_full_name() if msg.forwarded_from else None,
    })

def api_groups_by_course(request, course_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    groups = Group.objects.filter(course_id=course_id).values('id', 'name')
    return JsonResponse({'groups': list(groups)})

def api_schedule_professor(request):
    offset = int(request.GET.get('offset', 0))
    
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    user = Autoriz.objects.get(id=request.session['user_id'])
    
    try:
        professor = Professor.objects.get(autoriz=user)
    except Professor.DoesNotExist:
        return JsonResponse({'error': 'not professor'}, status=400)
    
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    target_week_start = week_start + timedelta(weeks=offset)
    
    schedules_data = []
    
    daily_schedules = DailySchedule.objects.filter(
        pair__professor=professor,
        schedule__week_start_date=target_week_start,
        schedule__is_active=True
    ).select_related('pair', 'pair__subject', 'pair__classroom', 'group', 'schedule')
    
    for ds in daily_schedules:
        schedules_data.append({
            'weekday': ds.weekday,
            'pair_order': ds.pair_order,
            'pair_time': ds.pair.get_pair_number_display(),
            'subject': ds.pair.subject.name_subject,
            'professor': str(ds.pair.professor),
            'classroom': ds.pair.classroom.name_classroom if ds.pair.classroom else None,
            'group': ds.group.name
        })
    
    dates = {}
    for i in range(7):
        current_date = target_week_start + timedelta(days=i)
        dates[i + 1] = current_date.strftime('%d.%m')
    
    return JsonResponse({
        'success': True,
        'schedules': schedules_data,
        'dates': dates,
        'week_start': target_week_start.strftime('%d.%m.%Y'),
        'week_end': (target_week_start + timedelta(days=6)).strftime('%d.%m.%Y')
    })

def api_professor_today_pairs(request):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    user = Autoriz.objects.get(id=request.session['user_id'])
    
    try:
        professor = Professor.objects.get(autoriz=user)
    except Professor.DoesNotExist:
        return JsonResponse({'error': 'not professor'}, status=400)
    
    today = timezone.now().date()
    weekday = today.isoweekday()
    
    schedules = Schedule.objects.filter(is_active=True)
    today_pairs = []
    
    for schedule in schedules:
        daily = DailySchedule.objects.filter(
            schedule=schedule,
            weekday=weekday,
            pair__professor=professor
        ).select_related('pair', 'pair__subject', 'pair__classroom', 'group').first()
        
        if daily:
            pair_info = {
                'id': daily.id,
                'pair_number': daily.pair_order,
                'time_start': daily.pair.get_pair_number_display().split('-')[0],
                'time_end': daily.pair.get_pair_number_display().split('-')[1],
                'subject': daily.pair.subject.name_subject,
                'group': daily.group.name,
                'classroom': daily.pair.classroom.name_classroom if daily.pair.classroom else None,
                'is_completed': False,
                'is_cancelled': False
            }
            
            if hasattr(daily, 'attendance_meta'):
                pair_info['is_completed'] = daily.attendance_meta.get('is_completed', False)
                pair_info['is_cancelled'] = daily.attendance_meta.get('is_cancelled', False)
                pair_info['topic'] = daily.attendance_meta.get('topic', '')
            
            today_pairs.append(pair_info)
    
    return JsonResponse({'success': True, 'pairs': today_pairs, 'date': today.strftime('%d.%m.%Y')})

def api_attendance_students(request, pair_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    group_name = request.GET.get('group')
    
    try:
        group = Group.objects.get(name=group_name)
        students = Student.objects.filter(group=group).order_by('surname')
        
        students_data = []
        for student in students:
            students_data.append({
                'id': student.id,
                'full_name': f"{student.surname} {student.name} {student.patronymic}",
                'initials': f"{student.surname[0]}{student.name[0]}"
            })
        
        return JsonResponse({'success': True, 'students': students_data})
    except Group.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Group not found'})

def api_attendance_save(request, pair_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    data = json.loads(request.body)
    students = data.get('students', [])
    topic = data.get('topic', '')
    complete = data.get('complete', False)
    
    for student_data in students:
        attendance, created = Attendance.objects.update_or_create(
            student_id=student_data['id'],
            data_created=timezone.now().date(),
            defaults={
                'type': student_data['status'],
                'comment': student_data.get('comment', ''),
                'data_updated': timezone.now().date()
            }
        )
    
    return JsonResponse({'success': True})

@csrf_exempt
def api_attendance_save(request, pair_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    data = json.loads(request.body)
    students = data.get('students', [])
    topic = data.get('topic', '')
    complete = data.get('complete', False)
    
    for student_data in students:
        attendance, created = Attendance.objects.update_or_create(
            student_id=student_data['id'],
            data_created=timezone.now().date(),
            defaults={
                'type': student_data['status'],
                'comment': student_data.get('comment', ''),
                'data_updated': timezone.now().date()
            }
        )
    
    try:
        daily = DailySchedule.objects.get(id=pair_id)
        daily.topic = topic
        if complete:
            daily.is_completed = True
            daily.is_missed = False
        daily.save()
    except DailySchedule.DoesNotExist:
        pass
    
    return JsonResponse({'success': True})

@csrf_exempt
def api_attendance_save(request, pair_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    data = json.loads(request.body)
    students = data.get('students', [])
    topic = data.get('topic', '')
    complete = data.get('complete', False)
    
    for student_data in students:
        attendance, created = Attendance.objects.update_or_create(
            student_id=student_data['id'],
            data_created=timezone.now().date(),
            defaults={
                'type': student_data['status'],
                'comment': student_data.get('comment', ''),
                'data_updated': timezone.now().date()
            }
        )
        
        bonus = student_data.get('bonus', 0)
        if bonus > 0:
            try:
                student = Student.objects.get(id=student_data['id'])
                balance, _ = balance_topcoins_and_topgems.objects.get_or_create(
                    student=student,
                    defaults={'topcoins': 0, 'topgems': 0}
                )
                balance.topcoins += bonus
                balance.save()
                update_topmoney_for_student(student)
            except Student.DoesNotExist:
                pass
    
    try:
        daily = DailySchedule.objects.get(id=pair_id)
        daily.topic = topic
        if complete:
            daily.is_completed = True
            daily.is_missed = False
        daily.save()
        return JsonResponse({'success': True})
    except DailySchedule.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pair not found'})

@csrf_exempt
def api_attendance_miss_pair(request, pair_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    try:
        daily = DailySchedule.objects.get(id=pair_id)
        daily.is_missed = True
        daily.is_completed = False
        daily.save()
        return JsonResponse({'success': True})
    except DailySchedule.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pair not found'})

def api_attendance_pair_get(request, pair_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    try:
        daily = DailySchedule.objects.get(id=pair_id)
        
        attendances = Attendance.objects.filter(data_created=timezone.now().date())
        
        students_data = {}
        for att in attendances:
            students_data[att.student_id] = {
                'status': att.type,
                'comment': att.comment or ''
            }
        
        return JsonResponse({
            'success': True,
            'topic': daily.topic or '',
            'students': students_data,
            'is_completed': daily.is_completed,
            'is_missed': daily.is_missed
        })
    except DailySchedule.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pair not found'})
    
def student_reviews_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    context = get_user_context(request)
    user = context.get('user')
    
    try:
        student = Student.objects.get(autoriz=user)
        reviews = Student_Reviews.objects.filter(student=student).order_by('-date')
        
        context['reviews'] = reviews
        context['reviews_count'] = reviews.count()
        context['professors_count'] = reviews.values('professor').distinct().count()
        context['last_review_date'] = reviews.first().date.strftime('%d.%m.%Y') if reviews.exists() else None
        context['subjects'] = Subjects.objects.all()
        context['user_role'] = 'student'
        
    except Student.DoesNotExist:
        return redirect('main_view')
    
    return render(request, 'my_reviews.html', context)

@csrf_exempt
def api_add_bonus(request):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id')
        bonus = data.get('bonus', 0)
        
        if not student_id or bonus <= 0:
            return JsonResponse({'success': False, 'error': 'Invalid data'})
        
        student = Student.objects.get(id=student_id)
        balance, created = balance_topcoins_and_topgems.objects.get_or_create(
            student=student,
            defaults={'topcoins': 0, 'topgems': 0}
        )
        balance.topcoins += bonus
        balance.save()
        
        update_topmoney_for_student(student)
        
        return JsonResponse({'success': True, 'new_balance': balance.topcoins})
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def check_homework_bonuses():
    today = date.today()
    
    expired_penalties = {}
    
    all_homeworks = Add_HW_Professor_to_course.objects.all()
    
    for hw in all_homeworks:
        submissions = HomeworkSubmission.objects.filter(homework=hw)
        
        for submission in submissions:
            student = submission.student
            balance, _ = balance_topcoins_and_topgems.objects.get_or_create(
                student=student,
                defaults={'topcoins': 0, 'topgems': 0}
            )
            
            if submission.submitted_at.date() <= hw.date_final and not submission.bonus_received and not submission.is_checked:
                balance.topcoins += 5
                balance.topgems += 1
                balance.save()
                submission.bonus_received = True
                submission.save()
                update_topmoney_for_student(student)
                print(f"Бонус начислен студенту {student} за ДЗ по {hw.subject.name_subject}")
            
            if submission.submitted_at.date() > hw.date_final and not submission.is_checked:
                days_overdue = (today - hw.date_final).days
                if days_overdue > 0:
                    penalty = days_overdue
                    if balance.topcoins >= penalty:
                        balance.topcoins -= penalty
                        balance.save()
                        update_topmoney_for_student(student)
                        print(f"Списано {penalty} топкоинов со студента {student} за просрочку ДЗ по {hw.subject.name_subject}")
                    else:
                        balance.topcoins = 0
                        balance.save()
                        update_topmoney_for_student(student)
                        print(f"Баланс обнулён у студента {student} за просрочку ДЗ по {hw.subject.name_subject}")