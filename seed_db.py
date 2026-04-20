# seed_full_db.py
import os
import django
from datetime import date, timedelta
from random import choice, randint
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.models import (
    Autoriz, Direction, Course, AcademicYear, Group, Subjects, Professor,
    Student, Add_Сlassroom, LessonType, Pair, DailySchedule, Schedule,
    Semester, balance_topcoins_and_topgems, Shop_add_products,
    All_payment_of_education, Announcement, Event, Chat, Message,
    ChatProfile, Student_Reviews, Attendance, Estimation,
    HomeworkSubmission, Add_HW_Professor_to_course, Poll, PollOption,
    PollVote, LeaderboardEntry, Ranking, StudentStats, Reward, UserReward,
    AcademicDebt, GraduationWork, Internship, EducationalMaterial,
    PaymentInfo, Debtor, Scholarship, Notification, Review_of_the_Academy,
    Appeals_to_the_educational_unit, Complaint_to_the_CEO, AcademicStaff,
    Topmoney_student
)
from django.utils import timezone

def create_directions():
    directions = [
        {'code': '09.02.07', 'name': 'Информационные системы и программирование'},
        {'code': '38.02.01', 'name': 'Экономика и бухгалтерский учет'},
        {'code': '40.02.01', 'name': 'Право и организация социального обеспечения'},
        {'code': '13.02.11', 'name': 'Техническая эксплуатация электрического оборудования'},
        {'code': '42.02.01', 'name': 'Реклама'},
        {'code': '54.02.01', 'name': 'Дизайн (по отраслям)'},
        {'code': '43.02.14', 'name': 'Гостиничное дело'},
    ]
    for d in directions:
        Direction.objects.get_or_create(code=d['code'], defaults={'name': d['name']})
    print(f"Создано {Direction.objects.count()} направлений")

def create_courses():
    for i in range(1, 5):
        Course.objects.get_or_create(number=i)
    print(f"Создано {Course.objects.count()} курсов")

def create_academic_years():
    current_year = date.today().year
    years = [
        {'name': f'{current_year-2}-{current_year-1}', 'start_date': date(current_year-2, 9, 1),
         'end_date': date(current_year-1, 8, 31), 'is_current': False},
        {'name': f'{current_year-1}-{current_year}', 'start_date': date(current_year-1, 9, 1),
         'end_date': date(current_year, 8, 31), 'is_current': True},
        {'name': f'{current_year}-{current_year+1}', 'start_date': date(current_year, 9, 1),
         'end_date': date(current_year+1, 8, 31), 'is_current': False},
    ]
    for y in years:
        AcademicYear.objects.get_or_create(name=y['name'], defaults=y)
    print(f"Создано {AcademicYear.objects.count()} учебных годов")

def create_groups():
    groups_data = [
        ('ПРО-11', 1, '09.02.07'), ('ПРО-12', 1, '09.02.07'), ('ПРО-13', 1, '09.02.07'),
        ('ПРО-21', 2, '09.02.07'), ('ПРО-22', 2, '09.02.07'), ('ПРО-31', 3, '09.02.07'),
        ('ПРО-32', 3, '09.02.07'), ('ПРО-41', 4, '09.02.07'), ('ЭК-11', 1, '38.02.01'),
        ('ЭК-12', 1, '38.02.01'), ('ЭК-21', 2, '38.02.01'), ('ЭК-22', 2, '38.02.01'),
        ('ЭК-31', 3, '38.02.01'), ('ПСО-11', 1, '40.02.01'), ('ПСО-21', 2, '40.02.01'),
        ('ПСО-31', 3, '40.02.01'), ('ЭЛ-11', 1, '13.02.11'), ('ЭЛ-21', 2, '13.02.11'),
        ('РК-11', 1, '42.02.01'), ('РК-21', 2, '42.02.01'), ('ДЗ-11', 1, '54.02.01'),
        ('ГД-11', 1, '43.02.14'),
    ]
    academic_year = AcademicYear.objects.filter(is_current=True).first()
    for name, course_num, dir_code in groups_data:
        direction = Direction.objects.get(code=dir_code)
        course = Course.objects.get(number=course_num)
        Group.objects.get_or_create(
            name=name,
            defaults={
                'course': course,
                'direction': direction,
                'academic_year': academic_year.name if academic_year else '2024-2025'
            }
        )
    print(f"Создано {Group.objects.count()} групп")

def create_subjects():
    subjects = [
        'Основы программирования', 'Базы данных', 'Web-разработка',
        'Объектно-ориентированное программирование', 'Операционные системы',
        'Математика', 'Русский язык', 'Английский язык', 'Физика',
        'Экономика', 'Бухгалтерский учет', 'Налоги и налогообложение',
        'Гражданское право', 'Уголовное право', 'Административное право',
        'Электротехника', 'Схемотехника', 'Микропроцессоры',
        'Маркетинг', 'Рекламные технологии', 'Графический дизайн',
        'Web-дизайн', 'Гостиничный менеджмент', 'Правоведение'
    ]
    for subj in subjects:
        Subjects.objects.get_or_create(name_subject=subj)
    print(f"Создано {Subjects.objects.count()} предметов")

def create_users():
    users_data = [
        {'user': 'ivanov_i', 'password': 'ivanov123', 'email': 'i.ivanov@college.ru', 'role': 'professor',
         'name': 'Иван', 'surname': 'Иванов', 'patronymic': 'Петрович', 'subject': 'Основы программирования'},
        {'user': 'petrov_p', 'password': 'petrov123', 'email': 'p.petrov@college.ru', 'role': 'professor',
         'name': 'Петр', 'surname': 'Петров', 'patronymic': 'Сергеевич', 'subject': 'Базы данных'},
        {'user': 'sidorov_s', 'password': 'sidorov123', 'email': 's.sidorov@college.ru', 'role': 'professor',
         'name': 'Сидор', 'surname': 'Сидоров', 'patronymic': 'Алексеевич', 'subject': 'Математика'},
        {'user': 'smirnova_a', 'password': 'smirnova123', 'email': 'a.smirnova@college.ru', 'role': 'professor',
         'name': 'Анна', 'surname': 'Смирнова', 'patronymic': 'Владимировна', 'subject': 'Английский язык'},
        {'user': 'kozlov_d', 'password': 'kozlov123', 'email': 'd.kozlov@college.ru', 'role': 'professor',
         'name': 'Дмитрий', 'surname': 'Козлов', 'patronymic': 'Николаевич', 'subject': 'Экономика'},
        {'user': 'morozova_e', 'password': 'morozova123', 'email': 'e.morozova@college.ru', 'role': 'professor',
         'name': 'Елена', 'surname': 'Морозова', 'patronymic': 'Андреевна', 'subject': 'Web-разработка'},
        {'user': 'volkov_a', 'password': 'volkov123', 'email': 'a.volkov@college.ru', 'role': 'professor',
         'name': 'Алексей', 'surname': 'Волков', 'patronymic': 'Игоревич', 'subject': 'Правоведение'},
        {'user': 'admin_staff', 'password': 'admin123', 'email': 'admin@college.ru', 'role': 'staff',
         'name': 'Ольга', 'surname': 'Николаева', 'patronymic': 'Владимировна', 'position': 'Заведующая учебной частью'},
        {'user': 'methodist', 'password': 'method123', 'email': 'method@college.ru', 'role': 'staff',
         'name': 'Сергей', 'surname': 'Михайлов', 'patronymic': 'Алексеевич', 'position': 'Методист'},
    ]
    students_data = [
        {'user': 'alekseev_a', 'surname': 'Алексеев', 'name': 'Алексей', 'patronymic': 'Алексеевич', 'group': 'ПРО-11'},
        {'user': 'borisov_b', 'surname': 'Борисов', 'name': 'Борис', 'patronymic': 'Борисович', 'group': 'ПРО-11'},
        {'user': 'vinogradov_v', 'surname': 'Виноградов', 'name': 'Виктор', 'patronymic': 'Викторович', 'group': 'ПРО-11'},
        {'user': 'grigoriev_g', 'surname': 'Григорьев', 'name': 'Григорий', 'patronymic': 'Григорьевич', 'group': 'ПРО-11'},
        {'user': 'dmitriev_d', 'surname': 'Дмитриев', 'name': 'Дмитрий', 'patronymic': 'Дмитриевич', 'group': 'ПРО-11'},
        {'user': 'egorov_e', 'surname': 'Егоров', 'name': 'Егор', 'patronymic': 'Егорович', 'group': 'ПРО-11'},
        {'user': 'zhukova_a', 'surname': 'Жукова', 'name': 'Анна', 'patronymic': 'Сергеевна', 'group': 'ПРО-11'},
        {'user': 'zaytseva_e', 'surname': 'Зайцева', 'name': 'Елена', 'patronymic': 'Владимировна', 'group': 'ПРО-11'},
        {'user': 'ivanova_m', 'surname': 'Иванова', 'name': 'Мария', 'patronymic': 'Петровна', 'group': 'ПРО-11'},
        {'user': 'kuznetsov_a', 'surname': 'Кузнецов', 'name': 'Андрей', 'patronymic': 'Игоревич', 'group': 'ПРО-11'},
        {'user': 'kuznetsov_a2', 'surname': 'Кузнецов', 'name': 'Александр', 'patronymic': 'Владимирович', 'group': 'ПРО-11'},
        {'user': 'lebedeva_o', 'surname': 'Лебедева', 'name': 'Ольга', 'patronymic': 'Николаевна', 'group': 'ПРО-11'},
        {'user': 'mikhailov_m', 'surname': 'Михайлов', 'name': 'Михаил', 'patronymic': 'Михайлович', 'group': 'ПРО-12'},
        {'user': 'nikolaev_n', 'surname': 'Николаев', 'name': 'Николай', 'patronymic': 'Николаевич', 'group': 'ПРО-12'},
        {'user': 'orlova_i', 'surname': 'Орлова', 'name': 'Ирина', 'patronymic': 'Алексеевна', 'group': 'ПРО-12'},
        {'user': 'pavlov_p', 'surname': 'Павлов', 'name': 'Павел', 'patronymic': 'Павлович', 'group': 'ПРО-12'},
        {'user': 'romanov_r', 'surname': 'Романов', 'name': 'Роман', 'patronymic': 'Романович', 'group': 'ПРО-12'},
        {'user': 'sokolova_s', 'surname': 'Соколова', 'name': 'Светлана', 'patronymic': 'Сергеевна', 'group': 'ПРО-12'},
        {'user': 'titov_t', 'surname': 'Титов', 'name': 'Тимофей', 'patronymic': 'Тимофеевич', 'group': 'ПРО-21'},
        {'user': 'ustinov_u', 'surname': 'Устинов', 'name': 'Устин', 'patronymic': 'Устинович', 'group': 'ПРО-21'},
        {'user': 'fedorov_f', 'surname': 'Федоров', 'name': 'Федор', 'patronymic': 'Федорович', 'group': 'ПРО-21'},
        {'user': 'kharitonova_k', 'surname': 'Харитонова', 'name': 'Ксения', 'patronymic': 'Константиновна', 'group': 'ПРО-21'},
        {'user': 'tsvetkova_t', 'surname': 'Цветкова', 'name': 'Татьяна', 'patronymic': 'Тимофеевна', 'group': 'ЭК-11'},
        {'user': 'shapovalov_s', 'surname': 'Шаповалов', 'name': 'Сергей', 'patronymic': 'Сергеевич', 'group': 'ЭК-11'},
        {'user': 'shcherbakova_s', 'surname': 'Щербакова', 'name': 'Софья', 'patronymic': 'Андреевна', 'group': 'ЭК-11'},
        {'user': 'yakovlev_y', 'surname': 'Яковлев', 'name': 'Ярослав', 'patronymic': 'Яковлевич', 'group': 'ЭК-11'},
        {'user': 'abramov_a', 'surname': 'Абрамов', 'name': 'Артем', 'patronymic': 'Артемович', 'group': 'ПСО-11'},
        {'user': 'belova_b', 'surname': 'Белова', 'name': 'Валерия', 'patronymic': 'Викторовна', 'group': 'ПСО-11'},
        {'user': 'vasiliev_v', 'surname': 'Васильев', 'name': 'Владислав', 'patronymic': 'Владиславович', 'group': 'ПСО-11'},
    ]
    for data in users_data:
        if data['role'] == 'professor':
            user, _ = Autoriz.objects.get_or_create(
                user=data['user'],
                defaults={
                    'password': data['password'],
                    'email': data['email'],
                    'birth_date': date(randint(1970, 1985), randint(1, 12), randint(1, 28)),
                    'gender': choice(['M', 'F']),
                    'phone': f'+7{randint(900, 999)}{randint(1000000, 9999999)}',
                    'hide_phone': False
                }
            )
            subject = Subjects.objects.filter(name_subject=data['subject']).first()
            Professor.objects.get_or_create(
                autoriz=user,
                defaults={
                    'name': data['name'],
                    'surname': data['surname'],
                    'patronymic': data['patronymic'],
                    'leads_the_subject': subject
                }
            )
            ChatProfile.objects.get_or_create(user=user, defaults={
                'interests': choice(['Программирование', 'Чтение книг', 'Спорт', 'Путешествия', 'Музыка']),
                'about': f'Преподаватель предмета {data["subject"]}. Опыт работы более {randint(5, 20)} лет.',
                'city': choice(['Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск', 'Екатеринбург'])
            })
    for data in users_data:
        if data['role'] == 'staff':
            user, _ = Autoriz.objects.get_or_create(
                user=data['user'],
                defaults={
                    'password': data['password'],
                    'email': data['email'],
                    'birth_date': date(randint(1975, 1990), randint(1, 12), randint(1, 28)),
                    'gender': choice(['M', 'F']),
                    'phone': f'+7{randint(900, 999)}{randint(1000000, 9999999)}',
                    'hide_phone': False
                }
            )
            AcademicStaff.objects.get_or_create(
                autoriz=user,
                defaults={
                    'name': data['name'],
                    'surname': data['surname'],
                    'patronymic': data['patronymic'],
                    'position': data['position']
                }
            )
            ChatProfile.objects.get_or_create(user=user, defaults={
                'interests': 'Административная работа',
                'about': f'Сотрудник учебной части, {data["position"]}',
                'city': 'Москва'
            })
    groups = {g.name: g for g in Group.objects.all()}
    student_counter = 1
    for data in students_data:
        group = groups.get(data['group'])
        if group:
            user, _ = Autoriz.objects.get_or_create(
                user=data['user'],
                defaults={
                    'password': f'student{student_counter}',
                    'email': f'{data["user"]}@college.ru',
                    'birth_date': date(randint(2000, 2006), randint(1, 12), randint(1, 28)),
                    'gender': choice(['M', 'F']),
                    'phone': f'+7{randint(900, 999)}{randint(1000000, 9999999)}',
                    'hide_phone': choice([True, False])
                }
            )
            Student.objects.get_or_create(
                autoriz=user,
                defaults={
                    'name': data['name'],
                    'surname': data['surname'],
                    'patronymic': data['patronymic'],
                    'group': group
                }
            )
            ChatProfile.objects.get_or_create(user=user, defaults={
                'interests': choice(['Спорт', 'Музыка', 'Игры', 'Программирование', 'Дизайн', 'Кино']),
                'about': f'Студент группы {data["group"]}, учусь на {group.course.number} курсе',
                'city': choice(['Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск', 'Екатеринбург', 'Самара', 'Ростов-на-Дону'])
            })
            student_counter += 1
    print(f"Создано: {Autoriz.objects.count()} пользователей")
    print(f"  - Профессоров: {Professor.objects.count()}")
    print(f"  - Сотрудников: {AcademicStaff.objects.count()}")
    print(f"  - Студентов: {Student.objects.count()}")

def create_balances():
    for student in Student.objects.all():
        balance, _ = balance_topcoins_and_topgems.objects.get_or_create(
            student=student,
            defaults={
                'topcoins': randint(50, 500),
                'topgems': randint(5, 50)
            }
        )
        Topmoney_student.objects.get_or_create(
            student=student,
            balance_student=balance,
            defaults={'topmoney': balance.topcoins + balance.topgems}
        )
    print(f"Создано {balance_topcoins_and_topgems.objects.count()} балансов")

def create_classrooms():
    rooms = ['101', '102', '103', '104', '105', '106', '107', '201', '202', '203', '204', '205', '206',
             '207', '208', '301', '302', '303', '304', '305', '401', '402', 'Компьютерный класс A',
             'Компьютерный класс B', 'Лаборатория химии', 'Лаборатория физики', 'Актовый зал']
    for room in rooms:
        Add_Сlassroom.objects.get_or_create(name_classroom=f'Ауд. {room}')
    print(f"Создано {Add_Сlassroom.objects.count()} аудиторий")

def create_lesson_types():
    types = [
        {'type': 'lecture', 'name': 'Лекция'},
        {'type': 'practice', 'name': 'Практическое занятие'},
        {'type': 'lab', 'name': 'Лабораторная работа'},
        {'type': 'seminar', 'name': 'Семинар'},
        {'type': 'exam', 'name': 'Экзамен'},
        {'type': 'consultation', 'name': 'Консультация'},
    ]
    for t in types:
        LessonType.objects.get_or_create(type=t['type'], defaults={'name': t['name']})
    print(f"Создано {LessonType.objects.count()} типов занятий")

def create_semesters():
    academic_years = AcademicYear.objects.all()
    for year in academic_years:
        Semester.objects.get_or_create(
            name=f'Осенний семестр {year.name}',
            semester_type='autumn',
            academic_year=year,
            defaults={
                'start_date': date(year.start_date.year, 9, 1),
                'end_date': date(year.start_date.year, 12, 31),
                'is_active': year.is_current
            }
        )
        Semester.objects.get_or_create(
            name=f'Весенний семестр {year.name}',
            semester_type='spring',
            academic_year=year,
            defaults={
                'start_date': date(year.start_date.year + 1, 2, 1),
                'end_date': date(year.start_date.year + 1, 6, 30),
                'is_active': False
            }
        )
    print(f"Создано {Semester.objects.count()} семестров")

def create_pairs():
    professors = Professor.objects.all()
    subjects = Subjects.objects.all()
    classrooms = Add_Сlassroom.objects.all()
    lesson_types = LessonType.objects.all()
    for pair_num in range(1, 7):
        professor = professors[pair_num % len(professors)] if professors else None
        subject = subjects[pair_num % len(subjects)] if subjects else None
        classroom = classrooms[pair_num % len(classrooms)] if classrooms else None
        lesson_type = lesson_types[pair_num % len(lesson_types)] if lesson_types else None
        if professor and subject:
            Pair.objects.get_or_create(
                pair_number=pair_num,
                professor=professor,
                subject=subject,
                defaults={'classroom': classroom, 'lesson_type': lesson_type}
            )
    print(f"Создано {Pair.objects.count()} пар")

def create_schedules():
    print("Создание расписаний...")
    
    groups = Group.objects.all()
    semester = Semester.objects.filter(is_active=True).first()
    if not semester:
        semester = Semester.objects.first()
    
    pairs = list(Pair.objects.all())
    if not pairs:
        print("  Нет пар для создания расписания")
        return
    
    weekdays = [1, 2, 3, 4, 5]  # ПН-ПТ
    pair_orders = [1, 2, 3, 4]   # 4 пары
    
    for group in groups:
        # Создаем расписание на текущую неделю
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        schedule, created = Schedule.objects.get_or_create(
            group=group,
            semester=semester,
            week_start_date=week_start,
            defaults={
                'week_end_date': week_start + timedelta(days=6),
                'is_active': True,
                'is_current_week': True
            }
        )
        
        # Создаем DailySchedule для каждого дня и пары
        for weekday in weekdays:
            for pair_order in pair_orders:
                # Берем пару по индексу
                pair_index = (weekday * pair_order) % len(pairs)
                pair = pairs[pair_index]
                
                # Используем update_or_create с учетом schedule
                DailySchedule.objects.update_or_create(
                    schedule=schedule,
                    weekday=weekday,
                    pair_order=pair_order,
                    group=group,
                    defaults={'pair': pair}
                )
        
        daily_count = DailySchedule.objects.filter(schedule=schedule).count()
        print(f"  Группа {group.name}: {daily_count} записей в расписании")
    
    print(f"  Всего расписаний: {Schedule.objects.count()}")
    print(f"  Всего дневных расписаний: {DailySchedule.objects.count()}")

def create_shop_products():
    products = [
        {'name': 'Ручка гелевая', 'quantity': 100, 'coins': 15, 'gems': 1},
        {'name': 'Тетрадь общая', 'quantity': 80, 'coins': 30, 'gems': 2},
        {'name': 'Карандаш механический', 'quantity': 60, 'coins': 12, 'gems': 1},
        {'name': 'Ластик', 'quantity': 90, 'coins': 8, 'gems': 0},
        {'name': 'Линейка 15см', 'quantity': 50, 'coins': 20, 'gems': 1},
        {'name': 'Набор стикеров', 'quantity': 120, 'coins': 10, 'gems': 1},
        {'name': 'Блокнот A6', 'quantity': 40, 'coins': 60, 'gems': 5},
        {'name': 'Папка для документов', 'quantity': 35, 'coins': 45, 'gems': 3},
        {'name': 'Маркеры (набор)', 'quantity': 30, 'coins': 80, 'gems': 8},
        {'name': 'Степлер', 'quantity': 15, 'coins': 120, 'gems': 12},
        {'name': 'Дырокол', 'quantity': 10, 'coins': 150, 'gems': 15},
        {'name': 'Скоросшиватель', 'quantity': 70, 'coins': 25, 'gems': 2},
    ]
    for p in products:
        Shop_add_products.objects.get_or_create(
            name_product=p['name'],
            defaults={
                'product_quantity': p['quantity'],
                'price_product_topcoins': p['coins'],
                'price_product_topgems': p['gems']
            }
        )
    print(f"Создано {Shop_add_products.objects.count()} товаров")

def create_payment_settings():
    groups = Group.objects.all()
    for group in groups[:10]:
        All_payment_of_education.objects.get_or_create(
            group=group,
            type_payment=choice(['month', 'year']),
            defaults={
                'amount': choice([15000, 18000, 20000, 25000, 30000]),
                'period_of_study': randint(9, 48),
                'date': date.today().replace(day=1)
            }
        )
    print(f"Создано {All_payment_of_education.objects.count()} настроек оплаты")

def create_announcements():
    announcements = [
        {'title': 'День открытых дверей', 'description': 'Приглашаем всех желающих на день открытых дверей 25 апреля в 11:00', 'is_for_all': True},
        {'title': 'Расписание экзаменов', 'description': 'Расписание экзаменов опубликовано в разделе "Экзамены"', 'is_for_all': True},
        {'title': 'Стипендия за март', 'description': 'Стипендия за март будет выплачена 10 апреля', 'is_for_all': True},
        {'title': 'Олимпиада по программированию', 'description': 'Регистрация на олимпиаду открыта до 1 мая', 'is_for_all': True},
        {'title': 'График каникул', 'description': 'Летние каникулы с 1 июля по 31 августа', 'is_for_all': True},
        {'title': 'Встреча выпускников', 'description': 'Встреча выпускников состоится 15 мая в 18:00', 'is_for_all': True},
    ]
    for ann in announcements:
        Announcement.objects.get_or_create(title=ann['title'], defaults=ann)
    print(f"Создано {Announcement.objects.count()} объявлений")

def create_events():
    events = [
        {'title': 'Олимпиада по программированию', 'event_type': 'exam',
         'start_date': timezone.now() + timedelta(days=14), 'end_date': timezone.now() + timedelta(days=14),
         'description': 'Внутриколледжная олимпиада по программированию', 'location': 'Ауд. 201', 'is_for_all': True},
        {'title': 'Субботник', 'event_type': 'other',
         'start_date': timezone.now() + timedelta(days=7), 'end_date': timezone.now() + timedelta(days=7),
         'description': 'Весенний субботник на территории колледжа', 'location': 'Территория колледжа', 'is_for_all': True},
        {'title': 'День карьеры', 'event_type': 'meeting',
         'start_date': timezone.now() + timedelta(days=21), 'end_date': timezone.now() + timedelta(days=21),
         'description': 'Встреча с представителями компаний-работодателей', 'location': 'Актовый зал', 'is_for_all': True},
        {'title': 'Концерт ко Дню Победы', 'event_type': 'holiday',
         'start_date': timezone.now() + timedelta(days=25), 'end_date': timezone.now() + timedelta(days=25),
         'description': 'Праздничный концерт', 'location': 'Актовый зал', 'is_for_all': True},
    ]
    for ev in events:
        Event.objects.get_or_create(title=ev['title'], defaults=ev)
    print(f"Создано {Event.objects.count()} событий")

def create_chats():
    users = Autoriz.objects.all()
    for i, user1 in enumerate(users):
        for user2 in users[i+1:]:
            if randint(0, 2) < 1:
                chat, _ = Chat.objects.get_or_create()
                chat.participants.add(user1, user2)
    print(f"Создано {Chat.objects.count()} чатов")

def create_messages():
    chats = Chat.objects.all()
    message_templates = [
        "Привет! Как дела?", "Отлично! А у тебя?", "Что делаешь?", "Готовишься к экзаменам?",
        "Да, готовлюсь", "Удачи!", "Спасибо!", "Приходи на пару завтра", "Обязательно приду",
        "Скинь домашнее задание", "Вот файл с заданием", "Спасибо большое!", "Не за что!",
        "Когда будет консультация?", "В пятницу в 14:00", "Понял, спасибо", "Помоги с лабораторной",
        "Какую тему?", "Базы данных", "Хорошо, скину пример"
    ]
    for chat in chats:
        participants = list(chat.participants.all())
        if len(participants) >= 2:
            for _ in range(randint(3, 20)):
                sender = choice(participants)
                Message.objects.create(
                    chat=chat,
                    sender=sender,
                    text=choice(message_templates),
                    created_at=timezone.now() - timedelta(days=randint(0, 30), hours=randint(0, 23)),
                    is_read=choice([True, False]),
                    is_delivered=True
                )
    print(f"Создано {Message.objects.count()} сообщений")

def create_estimations():
    students = Student.objects.all()
    subjects = Subjects.objects.all()
    for student in students:
        for subject in subjects[:randint(5, 10)]:
            for _ in range(randint(1, 5)):
                Estimation.objects.create(
                    student=student,
                    subject=subject,
                    type_estimation=randint(2, 5),
                    date=timezone.now() - timedelta(days=randint(0, 365))
                )
    print(f"Создано {Estimation.objects.count()} оценок")

def create_attendance():
    students = Student.objects.all()
    schedules = Schedule.objects.filter(is_active=True)
    for student in students[:50]:
        for schedule in schedules[:10]:
            for _ in range(randint(1, 5)):
                Attendance.objects.create(
                    student=student,
                    schedule=schedule,
                    type=choice(['presence', 'late', 'absence']),
                    data_created=timezone.now() - timedelta(days=randint(0, 30))
                )
    print(f"Создано {Attendance.objects.count()} записей посещаемости")

def create_rewards():
    rewards = [
        {'name': 'За отличную учебу', 'description': 'Награждаются студенты с высоким средним баллом',
         'reward_type': 'one_time', 'topcoins_award': 200, 'topgems_award': 20, 'is_active': True},
        {'name': 'За идеальную посещаемость', 'description': 'Награждаются студенты без пропусков',
         'reward_type': 'one_time', 'topcoins_award': 150, 'topgems_award': 15, 'is_active': True},
        {'name': 'За активность', 'description': 'За активное участие в жизни колледжа',
         'reward_type': 'multiple', 'topcoins_award': 100, 'topgems_award': 10, 'is_active': True},
        {'name': 'Победитель олимпиады', 'description': 'Приз за победу в олимпиаде',
         'reward_type': 'one_time', 'topcoins_award': 500, 'topgems_award': 50, 'is_active': True},
        {'name': 'Волонтер года', 'description': 'За вклад в волонтерскую деятельность',
         'reward_type': 'one_time', 'topcoins_award': 300, 'topgems_award': 30, 'is_active': True},
    ]
    for r in rewards:
        Reward.objects.get_or_create(name=r['name'], defaults=r)
    print(f"Создано {Reward.objects.count()} наград")

def create_user_rewards():
    students = Student.objects.all()
    rewards = Reward.objects.all()
    for student in students[:30]:
        for reward in rewards[:randint(1, 3)]:
            UserReward.objects.get_or_create(
                student=student,
                reward=reward,
                defaults={
                    'topcoins_given': reward.topcoins_award,
                    'topgems_given': reward.topgems_award
                }
            )
    print(f"Создано {UserReward.objects.count()} наград студентов")

def create_leaderboard():
    students = Student.objects.all()
    semester = Semester.objects.filter(is_active=True).first()
    groups = Group.objects.all()
    for group in groups:
        group_students = Student.objects.filter(group=group)
        student_topmoney = []
        for student in group_students:
            try:
                topmoney_obj = Topmoney_student.objects.get(student=student)
                student_topmoney.append((student, topmoney_obj.topmoney))
            except Topmoney_student.DoesNotExist:
                student_topmoney.append((student, 0))
        student_topmoney.sort(key=lambda x: x[1], reverse=True)
        for rank, (student, topmoney) in enumerate(student_topmoney[:10], 1):
            LeaderboardEntry.objects.get_or_create(
                student=student,
                semester=semester,
                defaults={
                    'topmoney': topmoney,
                    'group': group,
                    'rank_in_group': rank,
                    'rank_in_course': rank
                }
            )
    print(f"Создано {LeaderboardEntry.objects.count()} записей рейтинга")

def create_homeworks():
    professors = Professor.objects.all()
    groups = Group.objects.all()
    subjects = Subjects.objects.all()
    counter = 1
    for group in groups[:5]:
        for subject in subjects[:3]:
            professor = professors.first()
            Add_HW_Professor_to_course.objects.get_or_create(
                group=group,
                subject=subject,
                professor=professor,
                defaults={
                    'file': f'static/image/homeworks_for_students/hw_{counter}.pdf',
                    'comment': f'Домашнее задание по предмету {subject.name_subject} для группы {group.name}',
                    'date_final': date.today() + timedelta(days=7)
                }
            )
            counter += 1
    print(f"Создано {Add_HW_Professor_to_course.objects.count()} домашних заданий")

def create_homework_submissions():
    students = Student.objects.all()
    homeworks = Add_HW_Professor_to_course.objects.all()
    for student in students[:20]:
        for homework in homeworks[:3]:
            HomeworkSubmission.objects.get_or_create(
                homework=homework,
                student=student,
                defaults={
                    'file': f'static/image/homework_submissions/submission_{student.id}_{homework.id}.pdf',
                    'comment': f'Работа студента {student}',
                    'time_work': randint(30, 180),
                    'the_usefulness_of_knowledge': randint(1, 5),
                    'grade': randint(2, 5),
                    'is_checked': choice([True, False])
                }
            )
    print(f"Создано {HomeworkSubmission.objects.count()} сданных работ")

def create_educational_materials():
    professors = Professor.objects.all()
    subjects = Subjects.objects.all()
    for professor in professors:
        for subject in subjects[:2]:
            EducationalMaterial.objects.get_or_create(
                title=f'Материалы по {subject.name_subject}',
                professor=professor,
                subject=subject,
                defaults={
                    'file': f'static/image/educational_materials/material_{professor.id}_{subject.id}.pdf',
                    'description': f'Учебные материалы по предмету {subject.name_subject}',
                    'is_public': choice([True, False])
                }
            )
    print(f"Создано {EducationalMaterial.objects.count()} учебных материалов")

def create_all_schedules():
    groups = Group.objects.all()
    semester = Semester.objects.filter(is_active=True).first()
    pairs = Pair.objects.all()

    for group in groups:
        week_start = date.today()
        if week_start.weekday() != 0:
            days_ahead = 0 - week_start.weekday()
            week_start += timedelta(days=days_ahead)

        schedule, _ = Schedule.objects.get_or_create(
            group=group,
            semester=semester,
            week_start_date=week_start,
            defaults={'is_active': True, 'is_current_week': True}
        )

        for day in range(1, 6):
            for pair_order in range(1, 5):
                pair = pairs[(day * pair_order) % len(pairs)] if pairs else None
                if pair:
                    DailySchedule.objects.get_or_create(
                        weekday=day,
                        pair_order=pair_order,
                        group=group,
                        schedule=schedule,
                        defaults={'pair': pair}
                    )
    print(f"Создано расписаний: {Schedule.objects.count()}")

def run_seed():
    print("\n" + "="*60)
    print("🚀 НАЧАЛО ЗАПОЛНЕНИЯ БАЗЫ ДАННЫХ")
    print("="*60 + "\n")
    create_directions()
    create_courses()
    create_academic_years()
    create_groups()
    create_subjects()
    create_users()
    create_balances()
    create_classrooms()
    create_lesson_types()
    create_semesters()
    create_pairs()
    create_schedules()
    create_shop_products()
    create_payment_settings()
    create_announcements()
    create_events()
    create_chats()
    create_messages()
    create_estimations()
    create_attendance()
    create_rewards()
    create_user_rewards()
    create_leaderboard()
    create_homeworks()
    create_homework_submissions()
    create_educational_materials()
    create_all_schedules()
    print("\n" + "="*60)
    print("✅ БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
    print("="*60)
    print("\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"   - Направлений: {Direction.objects.count()}")
    print(f"   - Курсов: {Course.objects.count()}")
    print(f"   - Учебных годов: {AcademicYear.objects.count()}")
    print(f"   - Групп: {Group.objects.count()}")
    print(f"   - Предметов: {Subjects.objects.count()}")
    print(f"   - Преподавателей: {Professor.objects.count()}")
    print(f"   - Сотрудников: {AcademicStaff.objects.count()}")
    print(f"   - Студентов: {Student.objects.count()}")
    print(f"   - Пользователей: {Autoriz.objects.count()}")
    print(f"   - Аудиторий: {Add_Сlassroom.objects.count()}")
    print(f"   - Типов занятий: {LessonType.objects.count()}")
    print(f"   - Семестров: {Semester.objects.count()}")
    print(f"   - Пар: {Pair.objects.count()}")
    print(f"   - Расписаний: {Schedule.objects.count()}")
    print(f"   - Товаров в магазине: {Shop_add_products.objects.count()}")
    print(f"   - Объявлений: {Announcement.objects.count()}")
    print(f"   - Событий: {Event.objects.count()}")
    print(f"   - Чатов: {Chat.objects.count()}")
    print(f"   - Сообщений: {Message.objects.count()}")
    print(f"   - Оценок: {Estimation.objects.count()}")
    print(f"   - Посещаемости: {Attendance.objects.count()}")
    print(f"   - Наград: {Reward.objects.count()}")
    print(f"   - Наград студентов: {UserReward.objects.count()}")
    print(f"   - Рейтингов: {LeaderboardEntry.objects.count()}")

if __name__ == "__main__":
    run_seed()