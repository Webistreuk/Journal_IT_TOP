from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from .models import Autoriz, Subjects, Student, Professor, AcademicStaff, Group, Add_HW_Professor_to_course, HomeworkSubmission, Attendance, Estimation, balance_topcoins_and_topgems, Shop_add_products, PaymentInfo, Announcement, Event, Poll, PollOption, PollVote, Chat, Message, Schedule, DailySchedule, Pair, LessonType, Add_Сlassroom, Semester, Vacation, ScheduleReplacement, LeaderboardEntry, Ranking, StudentStats, Reward, UserReward, AcademicDebt, GraduationWork, Internship, EducationalMaterial, PersonalAccount, Review_of_the_Academy, Appeals_to_the_educational_unit, Complaint_to_the_CEO, Student_Reviews, Exam, ExamSession, ScheduledExam, Topmoney_student, Type_work, Course, Direction, AcademicYear, image_student, image_professor, Students_payment_account, All_payment_of_education, Notification, Debtor, Scholarship, ChatProfile, Story
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json
import pytz
import os

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
    try:
        user = Autoriz.objects.get(id=request.session['user_id'])
    except Autoriz.DoesNotExist:
        return redirect('autoriz_view')
    context = {'user': user}
    try:
        student = Student.objects.get(autoriz=user)
        context['student'] = student
        context['user_role'] = 'student'
        context['balance'] = getattr(student, 'balance_topcoins_and_topgems', None)
        context['announcements'] = Announcement.objects.filter(Q(is_for_all=True) | Q(groups=student.group)).distinct()[:5]
        context['homeworks'] = Add_HW_Professor_to_course.objects.filter(group=student.group).order_by('-date_start')[:5]
        context['events'] = Event.objects.filter(Q(is_for_all=True) | Q(groups=student.group), start_date__gte=timezone.now()).order_by('start_date')[:5]
        context['polls'] = Poll.objects.filter(Q(is_active=True), Q(groups=student.group) | Q(groups__isnull=True), start_date__lte=timezone.now(), end_date__gte=timezone.now()).distinct()
    except Student.DoesNotExist:
        try:
            professor = Professor.objects.get(autoriz=user)
            context['professor'] = professor
            context['user_role'] = 'professor'
            context['unchecked_homeworks'] = HomeworkSubmission.objects.filter(homework__professor=professor, is_checked=False).count()
            context['my_subjects'] = Subjects.objects.filter(professor=professor)
        except Professor.DoesNotExist:
            try:
                staff = AcademicStaff.objects.get(autoriz=user)
                context['staff'] = staff
                context['user_role'] = 'academic_staff'
                context['pending_payments'] = PaymentInfo.objects.filter(period_end__gte=timezone.now().date()).count()
                context['total_students'] = Student.objects.count()
                context['total_professors'] = Professor.objects.count()
            except AcademicStaff.DoesNotExist:
                context['user_role'] = 'unknown'
    return render(request, 'main.html', context)

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('autoriz_view')

def profile_edit_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
    
    return render(request, 'profile_edit.html', {
        'user': user,
        'chat_profile': chat_profile
    })

def homework_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    user = Autoriz.objects.get(id=request.session['user_id'])
    
    try:
        student = Student.objects.get(autoriz=user)
        homeworks = Add_HW_Professor_to_course.objects.filter(group=student.group).order_by('-date_start')
        
        homework_data = []
        for hw in homeworks:
            try:
                submission = HomeworkSubmission.objects.get(homework=hw, student=student)
                homework_data.append({
                    'homework': hw,
                    'submission': submission,
                    'has_submission': True,
                    'is_checked': submission.is_checked
                })
            except HomeworkSubmission.DoesNotExist:
                homework_data.append({
                    'homework': hw,
                    'submission': None,
                    'has_submission': False,
                    'is_checked': False
                })
        
        return render(request, 'homework_list.html', {
            'homework_data': homework_data,
            'user': user
        })
    except Student.DoesNotExist:
        return redirect('main_view')

def homework_add_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
        return render(request, 'homework_add.html', {'form': form, 'user': user})
    except Professor.DoesNotExist:
        return redirect('main_view')

def homework_submit_view(request, homework_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    homework = get_object_or_404(Add_HW_Professor_to_course, id=homework_id)
    user = Autoriz.objects.get(id=request.session['user_id'])
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
        return render(request, 'homework_submit.html', {'form': form, 'homework': homework, 'user': user})
    except Student.DoesNotExist:
        return redirect('main_view')

def homework_check_view(request, submission_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    submission = get_object_or_404(HomeworkSubmission, id=submission_id)
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        professor = Professor.objects.get(autoriz=user)
        if submission.homework.professor != professor:
            return redirect('homework_list_view')
        if request.method == 'POST':
            form = HomeworkGradeForm(request.POST, instance=submission)
            if form.is_valid():
                form.save()
                messages.success(request, 'Оценка выставлена')
                return redirect('homework_list_view')
        else:
            form = HomeworkGradeForm(instance=submission)
        return render(request, 'homework_check.html', {'form': form, 'submission': submission, 'user': user})
    except Professor.DoesNotExist:
        return redirect('main_view')

def schedule_view(request, group_id=None):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        student = Student.objects.get(autoriz=user)
        group = student.group if not group_id else get_object_or_404(Group, id=group_id)
    except Student.DoesNotExist:
        try:
            if hasattr(user, 'professor') or hasattr(user, 'academicstaff'):
                group = get_object_or_404(Group, id=group_id) if group_id else None
            else:
                return redirect('main_view')
        except:
            return redirect('main_view')
    if not group:
        return redirect('main_view')
    schedules = Schedule.objects.filter(group=group, is_active=True).order_by('-week_start_date')
    weekdays = [(1, 'Пн'), (2, 'Вт'), (3, 'Ср'), (4, 'Чт'), (5, 'Пт'), (6, 'Сб'), (7, 'Вс')]
    return render(request, 'schedule.html', {'schedules': schedules, 'group': group, 'user': user, 'weekdays': weekdays})

def schedule_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if not hasattr(user, 'academicstaff') and not hasattr(user, 'professor'):
        return redirect('main_view')
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Расписание создано')
            return redirect('schedule_view')
    else:
        form = ScheduleForm()
    subjects = Subjects.objects.all()
    professors = Professor.objects.all()
    classrooms = Add_Сlassroom.objects.all()
    return render(request, 'schedule_create.html', {'form': form, 'user': user, 'subjects': subjects, 'professors': professors, 'classrooms': classrooms})

def daily_schedule_add_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = DailyScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Занятие добавлено в расписание')
            return redirect('schedule_view')
    else:
        form = DailyScheduleForm()
    return render(request, 'daily_schedule_add.html', {'form': form, 'user': user})

def pair_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = PairForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пара создана')
            return redirect('pair_list_view')
    else:
        form = PairForm()
    return render(request, 'pair_create.html', {'form': form, 'user': user})

def pair_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    pairs = Pair.objects.all().order_by('pair_number')
    return render(request, 'pair_list.html', {'pairs': pairs, 'user': user})

def lesson_type_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = LessonTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип занятия создан')
            return redirect('lesson_type_list_view')
    else:
        form = LessonTypeForm()
    return render(request, 'lesson_type_create.html', {'form': form, 'user': user})

def lesson_type_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    lesson_types = LessonType.objects.all()
    return render(request, 'lesson_type_list.html', {'lesson_types': lesson_types, 'user': user})

def add_classroom_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = AddClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аудитория добавлена')
            return redirect('classroom_list_view')
    else:
        form = AddClassroomForm()
    return render(request, 'add_classroom.html', {'form': form, 'user': user})

def classroom_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    classrooms = Add_Сlassroom.objects.all()
    return render(request, 'classroom_list.html', {'classrooms': classrooms, 'user': user})

def semester_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Семестр создан')
            return redirect('semester_list_view')
    else:
        form = SemesterForm()
    return render(request, 'semester_create.html', {'form': form, 'user': user})

def semester_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    semesters = Semester.objects.all().order_by('-start_date')
    return render(request, 'semester_list.html', {'semesters': semesters, 'user': user})

def vacation_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = VacationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Каникулы добавлены')
            return redirect('vacation_list_view')
    else:
        form = VacationForm()
    return render(request, 'vacation_create.html', {'form': form, 'user': user})

def vacation_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    vacations = Vacation.objects.all().order_by('start_date')
    return render(request, 'vacation_list.html', {'vacations': vacations, 'user': user})

def schedule_replacement_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = ScheduleReplacementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Замена создана')
            return redirect('schedule_replacement_list_view')
    else:
        form = ScheduleReplacementForm()
    return render(request, 'schedule_replacement_create.html', {'form': form, 'user': user})

def schedule_replacement_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    replacements = ScheduleReplacement.objects.all().order_by('-created_at')
    return render(request, 'schedule_replacement_list.html', {'replacements': replacements, 'user': user})

def attendance_mark_view(request, schedule_id=None):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        professor = Professor.objects.get(autoriz=user)
        schedules = Schedule.objects.filter(is_active=True)
        selected_schedule = None
        students = []
        if schedule_id:
            selected_schedule = get_object_or_404(Schedule, id=schedule_id)
            students = selected_schedule.group.student_set.all()
        if request.method == 'POST':
            sid = request.POST.get('schedule_id')
            if sid:
                selected_schedule = get_object_or_404(Schedule, id=sid)
                students = selected_schedule.group.student_set.all()
                for student in students:
                    type_val = request.POST.get(f'attendance_{student.id}')
                    if type_val:
                        Attendance.objects.update_or_create(
                            student=student,
                            schedule=selected_schedule,
                            defaults={'type': type_val, 'data_updated': timezone.now().date()}
                        )
                messages.success(request, 'Посещаемость сохранена')
                return redirect('attendance_mark_view')
        return render(request, 'attendance_mark.html', {
            'schedules': schedules,
            'selected_schedule': selected_schedule,
            'students': students,
            'user': user
        })
    except Professor.DoesNotExist:
        return redirect('main_view')

def attendance_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        student = Student.objects.get(autoriz=user)
        attendances = Attendance.objects.filter(student=student).order_by('-data_created')
        present_count = attendances.filter(type='presence').count()
        late_count = attendances.filter(type='late').count()
        absent_count = attendances.filter(type='absence').count()
        subjects = Subjects.objects.all()
        return render(request, 'attendance_list.html', {
            'attendances': attendances,
            'present_count': present_count,
            'late_count': late_count,
            'absent_count': absent_count,
            'total_count': attendances.count(),
            'user': user,
            'subjects': subjects
        })
    except Student.DoesNotExist:
        return redirect('main_view')

def estimation_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        professor = Professor.objects.get(autoriz=user)
        if request.method == 'POST':
            form = EstimationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Оценка выставлена')
                return redirect('estimation_view')
        else:
            form = EstimationForm()
        estimations = Estimation.objects.filter(subject__in=professor.leads_the_subject.all()).order_by('-date')
        return render(request, 'estimation.html', {'form': form, 'estimations': estimations, 'user': user})
    except Professor.DoesNotExist:
        try:
            student = Student.objects.get(autoriz=user)
            estimations = Estimation.objects.filter(student=student).order_by('-date')
            return render(request, 'student_estimations.html', {'estimations': estimations, 'user': user})
        except Student.DoesNotExist:
            return redirect('main_view')

def shop_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    products = Shop_add_products.objects.all()
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        student = Student.objects.get(autoriz=user)
        balance = getattr(student, 'balance_topcoins_and_topgems', None)
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Shop_add_products, id=product_id)
            if balance and balance.topcoins >= product.price_product_topcoins:
                balance.topcoins -= product.price_product_topcoins
                balance.save()
                messages.success(request, f'Куплено {product.name_product}')
            else:
                messages.error(request, 'Недостаточно топкоинов')
            return redirect('shop_view')
        return render(request, 'shop.html', {'products': products, 'balance': balance, 'user': user})
    except Student.DoesNotExist:
        return render(request, 'shop.html', {'products': products, 'balance': None, 'user': user})

def shop_product_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = ShopProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар добавлен в магазин')
            return redirect('shop_view')
    else:
        form = ShopProductForm()
    return render(request, 'shop_product_create.html', {'form': form, 'user': user})

def leaderboard_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    entries = LeaderboardEntry.objects.filter(semester__is_active=True).order_by('rank_in_group')[:50]
    return render(request, 'leaderboard.html', {'entries': entries, 'user': user})

def polls_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
    return render(request, 'polls.html', {'polls': polls, 'user': user})

def poll_detail_view(request, poll_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    poll = get_object_or_404(Poll, id=poll_id)
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        option_id = request.POST.get('option')
        option = get_object_or_404(PollOption, id=option_id)
        PollVote.objects.get_or_create(poll=poll, user=user, defaults={'option': option})
        messages.success(request, 'Голос учтён')
        return redirect('polls_view')
    options = poll.options.all()
    user_vote = PollVote.objects.filter(poll=poll, user=user).first()
    total_votes = sum(opt.votes for opt in options)
    return render(request, 'poll_detail.html', {
        'poll': poll,
        'options': options,
        'user_vote': user_vote,
        'total_votes': total_votes,
        'user': user
    })

def poll_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save()
            messages.success(request, 'Опрос создан. Теперь добавьте варианты ответов.')
            return redirect('poll_option_add_view', poll_id=poll.id)
    else:
        form = PollForm()
    return render(request, 'poll_create.html', {'form': form, 'user': user})

def poll_option_add_view(request, poll_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
    options = poll.options.all()
    return render(request, 'poll_option_add.html', {'form': form, 'poll': poll, 'options': options, 'user': user})

def announcements_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        student = Student.objects.get(autoriz=user)
        announcements = Announcement.objects.filter(
            Q(is_for_all=True) | Q(groups=student.group)
        ).distinct().order_by('-date_added')
    except Student.DoesNotExist:
        announcements = Announcement.objects.all().order_by('-date_added')
    return render(request, 'announcements.html', {'announcements': announcements, 'user': user})

def announcement_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление создано')
            return redirect('announcements_view')
    else:
        form = AnnouncementForm()
    groups = Group.objects.all()
    return render(request, 'announcement_create.html', {'form': form, 'groups': groups, 'user': user})

def events_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        student = Student.objects.get(autoriz=user)
        events = Event.objects.filter(
            Q(is_for_all=True) | Q(groups=student.group),
            start_date__gte=timezone.now()
        ).order_by('start_date')
    except Student.DoesNotExist:
        events = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')
    return render(request, 'events.html', {'events': events, 'user': user})

def event_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Событие создано')
            return redirect('events_view')
    else:
        form = EventForm()
    groups = Group.objects.all()
    return render(request, 'event_create.html', {'form': form, 'groups': groups, 'user': user})

def payment_info_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
    return render(request, 'payment_info.html', {
        'form': form,
        'payments': payments,
        'total_paid': total_paid,
        'monthly_paid': monthly_paid,
        'user': user
    })

def educational_materials_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        student = Student.objects.get(autoriz=user)
        materials = EducationalMaterial.objects.filter(
            Q(is_public=True) | Q(groups=student.group)
        ).distinct().order_by('-upload_date')
    except Student.DoesNotExist:
        try:
            professor = Professor.objects.get(autoriz=user)
            materials = EducationalMaterial.objects.filter(professor=professor).order_by('-upload_date')
        except Professor.DoesNotExist:
            materials = EducationalMaterial.objects.all().order_by('-upload_date')
    subjects = Subjects.objects.all()
    return render(request, 'materials.html', {'materials': materials, 'user': user, 'subjects': subjects})

def educational_material_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
        groups = Group.objects.all()
        subjects = Subjects.objects.all()
        return render(request, 'educational_material_create.html', {
            'form': form,
            'groups': groups,
            'subjects': subjects,
            'user': user
        })
    except Professor.DoesNotExist:
        return redirect('main_view')

def appeal_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
        return render(request, 'appeal.html', {'form': form, 'user': user})
    except Student.DoesNotExist:
        return redirect('main_view')

def review_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
        my_reviews = Review_of_the_Academy.objects.filter(student=student)
        return render(request, 'review.html', {'form': form, 'my_reviews': my_reviews, 'user': user})
    except Student.DoesNotExist:
        return redirect('main_view')

def complaint_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
        return render(request, 'complaint.html', {'form': form, 'user': user})
    except Student.DoesNotExist:
        return redirect('main_view')

def student_review_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    reviews = Student_Reviews.objects.all().order_by('-date')
    groups = Group.objects.all()
    subjects = Subjects.objects.all()
    return render(request, 'student_review_list.html', {
        'reviews': reviews,
        'groups': groups,
        'subjects': subjects,
        'user': user
    })

def student_review_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        professor = Professor.objects.get(autoriz=user)
        if request.method == 'POST':
            form = StudentReviewForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Отзыв о студенте добавлен')
                return redirect('student_review_list_view')
        else:
            form = StudentReviewForm()
        students = Student.objects.all()
        professors = Professor.objects.all()
        subjects = Subjects.objects.all()
        recent_reviews = Student_Reviews.objects.all().order_by('-date')[:5]
        return render(request, 'student_review_create.html', {
            'form': form,
            'students': students,
            'professors': professors,
            'subjects': subjects,
            'recent_reviews': recent_reviews,
            'professor': professor,
            'user': user
        })
    except Professor.DoesNotExist:
        return redirect('main_view')

def chat_list_view(request, chat_id=None):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    user = Autoriz.objects.get(id=request.session['user_id'])
    chats = Chat.objects.filter(participants=user)
    
    selected_chat = None
    messages_list = []
    
    if chat_id:
        selected_chat = get_object_or_404(Chat, id=chat_id, participants=user)
        Message.objects.filter(chat=selected_chat, sender__in=selected_chat.participants.exclude(id=user.id), is_delivered=False).update(is_delivered=True)
        messages_list = selected_chat.messages.all().order_by('created_at')
    
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        delete_id = request.POST.get('delete_id')
        text = request.POST.get('text')
        file = request.FILES.get('file')
        
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
            Message.objects.create(
                chat=selected_chat,
                sender=user,
                text=text or '',
                file=saved_path,
                original_filename=original_filename,
                is_delivered=False,
                is_read=False
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
        'today': today.strftime('%Y-%m-%d'),
        'yesterday': yesterday.strftime('%Y-%m-%d'),
    })

def create_chat_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    
    current_user = Autoriz.objects.get(id=request.session['user_id'])
    
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
    
    return render(request, 'create_chat.html', {
        'users': users_with_details,
        'user': current_user
    })

def exam_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
    return render(request, 'exam_list.html', {
        'exams': exams,
        'passed_count': passed_count,
        'avg_grade': avg_grade,
        'user': user
    })

def exam_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = ExamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Экзамен добавлен')
            return redirect('exam_list_view')
    else:
        form = ExamForm()
    students = Student.objects.all()
    subjects = Subjects.objects.all()
    professors = Professor.objects.all()
    semesters = Semester.objects.all()
    return render(request, 'exam_create.html', {
        'form': form,
        'students': students,
        'subjects': subjects,
        'professors': professors,
        'semesters': semesters,
        'user': user
    })

def exam_session_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = ExamSessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Экзаменационная сессия создана')
            return redirect('exam_session_list_view')
    else:
        form = ExamSessionForm()
    return render(request, 'exam_session_create.html', {'form': form, 'user': user})

def exam_session_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    sessions = ExamSession.objects.all().order_by('-start_date')
    return render(request, 'exam_session_list.html', {'sessions': sessions, 'user': user})

def scheduled_exam_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
    return render(request, 'scheduled_exam_create.html', {'form': form, 'user': user})

def scheduled_exam_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    exams = ScheduledExam.objects.all().order_by('preliminary_date')
    return render(request, 'scheduled_exam_list.html', {'exams': exams, 'user': user})

def academic_debt_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = AcademicDebtForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задолженность добавлена')
            return redirect('academic_debt_list_view')
    else:
        form = AcademicDebtForm()
    return render(request, 'academic_debt_create.html', {'form': form, 'user': user})

def academic_debt_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    debts = AcademicDebt.objects.all().order_by('exam_date')
    return render(request, 'academic_debt_list.html', {'debts': debts, 'user': user})

def graduation_work_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = GraduationWorkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Дипломная работа добавлена')
            return redirect('graduation_work_list_view')
    else:
        form = GraduationWorkForm()
    return render(request, 'graduation_work_create.html', {'form': form, 'user': user})

def graduation_work_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    works = GraduationWork.objects.all().order_by('-defense_date')
    return render(request, 'graduation_work_list.html', {'works': works, 'user': user})

def internship_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = InternshipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Практика добавлена')
            return redirect('internship_list_view')
    else:
        form = InternshipForm()
    return render(request, 'internship_create.html', {'form': form, 'user': user})

def internship_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    internships = Internship.objects.all().order_by('-start_date')
    return render(request, 'internship_list.html', {'internships': internships, 'user': user})

def group_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups, 'user': user})

def group_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Группа создана')
            return redirect('group_list_view')
    else:
        form = GroupForm()
    return render(request, 'group_create.html', {'form': form, 'user': user})

def subject_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    subjects = Subjects.objects.all()
    subjects_with_professors = subjects.filter(professor__isnull=False).count()
    groups = Group.objects.all()
    return render(request, 'subject_list.html', {
        'subjects': subjects,
        'subjects_with_professors': subjects_with_professors,
        'groups': groups,
        'user': user
    })

def subject_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = SubjectsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Предмет добавлен')
            return redirect('subject_list_view')
    else:
        form = SubjectsForm()
    return render(request, 'subject_create.html', {'form': form, 'user': user})

def course_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    courses = Course.objects.all()
    for c in courses:
        c.student_count = Student.objects.filter(group__course=c).count()
    return render(request, 'course_list.html', {'courses': courses, 'user': user})

def course_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс добавлен')
            return redirect('course_list_view')
    else:
        form = CourseForm()
    return render(request, 'course_create.html', {'form': form, 'user': user})

def direction_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    directions = Direction.objects.all()
    for d in directions:
        d.student_count = Student.objects.filter(group__direction=d).count()
    active_directions = directions.filter(group__isnull=False).distinct().count()
    return render(request, 'direction_list.html', {
        'directions': directions,
        'active_directions': active_directions,
        'user': user
    })

def direction_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = DirectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Направление добавлено')
            return redirect('direction_list_view')
    else:
        form = DirectionForm()
    return render(request, 'direction_create.html', {'form': form, 'user': user})

def academic_year_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    years = AcademicYear.objects.all().order_by('-start_date')
    return render(request, 'academic_year_list.html', {'years': years, 'user': user})

def academic_year_create_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Учебный год добавлен')
            return redirect('academic_year_list_view')
    else:
        form = AcademicYearForm()
    return render(request, 'academic_year_create.html', {'form': form, 'user': user})

def notification_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    return render(request, 'notification_list.html', {'notifications': notifications, 'user': user})

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
    user = Autoriz.objects.get(id=request.session['user_id'])
    debtors = Debtor.objects.filter(is_paid=False).order_by('due_date')
    total_debt = sum(d.debt_amount for d in debtors)
    groups = Group.objects.all()
    return render(request, 'debtor_list.html', {
        'debtors': debtors,
        'total_debt': total_debt,
        'groups': groups,
        'user': user
    })

def scholarship_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    scholarships = Scholarship.objects.all().order_by('-month')
    return render(request, 'scholarship_list.html', {'scholarships': scholarships, 'user': user})

def personal_account_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        personal_account = PersonalAccount.objects.get(user=user)
    except PersonalAccount.DoesNotExist:
        personal_account = None
    return render(request, 'personal_account.html', {'personal_account': personal_account, 'user': user})

def personal_account_edit_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
    return render(request, 'personal_account_edit.html', {'form': form, 'user': user})

def student_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students, 'user': user})

def professor_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    professors = Professor.objects.all()
    return render(request, 'professor_list.html', {'professors': professors, 'user': user})

def academic_staff_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    staff = AcademicStaff.objects.all()
    return render(request, 'academic_staff_list.html', {'staff': staff, 'user': user})

def student_detail_view(request, student_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_detail.html', {'student': student, 'user': user})

def professor_detail_view(request, professor_id):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    professor = get_object_or_404(Professor, id=professor_id)
    return render(request, 'professor_detail.html', {'professor': professor, 'user': user})

def balance_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    balances = balance_topcoins_and_topgems.objects.all()
    return render(request, 'balance_list.html', {'balances': balances, 'user': user})

def topmoney_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    topmoney_list = Topmoney_student.objects.all().order_by('-topmoney')
    return render(request, 'topmoney_list.html', {'topmoney_list': topmoney_list, 'user': user})

def ranking_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    rankings = Ranking.objects.filter(semester__is_active=True).order_by('group_rank')[:50]
    return render(request, 'ranking_list.html', {'rankings': rankings, 'user': user})

def reward_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    rewards = Reward.objects.filter(is_active=True)
    return render(request, 'reward_list.html', {'rewards': rewards, 'user': user})

def user_reward_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    try:
        student = Student.objects.get(autoriz=user)
        user_rewards = UserReward.objects.filter(student=student).order_by('-awarded_at')
        total_topcoins = sum(ur.topcoins_given for ur in user_rewards)
        total_topgems = sum(ur.topgems_given for ur in user_rewards)
        return render(request, 'user_reward_list.html', {
            'user_rewards': user_rewards,
            'total_topcoins': total_topcoins,
            'total_topgems': total_topgems,
            'user': user
        })
    except Student.DoesNotExist:
        return redirect('main_view')

def type_work_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    types = Type_work.objects.all()
    return render(request, 'type_work_list.html', {'types': types, 'user': user})

def image_student_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    images = image_student.objects.all()
    return render(request, 'image_student_list.html', {'images': images, 'user': user})

def image_professor_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    images = image_professor.objects.all()
    return render(request, 'image_professor_list.html', {'images': images, 'user': user})

def students_payment_account_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    accounts = Students_payment_account.objects.all()
    return render(request, 'students_payment_account_list.html', {'accounts': accounts, 'user': user})

def all_payment_of_education_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    payments = All_payment_of_education.objects.all()
    return render(request, 'all_payment_of_education_list.html', {'payments': payments, 'user': user})

def student_stats_list_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    stats = StudentStats.objects.all()
    return render(request, 'student_stats_list.html', {'stats': stats, 'user': user})

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
            'sender_id': msg.sender.id,
            'is_read': msg.is_read,
            'is_delivered': msg.is_delivered,
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
        'role': None,
        'student_info': None,
    }
    try:
        student = Student.objects.get(autoriz=target_user)
        data['role'] = 'student'
        data['student_info'] = {
            'group': student.group.name if student.group else None,
            'course': student.group.course.number if student.group else None,
            'direction': student.group.direction.name if student.group else None,
        }
    except Student.DoesNotExist:
        try:
            professor = Professor.objects.get(autoriz=target_user)
            data['role'] = 'professor'
        except Professor.DoesNotExist:
            try:
                staff = AcademicStaff.objects.get(autoriz=target_user)
                data['role'] = 'staff'
            except AcademicStaff.DoesNotExist:
                data['role'] = 'user'
    
    return JsonResponse(data)

def api_chat_participant(request, chat_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'unauthorized'}, status=401)
    user = Autoriz.objects.get(id=request.session['user_id'])
    chat = get_object_or_404(Chat, id=chat_id, participants=user)
    other = chat.participants.exclude(id=user.id).first()
    if other:
        return JsonResponse({'user_id': other.id})
    return JsonResponse({'error': 'no participant'}, status=404)

def profile_settings_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
    
    return render(request, 'profile_settings.html', {
        'user': user,
        'chat_profile': chat_profile
    })

def saved_messages_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    saved_messages = Message.objects.filter(sender=user, is_saved=True).order_by('-created_at')
    return render(request, 'saved_messages.html', {'user': user, 'saved_messages': saved_messages})

def archived_chats_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    archived = request.session.get('archived_chats', [])
    archived_chats = Chat.objects.filter(id__in=archived, participants=user)
    return render(request, 'archived_chats.html', {'user': user, 'archived_chats': archived_chats})

def my_stories_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    stories = []
    try:
        student = Student.objects.get(autoriz=user)
        stories = Story.objects.filter(student=student, expires_at__gt=timezone.now()).order_by('-created_at')
    except Student.DoesNotExist:
        pass
    return render(request, 'my_stories.html', {'user': user, 'stories': stories})

def contacts_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
    return render(request, 'contacts.html', {'user': user, 'contacts': contacts})

def wallet_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
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
    return render(request, 'wallet.html', {
        'user': user,
        'topcoins': topcoins,
        'topgems': topgems,
        'topmoney': topmoney,
        'transactions': transactions[:20]
    })

def settings_view(request):
    if 'user_id' not in request.session:
        return redirect('autoriz_view')
    user = Autoriz.objects.get(id=request.session['user_id'])
    return render(request, 'settings.html', {'user': user})

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