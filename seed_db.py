# seed_db.py
import os
import django
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.models import (
    Autoriz, Direction, Course, AcademicYear, Group, Subjects, Professor, 
    Student, Add_Сlassroom, LessonType, Pair, DailySchedule, Schedule, 
    Semester, balance_topcoins_and_topgems, Shop_add_products, 
    All_payment_of_education, Students_payment_account, Announcement, Event
)

def create_directions():
    directions = [
        {'code': '09.02.07', 'name': 'Информационные системы и программирование'},
        {'code': '38.02.01', 'name': 'Экономика и бухгалтерский учет'},
        {'code': '40.02.01', 'name': 'Право и организация социального обеспечения'},
        {'code': '13.02.11', 'name': 'Техническая эксплуатация и обслуживание электрического и электромеханического оборудования'},
        {'code': '42.02.01', 'name': 'Реклама'},
    ]
    for d in directions:
        Direction.objects.get_or_create(code=d['code'], defaults={'name': d['name']})
    print(f"✅ Создано {Direction.objects.count()} направлений")

def create_courses():
    for i in range(1, 5):
        Course.objects.get_or_create(number=i)
    print(f"✅ Создано {Course.objects.count()} курсов")

def create_academic_years():
    current_year = date.today().year
    years = [
        {'name': f'{current_year-2}-{current_year-1}', 'start_date': date(current_year-2, 9, 1), 'end_date': date(current_year-1, 8, 31), 'is_current': False},
        {'name': f'{current_year-1}-{current_year}', 'start_date': date(current_year-1, 9, 1), 'end_date': date(current_year, 8, 31), 'is_current': True},
        {'name': f'{current_year}-{current_year+1}', 'start_date': date(current_year, 9, 1), 'end_date': date(current_year+1, 8, 31), 'is_current': False},
    ]
    for y in years:
        AcademicYear.objects.get_or_create(name=y['name'], defaults=y)
    print(f"✅ Создано {AcademicYear.objects.count()} учебных годов")

def create_groups():
    directions = Direction.objects.all()
    courses = Course.objects.all()
    academic_year = AcademicYear.objects.filter(is_current=True).first()
    
    groups_data = [
        ('ПРО-11', 1, '09.02.07'),
        ('ПРО-12', 1, '09.02.07'),
        ('ПРО-21', 2, '09.02.07'),
        ('ПРО-22', 2, '09.02.07'),
        ('ПРО-31', 3, '09.02.07'),
        ('ЭК-11', 1, '38.02.01'),
        ('ЭК-12', 1, '38.02.01'),
        ('ЭК-21', 2, '38.02.01'),
        ('ПСО-11', 1, '40.02.01'),
        ('ПСО-21', 2, '40.02.01'),
        ('ЭЛ-11', 1, '13.02.11'),
        ('РК-11', 1, '42.02.01'),
    ]
    
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
    print(f"✅ Создано {Group.objects.count()} групп")

def create_subjects():
    subjects = [
        'Основы программирования', 'Базы данных', 'Web-разработка', 
        'Объектно-ориентированное программирование', 'Операционные системы',
        'Математика', 'Русский язык', 'Английский язык', 'Физика',
        'Экономика', 'Бухгалтерский учет', 'Налоги и налогообложение',
        'Гражданское право', 'Уголовное право', 'Административное право',
        'Электротехника', 'Схемотехника', 'Микропроцессоры',
        'Маркетинг', 'Рекламные технологии'
    ]
    for subj in subjects:
        Subjects.objects.get_or_create(name_subject=subj)
    print(f"✅ Создано {Subjects.objects.count()} предметов")

def create_users_and_professors():
    professors_data = [
        {'user': 'ivanov', 'password': 'ivanov123', 'email': 'ivanov@college.ru', 
         'name': 'Иван', 'surname': 'Иванов', 'patronymic': 'Петрович', 'subject': 'Основы программирования'},
        {'user': 'petrov', 'password': 'petrov123', 'email': 'petrov@college.ru',
         'name': 'Петр', 'surname': 'Петров', 'patronymic': 'Сергеевич', 'subject': 'Базы данных'},
        {'user': 'sidorov', 'password': 'sidorov123', 'email': 'sidorov@college.ru',
         'name': 'Сидор', 'surname': 'Сидоров', 'patronymic': 'Алексеевич', 'subject': 'Математика'},
        {'user': 'smirnova', 'password': 'smirnova123', 'email': 'smirnova@college.ru',
         'name': 'Анна', 'surname': 'Смирнова', 'patronymic': 'Владимировна', 'subject': 'Английский язык'},
        {'user': 'kozlov', 'password': 'kozlov123', 'email': 'kozlov@college.ru',
         'name': 'Дмитрий', 'surname': 'Козлов', 'patronymic': 'Николаевич', 'subject': 'Экономика'},
    ]
    
    for prof in professors_data:
        user, _ = Autoriz.objects.get_or_create(
            user=prof['user'],
            defaults={'password': prof['password'], 'email': prof['email']}
        )
        subject = Subjects.objects.filter(name_subject=prof['subject']).first()
        Professor.objects.get_or_create(
            autoriz=user,
            defaults={
                'name': prof['name'],
                'surname': prof['surname'],
                'patronymic': prof['patronymic'],
                'leads_the_subject': subject
            }
        )
    print(f"✅ Создано {Professor.objects.count()} преподавателей")

def create_students():
    groups = Group.objects.all()
    students_data = [
        {'surname': 'Алексеев', 'name': 'Алексей', 'patronymic': 'Алексеевич'},
        {'surname': 'Борисов', 'name': 'Борис', 'patronymic': 'Борисович'},
        {'surname': 'Владимиров', 'name': 'Владимир', 'patronymic': 'Владимирович'},
        {'surname': 'Григорьев', 'name': 'Григорий', 'patronymic': 'Григорьевич'},
        {'surname': 'Дмитриев', 'name': 'Дмитрий', 'patronymic': 'Дмитриевич'},
        {'surname': 'Егоров', 'name': 'Егор', 'patronymic': 'Егорович'},
        {'surname': 'Жукова', 'name': 'Анна', 'patronymic': 'Сергеевна'},
        {'surname': 'Зайцева', 'name': 'Елена', 'patronymic': 'Владимировна'},
        {'surname': 'Иванова', 'name': 'Мария', 'patronymic': 'Петровна'},
        {'surname': 'Кузнецов', 'name': 'Андрей', 'patronymic': 'Игоревич'},
    ]
    
    student_counter = 1
    for group in groups:
        for i in range(5):
            if student_counter <= len(students_data):
                data = students_data[student_counter - 1]
            else:
                data = {'surname': f'Студент{student_counter}', 'name': 'Имя', 'patronymic': 'Отчество'}
            
            user, _ = Autoriz.objects.get_or_create(
                user=f'student{student_counter}',
                defaults={'password': f'student{student_counter}', 'email': f'student{student_counter}@college.ru'}
            )
            Student.objects.get_or_create(
                autoriz=user,
                defaults={
                    'surname': data['surname'],
                    'name': data['name'],
                    'patronymic': data['patronymic'],
                    'group': group
                }
            )
            student_counter += 1
    
    for student in Student.objects.all():
        balance_topcoins_and_topgems.objects.get_or_create(
            student=student,
            defaults={'topcoins': 100, 'topgems': 10}
        )
    
    print(f"✅ Создано {Student.objects.count()} студентов и балансов")

def create_classrooms():
    rooms = ['101', '102', '103', '104', '105', '201', '202', '203', '204', '205', '301', '302', '303']
    for room in rooms:
        Add_Сlassroom.objects.get_or_create(name_classroom=f'Ауд. {room}')
    print(f"✅ Создано {Add_Сlassroom.objects.count()} аудиторий")

def create_lesson_types():
    types = [
        {'type': 'lecture', 'name': 'Лекция'},
        {'type': 'practice', 'name': 'Практика'},
        {'type': 'lab', 'name': 'Лабораторная работа'},
        {'type': 'seminar', 'name': 'Семинар'},
        {'type': 'exam', 'name': 'Экзамен'},
    ]
    for t in types:
        LessonType.objects.get_or_create(type=t['type'], defaults={'name': t['name']})
    print(f"✅ Создано {LessonType.objects.count()} типов занятий")

def create_semesters():
    academic_years = AcademicYear.objects.all()
    for year in academic_years:
        autumn, _ = Semester.objects.get_or_create(
            name=f'Осенний семестр {year.name}',
            semester_type='autumn',
            academic_year=year,
            defaults={
                'start_date': date(year.start_date.year, 9, 1),
                'end_date': date(year.start_date.year, 12, 31),
                'is_active': year.is_current
            }
        )
        spring, _ = Semester.objects.get_or_create(
            name=f'Весенний семестр {year.name}',
            semester_type='spring',
            academic_year=year,
            defaults={
                'start_date': date(year.start_date.year + 1, 2, 1),
                'end_date': date(year.start_date.year + 1, 6, 30),
                'is_active': False
            }
        )
    print(f"✅ Создано {Semester.objects.count()} семестров")

def create_schedule():
    groups = Group.objects.filter(course__number=1)[:3]
    professors = Professor.objects.all()
    subjects = Subjects.objects.all()
    classrooms = Add_Сlassroom.objects.all()
    lesson_types = LessonType.objects.all()
    semester = Semester.objects.filter(is_active=True).first()
    
    week_start = date.today()
    if week_start.weekday() != 0:
        days_ahead = 0 - week_start.weekday()
        week_start += timedelta(days=days_ahead)
    
    schedule, _ = Schedule.objects.get_or_create(
        group=groups[0] if groups else None,
        semester=semester,
        week_start_date=week_start,
        defaults={'is_active': True, 'is_current_week': True}
    )
    
    for day in range(1, 6):
        for pair_order in range(1, 5):
            professor = professors[pair_order % len(professors)] if professors else None
            subject = subjects[pair_order % len(subjects)] if subjects else None
            classroom = classrooms[pair_order % len(classrooms)] if classrooms else None
            lesson_type = lesson_types[pair_order % len(lesson_types)] if lesson_types else None
            
            if professor and subject:
                pair, _ = Pair.objects.get_or_create(
                    pair_number=pair_order,
                    professor=professor,
                    subject=subject,
                    defaults={'classroom': classroom, 'lesson_type': lesson_type}
                )
                DailySchedule.objects.get_or_create(
                    weekday=day,
                    pair_order=pair_order,
                    group=groups[0],
                    defaults={'pair': pair}
                )
    
    print(f"✅ Создано расписание для группы {groups[0].name if groups else 'None'}")

def create_shop_products():
    products = [
        {'name': 'Ручка', 'quantity': 50, 'coins': 10, 'gems': 1},
        {'name': 'Тетрадь', 'quantity': 30, 'coins': 25, 'gems': 2},
        {'name': 'Карандаш', 'quantity': 40, 'coins': 8, 'gems': 0},
        {'name': 'Ластик', 'quantity': 35, 'coins': 5, 'gems': 0},
        {'name': 'Линейка', 'quantity': 25, 'coins': 15, 'gems': 1},
        {'name': 'Стикеры', 'quantity': 45, 'coins': 12, 'gems': 1},
        {'name': 'Блокнот', 'quantity': 20, 'coins': 50, 'gems': 5},
        {'name': 'Папка', 'quantity': 15, 'coins': 30, 'gems': 3},
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
    print(f"✅ Создано {Shop_add_products.objects.count()} товаров в магазине")

def create_payment_settings():
    groups = Group.objects.all()
    for group in groups[:3]:
        All_payment_of_education.objects.get_or_create(
            group=group,
            type_payment='month',
            defaults={
                'amount': 15000,
                'period_of_study': 10,
                'date': date.today().replace(day=1)
            }
        )
    print(f"✅ Создано {All_payment_of_education.objects.count()} настроек оплаты")

def create_announcements():
    announcements = [
        {'title': 'День открытых дверей', 'description': 'Приглашаем всех желающих на день открытых дверей 25 апреля в 11:00', 'is_for_all': True},
        {'title': 'Расписание экзаменов', 'description': 'Расписание экзаменов опубликовано в разделе "Экзамены"', 'is_for_all': True},
        {'title': 'Стипендия за март', 'description': 'Стипендия за март будет выплачена 10 апреля', 'is_for_all': True},
    ]
    for ann in announcements:
        Announcement.objects.get_or_create(title=ann['title'], defaults=ann)
    print(f"✅ Создано {Announcement.objects.count()} объявлений")

def create_events():
    events = [
        {'title': 'Олимпиада по программированию', 'event_type': 'exam', 
         'start_date': date.today() + timedelta(days=14), 'end_date': date.today() + timedelta(days=14), 
         'description': 'Внутриколледжная олимпиада по программированию', 'location': 'Ауд. 201', 'is_for_all': True},
        {'title': 'Субботник', 'event_type': 'other', 
         'start_date': date.today() + timedelta(days=7), 'end_date': date.today() + timedelta(days=7), 
         'description': 'Весенний субботник на территории колледжа', 'location': 'Территория колледжа', 'is_for_all': True},
    ]
    for ev in events:
        Event.objects.get_or_create(title=ev['title'], defaults=ev)
    print(f"✅ Создано {Event.objects.count()} событий")

def run_seed():
    print("\n" + "="*50)
    print("🚀 НАЧАЛО ЗАПОЛНЕНИЯ БАЗЫ ДАННЫХ")
    print("="*50 + "\n")
    
    create_directions()
    create_courses()
    create_academic_years()
    create_groups()
    create_subjects()
    create_users_and_professors()
    create_students()
    create_classrooms()
    create_lesson_types()
    create_semesters()
    create_schedule()
    create_shop_products()
    create_payment_settings()
    create_announcements()
    create_events()
    
    print("\n" + "="*50)
    print("✅ БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
    print("="*50)
    
    print("\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"   - Направлений: {Direction.objects.count()}")
    print(f"   - Курсов: {Course.objects.count()}")
    print(f"   - Учебных годов: {AcademicYear.objects.count()}")
    print(f"   - Групп: {Group.objects.count()}")
    print(f"   - Предметов: {Subjects.objects.count()}")
    print(f"   - Преподавателей: {Professor.objects.count()}")
    print(f"   - Студентов: {Student.objects.count()}")
    print(f"   - Аудиторий: {Add_Сlassroom.objects.count()}")
    print(f"   - Типов занятий: {LessonType.objects.count()}")
    print(f"   - Семестров: {Semester.objects.count()}")
    print(f"   - Товаров в магазине: {Shop_add_products.objects.count()}")
    print(f"   - Объявлений: {Announcement.objects.count()}")
    print(f"   - Событий: {Event.objects.count()}")

if __name__ == "__main__":
    run_seed()