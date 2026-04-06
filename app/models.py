from django.db import models
from datetime import timedelta

class Autoriz(models.Model):
    user = models.CharField(unique = True, max_length = 30, blank = False, null = True, error_messages = {'max_length': 'Длина имени не может содержать более 30 символов', 'blank': 'Напишите имя.', 'null': 'Напишите имя.'}, verbose_name = 'Имя аккаунта')
    password = models.CharField(max_length = 120, blank = False, null = False, error_messages = {'max_length': 'Длина пароля не может содержать более 40 символов', 'blank': 'Напишите пароль.', 'null': 'Напишите пароль.'}, verbose_name = 'Пароль от аккаунта')
    email = models.EmailField(unique = True, max_length = 100, blank = False, null = False, error_messages = {'max_length': 'Длина почты не может содержать более 100 символов', 'blank': 'Напишите почту.', 'null': 'Напишите почту.'}, verbose_name = 'Почта от аккаунта')

    class Meta:
        db_table = 'List_of_users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user

class Subjects(models.Model):
    name_subject = models.CharField(unique = True, max_length = 100, blank = False, null = False, verbose_name = 'Имя предмета')

    class Meta:
        db_table = 'List_of_subjects'
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name_subject

class Professor(models.Model):
    name = models.CharField(max_length = 30, blank = False, null = False, verbose_name = 'Имя профессора')
    surname = models.CharField(max_length = 30, blank = False, null = False, verbose_name = 'Фамилия профессора')
    patronymic = models.CharField(max_length = 40, blank = False, null = False, verbose_name = 'Отчество профессора')
    leads_the_subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, verbose_name = 'Ведет предмет')
    autoriz = models.ForeignKey(Autoriz, on_delete = models.CASCADE, verbose_name = 'Пользователь')

    class Meta:
        db_table = 'List_of_professors'
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return f"{self.surname} {self.name[0]}. {self.patronymic[0]}."

class AcademicStaff(models.Model):
    name = models.CharField(max_length = 30, verbose_name = 'Имя')
    surname = models.CharField(max_length = 30, verbose_name = 'Фамилия')
    patronymic = models.CharField(max_length = 40, verbose_name = 'Отчество')
    position = models.CharField(max_length = 100, verbose_name = 'Должность')
    autoriz = models.OneToOneField(Autoriz, on_delete = models.CASCADE, verbose_name = 'Пользователь')

    class Meta:
        db_table = 'List_of_academic_staff'
        verbose_name = 'Сотрудник учебной части'
        verbose_name_plural = 'Сотрудники учебной части'

    def __str__(self):
        return f"{self.surname} {self.name[0]}. {self.patronymic[0]}. - {self.position}"

class Direction(models.Model):
    name = models.CharField(max_length = 100, verbose_name = 'Название направления')
    code = models.CharField(max_length = 20, unique = True, verbose_name = 'Код направления')
    
    class Meta:
        db_table = 'List_of_directions'
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'
    
    def __str__(self):
        return f'{self.code} - {self.name}'

class Course(models.Model):
    number = models.IntegerField(verbose_name = 'Номер курса')
    
    class Meta:
        db_table = 'List_of_courses'
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
    
    def __str__(self):
        return f'{self.number} курс'

class Group(models.Model):
    name = models.CharField(max_length = 20, verbose_name = 'Название группы')
    course = models.ForeignKey(Course, on_delete = models.CASCADE, verbose_name = 'Курс')
    direction = models.ForeignKey(Direction, on_delete = models.CASCADE, verbose_name = 'Направление')
    academic_year = models.CharField(max_length = 9, verbose_name = 'Учебный год')
    
    class Meta:
        db_table = 'List_of_groups'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        unique_together = ['course', 'direction', 'name']
    
    def __str__(self):
        return f'{self.course.number}{self.direction.code}-{self.name}'

class AcademicYear(models.Model):
    name = models.CharField(max_length = 9, unique = True, verbose_name = 'Название', help_text = 'Например: 2024-2025')
    start_date = models.DateField(verbose_name = 'Дата начала')
    end_date = models.DateField(verbose_name = 'Дата окончания')
    is_current = models.BooleanField(default = False, verbose_name = 'Текущий учебный год')
    
    class Meta:
        db_table = 'List_of_academic_years'
        verbose_name = 'Учебный год'
        verbose_name_plural = 'Учебные годы'
    
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length = 30, blank = False, null = False, verbose_name = 'Имя студента')
    surname = models.CharField(max_length = 30, blank = False, null = False, verbose_name = 'Фамилия студента')
    patronymic = models.CharField(max_length = 40, blank = False, null = False, verbose_name = 'Отчество студента')
    autoriz = models.ForeignKey(Autoriz, on_delete = models.CASCADE, verbose_name = 'Пользователь')
    group = models.ForeignKey(Group, on_delete = models.CASCADE, null = True, blank = True, verbose_name = 'Группа')

    class Meta:
        db_table = 'List_of_students'
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
         return f"{self.surname} {self.name[0]}. {self.patronymic[0]}."

class Type_work(models.Model):
    HW = 'HW'
    LABS = 'LABS'
    CW = 'CW'
    KW = 'KW'
    PW = 'PW'
    SK = 'SK'
    
    CHOICE_TYPE_WORK = [
        (HW, 'Домашние задания'),
        (LABS, 'Лабораторные работы'),
        (CW, 'Классная работа'),
        (KW, 'Контрольные работы'),
        (PW, 'Практические работы'),
        (SK, 'Итоговая контрольная'),
    ]
    
    type = models.CharField(max_length = 4, choices = CHOICE_TYPE_WORK, default = HW, verbose_name = 'Тип работы')

class Estimation(models.Model):
    five = 'five'
    four = 'four'
    three = 'three'
    two = 'two'
    one = 'one'

    CHOICE_OF_ESTIMATION = [
        (five, 5),
        (four, 4),
        (three, 3),
        (two, 2),
        (one, 1)
    ]

    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'ФИО студента')
    subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, null = True, blank = True, verbose_name = 'Предмет')
    type_estimation = models.IntegerField(choices = CHOICE_OF_ESTIMATION, blank = False, null = False, verbose_name = 'Оценка студенту')
    date = models.DateField(auto_now_add = True, verbose_name = 'Дата получения оценки')

class Add_Сlassroom(models.Model):
    name_classroom = models.CharField(unique = True, blank = False, null = False, verbose_name = 'Название аудитории')

    class Meta:
        db_table = 'List_of_Add_classroom'
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'

    def __str__(self):
        return self.name_classroom

class LessonType(models.Model):
    LECTURE = 'lecture'
    PRACTICE = 'practice'
    LAB = 'lab'
    SEMINAR = 'seminar'
    EXAM = 'exam'
    
    TYPE_CHOICES = [
        (LECTURE, 'Лекция'),
        (PRACTICE, 'Практика'),
        (LAB, 'Лабораторная работа'),
        (SEMINAR, 'Семинар'),
        (EXAM, 'Экзамен'),
    ]
    
    type = models.CharField(max_length = 20, choices = TYPE_CHOICES, verbose_name = 'Тип занятия')
    name = models.CharField(max_length = 100, verbose_name = 'Название')
    
    class Meta:
        db_table = 'List_of_lesson_types'
        verbose_name = 'Тип занятия'
        verbose_name_plural = 'Типы занятий'
    
    def __str__(self):
        return self.name

class Pair(models.Model):
    PAIR_TIMES = [
        (1, '08:30-09:50'),
        (2, '10:00-11:20'),
        (3, '11:50-13:10'),
        (4, '13:20-14:40'),
        (5, '14:50-16:10'),
        (6, '16:20-17:40'),
        (7, '17:50-19:10'),
    ]
    
    pair_number = models.IntegerField(choices = PAIR_TIMES, verbose_name = 'Номер пары')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Преподаватель')
    subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, verbose_name = 'Предмет')
    classroom = models.ForeignKey(Add_Сlassroom, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Аудитория')
    lesson_type = models.ForeignKey(LessonType, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Тип занятия')
    
    class Meta:
        db_table = 'List_of_pairs'
        verbose_name = 'Пара'
        verbose_name_plural = 'Пары'
    
    def __str__(self):
        return f'{self.get_pair_number_display()} - {self.subject} - {self.professor}'

class DailySchedule(models.Model):
    WEEKDAYS = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    ]
    
    weekday = models.IntegerField(choices = WEEKDAYS, verbose_name = 'День недели')
    pair = models.ForeignKey(Pair, on_delete = models.CASCADE, verbose_name = 'Пара')
    pair_order = models.IntegerField(verbose_name = 'Порядковый номер пары')
    group = models.ForeignKey(Group, on_delete = models.CASCADE, verbose_name = 'Группа')
    
    class Meta:
        db_table = 'List_of_daily_schedules'
        verbose_name = 'Дневное расписание'
        verbose_name_plural = 'Дневные расписания'
        unique_together = ['weekday', 'pair_order', 'group']
    
    def __str__(self):
        return f'{self.get_weekday_display()} - {self.pair_order} пара - {self.group}'

class Semester(models.Model):
    AUTUMN = 'autumn'
    SPRING = 'spring'
    
    CHOICE_SEMESTER_TYPE = [
        (AUTUMN, 'Осенний семестр'),
        (SPRING, 'Весенний семестр'),
    ]
    
    name = models.CharField(max_length = 50, verbose_name = 'Название семестра')
    semester_type = models.CharField(max_length = 10, choices = CHOICE_SEMESTER_TYPE, verbose_name = 'Тип семестра')
    academic_year = models.ForeignKey(AcademicYear, on_delete = models.CASCADE, verbose_name = 'Учебный год')
    start_date = models.DateField(verbose_name = 'Дата начала семестра')
    end_date = models.DateField(verbose_name = 'Дата окончания семестра')
    is_active = models.BooleanField(default = False, verbose_name = 'Текущий семестр')
    
    class Meta:
        db_table = 'List_of_semesters'
        verbose_name = 'Семестр'
        verbose_name_plural = 'Семестры'
        ordering = ['-start_date']
    
    def __str__(self):
        return f'{self.get_semester_type_display()} {self.academic_year}'

class Vacation(models.Model):
    WINTER = 'winter'
    SUMMER = 'summer'
    
    CHOICE_VACATION_TYPE = [
        (WINTER, 'Зимние каникулы'),
        (SUMMER, 'Летние каникулы'),
    ]
    
    vacation_type = models.CharField(max_length = 10, choices = CHOICE_VACATION_TYPE, verbose_name = 'Тип каникул')
    start_date = models.DateField(verbose_name = 'Дата начала каникул')
    end_date = models.DateField(verbose_name = 'Дата окончания каникул')
    academic_year = models.ForeignKey(AcademicYear, on_delete = models.CASCADE, verbose_name = 'Учебный год')
    semester = models.ForeignKey(Semester, on_delete = models.CASCADE, null = True, blank = True, related_name = 'vacations', verbose_name = 'Связанный семестр')
    description = models.TextField(max_length = 500, blank = True, null = True, verbose_name = 'Описание')
    is_active = models.BooleanField(default = True, verbose_name = 'Актуально')
    
    class Meta:
        db_table = 'List_of_vacations'
        verbose_name = 'Каникулы'
        verbose_name_plural = 'Каникулы'
        ordering = ['start_date']
    
    def __str__(self):
        return f'{self.get_vacation_type_display()} {self.academic_year}'

class Schedule(models.Model):
    group = models.ForeignKey(Group, on_delete = models.CASCADE, verbose_name = 'Группа')
    semester = models.ForeignKey(Semester, on_delete = models.CASCADE, verbose_name = 'Семестр')
    week_start_date = models.DateField(verbose_name = 'Дата начала недели')
    week_end_date = models.DateField(verbose_name = 'Дата окончания недели')
    is_active = models.BooleanField(default = True, verbose_name = 'Актуально')
    is_current_week = models.BooleanField(default = False, verbose_name = 'Текущая неделя')
    note = models.TextField(max_length = 500, blank = True, null = True, verbose_name = 'Примечание к расписанию')
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')
    updated_at = models.DateTimeField(auto_now = True, verbose_name = 'Дата обновления')
    created_by = models.ForeignKey(Professor, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'created_schedules', verbose_name = 'Кто создал')
    
    class Meta:
        db_table = 'List_of_schedule'
        verbose_name = 'Расписание на неделю'
        verbose_name_plural = 'Расписания на неделю'
        ordering = ['-week_start_date', 'group']
        unique_together = ['group', 'week_start_date']
    
    def __str__(self):
        return f'Расписание для {self.group} на неделю {self.week_start_date} - {self.week_end_date}'
    
    def save(self, *args, **kwargs):
        if not self.week_end_date and self.week_start_date:
            self.week_end_date = self.week_start_date + timedelta(days = 6)
        super().save(*args, **kwargs)

class ScheduleReplacement(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete = models.CASCADE, verbose_name = 'Расписание')
    original_date = models.DateField(verbose_name = 'Исходная дата')
    new_date = models.DateField(verbose_name = 'Новая дата')
    original_pair = models.ForeignKey(Pair, on_delete = models.CASCADE, related_name = 'original_replacements', verbose_name = 'Исходная пара')
    new_pair = models.ForeignKey(Pair, on_delete = models.CASCADE, related_name = 'new_replacements', verbose_name = 'Новая пара')
    reason = models.TextField(verbose_name = 'Причина замены')
    created_by = models.ForeignKey(Professor, on_delete = models.SET_NULL, null = True, verbose_name = 'Кто создал')
    created_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = 'List_of_schedule_replacements'
        verbose_name = 'Замена занятия'
        verbose_name_plural = 'Замены занятий'
    
    def __str__(self):
        return f'Замена {self.original_date} -> {self.new_date}'

class Attendance(models.Model):
    presence = 'presence'
    late = 'late'
    absense = 'absence'

    CHOICE_TYPE_PRESENCE = [
        (presence, 'Присутствует'),
        (late, 'Опоздал'),
        (absense, 'Отсутствует')
    ]

    type = models.CharField(max_length = 8, choices = CHOICE_TYPE_PRESENCE, default = presence, verbose_name = 'Состояние студента на паре')
    data_created = models.DateField(auto_now_add = True, verbose_name = 'Дата')
    data_updated = models.DateField(auto_now = True, verbose_name = 'Дата изменяемая')
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete = models.CASCADE, null = True, blank = True, verbose_name = 'Расписание')
    pair = models.ForeignKey(Pair, on_delete = models.CASCADE, null = True, blank = True, verbose_name = 'Пара')

    class Meta:
        db_table = 'List_of_stative_student'
        verbose_name = 'Состояние студента'
        verbose_name_plural = 'Состояние студентов'

    def __str__(self):
        return self.type

class Add_HW_Professor_to_course(models.Model):
    group = models.ForeignKey(Group, on_delete = models.CASCADE, verbose_name = 'Домашнее задание для группы')
    file = models.FileField(unique = True, upload_to = 'static/image/homeworks_for_students/', null = False, blank = False, verbose_name = 'Файл домашнего задания студентам')
    comment = models.TextField(max_length = 500, verbose_name = 'Комментарий студентам к домашнему заданию')
    date_start = models.DateField(auto_now_add = True, help_text = 'Дата создания домашнего задания.', verbose_name = 'Дата создания д/з')
    date_final = models.DateField(help_text = 'Выберите дату конечной сдачи домашнего задания студентам.', verbose_name = 'Конечная дата выполнения')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Задал-(а) домашнее задание')
    subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, verbose_name = 'Предмет')

    class Meta:
        db_table = 'List_of_add_hw_professor_to_course'
        verbose_name = 'Домашнее задание для группы'
        verbose_name_plural = 'Домашние задания для группы'

    def __str__(self):
        return f'Домашнее задание от {self.professor} студентам группы {self.group}'

class balance_topcoins_and_topgems(models.Model):
    topcoins = models.PositiveIntegerField(blank = False, null = False, default = 0, verbose_name = 'Топкоины')
    topgems = models.PositiveIntegerField(blank = False, null = False, default = 0, verbose_name = 'Топгемы')
    student = models.OneToOneField(Student, on_delete = models.CASCADE, verbose_name = 'Студент')

    class Meta:
        db_table = 'List_of_balance_students'
        verbose_name = 'Баланс студента'
        verbose_name_plural = 'Балансы студентов'

    def __str__(self):
        return f'Баланс {self.student}: {self.topcoins} топкоинов, {self.topgems} топгемов'

class Topmoney_student(models.Model):
    topmoney = models.PositiveIntegerField(blank = False, null = False, default = 0, verbose_name = 'Топмани')
    student = models.OneToOneField(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    balance_student = models.OneToOneField(balance_topcoins_and_topgems, on_delete = models.CASCADE, verbose_name = 'Баланс')

    class Meta:
        db_table = 'List_of_topmoney_student'
        verbose_name = 'Топмани студента'
        verbose_name_plural = 'Топмани студентов'

    def save(self, *args, **kwargs):
        if self.balance_student:
            self.topmoney = self.balance_student.topcoins + self.balance_student.topgems
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Топмани студента {self.student}: {self.topmoney}'

class StudentStats(models.Model):
    student = models.OneToOneField(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    total_attendance_days = models.PositiveIntegerField(default = 0, verbose_name = 'Всего дней посещения')
    consecutive_days_attended = models.PositiveIntegerField(default = 0, verbose_name = 'Дней подряд посещения')
    consecutive_days_on_time = models.PositiveIntegerField(default = 0, verbose_name = 'Дней подряд без опозданий')
    last_attendance_date = models.DateField(null = True, blank = True, verbose_name = 'Дата последнего посещения')
    topcoins_awarded_total = models.PositiveIntegerField(default = 0, verbose_name = 'Всего начислено топкоинов')
    topgems_awarded_total = models.PositiveIntegerField(default = 0, verbose_name = 'Всего начислено топгемов')

    class Meta:
        db_table = 'List_of_student_stats'
        verbose_name = 'Статистика студента'
        verbose_name_plural = 'Статистика студентов'

    def __str__(self):
        return f'Статистика {self.student}'

class Reward(models.Model):
    ONE_TIME = 'one_time'
    MULTIPLE = 'multiple'
    REWARD_TYPES = [
        (ONE_TIME, 'Единоразовая'),
        (MULTIPLE, 'Многоразовая'),
    ]
    name = models.CharField(max_length = 100, verbose_name = 'Название награды')
    description = models.TextField(verbose_name = 'Описание')
    reward_type = models.CharField(max_length = 10, choices = REWARD_TYPES, default = ONE_TIME, verbose_name = 'Тип награды')
    topcoins_award = models.PositiveIntegerField(default = 0, verbose_name = 'Топкоины за награду')
    topgems_award = models.PositiveIntegerField(default = 0, verbose_name = 'Топгемы за награду')
    condition_attendance_streak = models.PositiveIntegerField(null = True, blank = True, verbose_name = 'Необходимый непрерывный срок посещения (дней)')
    condition_on_time_streak = models.PositiveIntegerField(null = True, blank = True, verbose_name = 'Необходимый непрерывный срок без опозданий (дней)')
    is_active = models.BooleanField(default = True, verbose_name = 'Активна')

    class Meta:
        db_table = 'List_of_rewards'
        verbose_name = 'Награда'
        verbose_name_plural = 'Награды'

    def __str__(self):
        return self.name

class UserReward(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    reward = models.ForeignKey(Reward, on_delete = models.CASCADE, verbose_name = 'Награда')
    awarded_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата получения')
    topcoins_given = models.PositiveIntegerField(verbose_name = 'Выдано топкоинов')
    topgems_given = models.PositiveIntegerField(verbose_name = 'Выдано топгемов')

    class Meta:
        db_table = 'List_of_user_rewards'
        verbose_name = 'Награда студента'
        verbose_name_plural = 'Награды студентов'

    def __str__(self):
        return f'{self.student} получил {self.reward}'

class Exam(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, verbose_name = 'Предмет')
    schedule = models.ForeignKey(Schedule, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Связанное расписание')
    exam_file = models.FileField(upload_to = 'static/image/exams/', blank = True, null = True, verbose_name = 'Файл работы экзамена')
    grade = models.IntegerField(choices = [(2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name = 'Оценка за экзамен')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Преподаватель')
    exam_date = models.DateField(verbose_name = 'Дата проведения экзамена')
    semester = models.ForeignKey(Semester, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Семестр')

    class Meta:
        db_table = 'List_of_exams'
        verbose_name = 'Экзамен'
        verbose_name_plural = 'Экзамены'

    def __str__(self):
        return f'Экзамен по {self.subject} у {self.student}'

class ExamSession(models.Model):
    semester = models.ForeignKey(Semester, on_delete = models.CASCADE, verbose_name = 'Семестр')
    name = models.CharField(max_length = 100, verbose_name = 'Название сессии')
    start_date = models.DateField(verbose_name = 'Начало сессии')
    end_date = models.DateField(verbose_name = 'Конец сессии')
    is_active = models.BooleanField(default = False, verbose_name = 'Активна')
    
    class Meta:
        db_table = 'List_of_exam_sessions'
        verbose_name = 'Экзаменационная сессия'
        verbose_name_plural = 'Экзаменационные сессии'
    
    def __str__(self):
        return f'{self.name} - {self.semester}'

class ScheduledExam(models.Model):
    exam_name = models.CharField(max_length = 200, verbose_name = 'Название экзамена')
    subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, verbose_name = 'Предмет')
    preliminary_date = models.DateField(verbose_name = 'Предварительная дата проведения')
    group = models.ForeignKey(Group, on_delete = models.CASCADE, verbose_name = 'Группа')
    exam_session = models.ForeignKey(ExamSession, on_delete = models.CASCADE, verbose_name = 'Экзаменационная сессия')
    created_by = models.ForeignKey(Professor, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Куратор')
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')

    class Meta:
        db_table = 'List_of_scheduled_exams'
        verbose_name = 'Назначенный экзамен'
        verbose_name_plural = 'Назначенные экзамены'

    def __str__(self):
        return f'{self.exam_name} - {self.preliminary_date}'

class Announcement(models.Model):
    title = models.CharField(max_length = 200, verbose_name = 'Название объявления')
    date_added = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата добавления')
    photo = models.ImageField(upload_to = 'static/image/announcements/', blank = True, null = True, verbose_name = 'Фото для объявления')
    description = models.TextField(verbose_name = 'Подробное описание объявления')
    is_active = models.BooleanField(default = True, verbose_name = 'Активно')
    groups = models.ManyToManyField(Group, blank = True, verbose_name = 'Для групп')
    is_for_all = models.BooleanField(default = False, verbose_name = 'Для всех')

    class Meta:
        db_table = 'List_of_announcements'
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title

class LeaderboardEntry(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    topmoney = models.PositiveIntegerField(verbose_name = 'Топмани студента')
    group = models.ForeignKey(Group, on_delete = models.CASCADE, verbose_name = 'Группа')
    semester = models.ForeignKey(Semester, on_delete = models.CASCADE, verbose_name = 'Семестр')
    rank_in_group = models.PositiveIntegerField(verbose_name = 'Место в группе')
    rank_in_course = models.PositiveIntegerField(verbose_name = 'Место на курсе')
    date = models.DateField(auto_now_add = True, verbose_name = 'Дата обновления')

    class Meta:
        db_table = 'List_of_leaderboard'
        verbose_name = 'Таблица лидеров'
        verbose_name_plural = 'Таблицы лидеров'
        ordering = ['rank_in_group']

    def __str__(self):
        return f'{self.student} - {self.topmoney} топмани'

class Ranking(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    semester = models.ForeignKey(Semester, on_delete = models.CASCADE, verbose_name = 'Семестр')
    group_rank = models.PositiveIntegerField(verbose_name = 'Место в группе')
    course_rank = models.PositiveIntegerField(verbose_name = 'Место на курсе')
    average_grade = models.DecimalField(max_digits = 3, decimal_places = 2, null = True, blank = True, verbose_name = 'Средний балл')
    date = models.DateField(auto_now_add = True, verbose_name = 'Дата расчёта')

    class Meta:
        db_table = 'List_of_rankings'
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        ordering = ['group_rank']

    def __str__(self):
        return f'Рейтинг {self.student}: место в группе {self.group_rank}, на курсе {self.course_rank}'

class All_payment_of_education(models.Model):
    year = 'year'
    month = 'month'

    CHOICE_YEAR_OR_MONTH = [
        (year, 'Год'),
        (month, 'Месяц')
    ]

    type_payment = models.CharField(choices = CHOICE_YEAR_OR_MONTH, max_length = 5, default = month, verbose_name = 'Выберите тип оплаты обучения')
    amount = models.PositiveIntegerField(blank = False, null = False, default = None, verbose_name = 'Стоимость')
    group = models.ForeignKey(Group, on_delete = models.CASCADE, verbose_name = 'Группа')
    period_of_study = models.IntegerField(blank = False, null = False, default = 40, verbose_name = 'Период обучения(напишите в месяцах)')
    date = models.DateField(blank = False, null = False, verbose_name = 'Начало обучения')

    class Meta:
        db_table = 'List_of_payment_of_education'
        verbose_name = 'Общие настройки оплаты обучения'
        verbose_name_plural = 'Общие настройки оплаты обучения'

    def __str__(self):
        return f'Группа: {self.group}, Тип обучения: {self.type_payment}'

class Students_payment_account(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    all_payment_of_education = models.ForeignKey(All_payment_of_education, on_delete = models.CASCADE, verbose_name = 'Обучается на')

    date = models.DateField(blank = False, null = False, verbose_name = 'Начало обучения')

    class Meta:
        db_table = 'List_of_students_payment_account'
        verbose_name = 'Оплата обучения'
        verbose_name_plural = 'Оплаты обучений'

    def save(self, *args, **kwargs):
        if self.all_payment_of_education:
            self.date = self.all_payment_of_education.date
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Настройка оплаты обучения у {self.student}'

class PaymentInfo(models.Model):
    payment_account = models.ForeignKey(Students_payment_account, on_delete = models.CASCADE, verbose_name = 'Платежный аккаунт')
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    paid_by = models.CharField(max_length = 150, verbose_name = 'Кто оплатил (ФИО)')
    amount_paid = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = 'Сумма оплаты')
    payment_date = models.DateField(verbose_name = 'Дата оплаты')
    period_start = models.DateField(verbose_name = 'Начало оплачиваемого периода')
    period_end = models.DateField(verbose_name = 'Конец оплачиваемого периода')
    part_number = models.PositiveIntegerField(verbose_name = 'Номер оплаченной части (из общего числа)')
    total_parts = models.PositiveIntegerField(verbose_name = 'Общее количество частей обучения (в месяцах)')
    due_date = models.DateField(verbose_name = 'Крайний срок оплаты')
    comment = models.TextField(blank = True, null = True, verbose_name = 'Комментарий')

    class Meta:
        db_table = 'List_of_payment_info'
        verbose_name = 'Информация об оплате'
        verbose_name_plural = 'Информация об оплатах'

    def __str__(self):
        return f'Оплата {self.student} - {self.payment_date}'

class Debtor(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    payment_info = models.ForeignKey(PaymentInfo, on_delete = models.CASCADE, verbose_name = 'Платеж')
    debt_amount = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = 'Сумма долга')
    due_date = models.DateField(verbose_name = 'Срок оплаты')
    is_paid = models.BooleanField(default = False, verbose_name = 'Оплачено')
    notification_sent = models.BooleanField(default = False, verbose_name = 'Уведомление отправлено')
    
    class Meta:
        db_table = 'List_of_debtors'
        verbose_name = 'Должник'
        verbose_name_plural = 'Должники'
    
    def __str__(self):
        return f'{self.student} - долг {self.debt_amount}'

class Scholarship(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = 'Сумма')
    month = models.DateField(verbose_name = 'Месяц выплаты')
    is_paid = models.BooleanField(default = False, verbose_name = 'Выплачено')
    paid_date = models.DateField(null = True, blank = True, verbose_name = 'Дата выплаты')
    
    class Meta:
        db_table = 'List_of_scholarships'
        verbose_name = 'Стипендия'
        verbose_name_plural = 'Стипендии'
    
    def __str__(self):
        return f'Стипендия {self.student} за {self.month}'

class AcademicDebt(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, verbose_name = 'Предмет')
    semester = models.ForeignKey(Semester, on_delete = models.CASCADE, verbose_name = 'Семестр')
    exam_date = models.DateField(verbose_name = 'Дата пересдачи')
    is_passed = models.BooleanField(default = False, verbose_name = 'Сдано')
    retake_count = models.PositiveIntegerField(default = 1, verbose_name = 'Количество пересдач')
    commission_date = models.DateField(null = True, blank = True, verbose_name = 'Дата комиссии')
    
    class Meta:
        db_table = 'List_of_academic_debts'
        verbose_name = 'Академическая задолженность'
        verbose_name_plural = 'Академические задолженности'
    
    def __str__(self):
        return f'Долг {self.student} по {self.subject}'

class GraduationWork(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    title = models.CharField(max_length = 300, verbose_name = 'Тема работы')
    supervisor = models.ForeignKey(Professor, on_delete = models.CASCADE, related_name = 'supervised_works', verbose_name = 'Руководитель')
    reviewer = models.ForeignKey(Professor, on_delete = models.SET_NULL, null = True, related_name = 'reviewed_works', verbose_name = 'Рецензент')
    defense_date = models.DateField(verbose_name = 'Дата защиты')
    grade = models.IntegerField(null = True, blank = True, verbose_name = 'Оценка')
    file = models.FileField(upload_to = 'static/image/graduation_works/', blank = True, null = True, verbose_name = 'Файл работы')
    
    class Meta:
        db_table = 'List_of_graduation_works'
        verbose_name = 'Дипломная работа'
        verbose_name_plural = 'Дипломные работы'
    
    def __str__(self):
        return f'Диплом {self.student}: {self.title[:50]}'

class Internship(models.Model):
    INTERNSHIP_TYPES = [
        ('educational', 'Учебная практика'),
        ('industrial', 'Производственная практика'),
        ('pre_diploma', 'Преддипломная практика'),
    ]
    
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    internship_type = models.CharField(max_length = 20, choices = INTERNSHIP_TYPES, verbose_name = 'Тип практики')
    organization = models.CharField(max_length = 200, verbose_name = 'Организация')
    start_date = models.DateField(verbose_name = 'Дата начала')
    end_date = models.DateField(verbose_name = 'Дата окончания')
    supervisor = models.ForeignKey(Professor, on_delete = models.SET_NULL, null = True, verbose_name = 'Руководитель от колледжа')
    report_file = models.FileField(upload_to = 'static/image/internships/', blank = True, null = True, verbose_name = 'Отчет')
    grade = models.IntegerField(null = True, blank = True, verbose_name = 'Оценка')
    
    class Meta:
        db_table = 'List_of_internships'
        verbose_name = 'Практика'
        verbose_name_plural = 'Практики'
    
    def __str__(self):
        return f'{self.get_internship_type_display()} {self.student}'

class EducationalMaterial(models.Model):
    title = models.CharField(max_length = 200, verbose_name = 'Название материала')
    file = models.FileField(upload_to = 'static/image/educational_materials/', verbose_name = 'Файл материала')
    description = models.TextField(blank = True, null = True, verbose_name = 'Описание')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Преподаватель')
    groups = models.ManyToManyField(Group, blank = True, verbose_name = 'Для конкретных групп')
    is_public = models.BooleanField(default = False, verbose_name = 'Для всех групп')
    subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, null = True, blank = True, verbose_name = 'Предмет')
    upload_date = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата загрузки')

    class Meta:
        db_table = 'List_of_educational_materials'
        verbose_name = 'Учебный материал'
        verbose_name_plural = 'Учебные материалы'

    def __str__(self):
        return self.title

class PersonalAccount(models.Model):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('professor', 'Преподаватель'),
        ('academic_staff', 'Учебная часть'),
    ]
    user = models.OneToOneField(Autoriz, on_delete = models.CASCADE, verbose_name = 'Пользователь')
    role = models.CharField(max_length = 20, choices = ROLE_CHOICES, verbose_name = 'Роль')
    student_profile = models.OneToOneField(Student, on_delete = models.CASCADE, null = True, blank = True, verbose_name = 'Профиль студента')
    professor_profile = models.OneToOneField(Professor, on_delete = models.CASCADE, null = True, blank = True, verbose_name = 'Профиль преподавателя')
    academic_staff_profile = models.OneToOneField(AcademicStaff, on_delete = models.CASCADE, null = True, blank = True, verbose_name = 'Профиль сотрудника')
    school_certificate = models.FileField(upload_to = 'static/image/personal/student/', blank = True, null = True, verbose_name = 'Аттестат школы (для студента)')
    health_certificate = models.FileField(upload_to = 'static/image/personal/student/', blank = True, null = True, verbose_name = 'Справка 086У (для студента)')
    diploma = models.FileField(upload_to = 'static/image/personal/professor/', blank = True, null = True, verbose_name = 'Диплом (для преподавателя)')
    employment_contract = models.FileField(upload_to = 'static/image/personal/professor/', blank = True, null = True, verbose_name = 'Трудовой договор (для преподавателя)')
    internal_documents = models.FileField(upload_to = 'static/image/personal/staff/', blank = True, null = True, verbose_name = 'Внутренние документы (для учебной части)')
    additional_docs = models.FileField(upload_to = 'static/image/personal/other/', blank = True, null = True, verbose_name = 'Дополнительные документы')

    class Meta:
        db_table = 'List_of_personal_accounts'
        verbose_name = 'Личный кабинет'
        verbose_name_plural = 'Личные кабинеты'

    def __str__(self):
        return f'Личный кабинет {self.user} ({self.get_role_display()})'

class image_student(models.Model):
    photo = models.FileField(blank = False, null = False, verbose_name = 'Загрузить фотографию студента')
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')

    class Meta:
        db_table = 'List_of_image_students'
        verbose_name = 'Фотография студента'
        verbose_name_plural = 'Фотографии студентов'

    def __str__(self):
        return f'Фотография студента {self.student}'

class image_professor(models.Model):
    photo = models.FileField(blank = False, null = False, verbose_name = 'Загрузить фотографию преподавателя')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Преподаватель')

    class Meta:
        db_table = 'List_of_image_professor'
        verbose_name = 'Фотография преподавателя'
        verbose_name_plural = 'Фотографии преподавателей'

    def __str__(self):
        return f'Фотография преподавателя {self.professor}'

class Review_of_the_Academy(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    confirmation_review = models.FileField(blank = False, null = False, verbose_name = 'Загрузить картинку')
    google = 'google'
    yandex = 'yandex'
    zoon = 'zoon'

    CHOICE_A_SOCIAL_NETWORK = [
        (google, 'Гугл'),
        (yandex, 'Яндекс'),
        (zoon, 'Зун'),
    ]

    type_a_social_network = models.CharField(choices = CHOICE_A_SOCIAL_NETWORK, max_length = 6, verbose_name = 'Выберите тип социальной сети')

    class Meta:
        db_table = 'List_of_review_of_the_academy'
        verbose_name = 'Загрузка скриншота для подтверждения отзыва'
        verbose_name_plural = 'Загрузить скриншот для подтверждения отзыва'

    def __str__(self):
        return f'Отзыв об Академии студентом {self.student}'

class Appeals_to_the_educational_unit(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    proposal = 'proposal'
    question_in_the_study_section = 'question_in_the_study_section'
    question_about_payment = 'question_about_payment'
    question_about_homework = 'question_about_homework'
    
    CHOICE_THE_SIGNAL_TYPE = [
        (proposal, 'Предложение'),
        (question_in_the_study_section, 'Вопрос к учебной части'),
        (question_about_payment, 'Вопрос по оплате'),
        (question_about_homework, 'Вопрос по домашнему заданию')
    ]
    
    Select_the_signal_type = models.CharField(choices = CHOICE_THE_SIGNAL_TYPE, max_length = 30, verbose_name = 'Выберите тип сигнала')
    question = models.TextField(max_length = 500, blank = False, null = False, verbose_name = 'Вопрос студента')

    class Meta:
        db_table = 'List_of_appeals_to_the_educatinal_unit'
        verbose_name = 'Вопрос к учебной части'
        verbose_name_plural = 'Вопросы к учебной части'

    def __str__(self):
        return f'Вопрос от студента {self.student}'

class Shop_add_products(models.Model):
    name_product = models.CharField(max_length = 50, blank = False, null = False, verbose_name = 'Название продукта')
    photo_product = models.FileField(blank = False, null = False, verbose_name = 'Фотография продукта')
    product_quantity = models.PositiveIntegerField(blank = False, null = False, verbose_name = 'Количество')
    price_product_topcoins = models.PositiveIntegerField(blank = False, null = False, verbose_name = 'Цена в топкоинах')
    price_product_topgems = models.PositiveIntegerField(blank = False, null = False, verbose_name = 'Цена в топгемах')

    class Meta:
        db_table = 'List_of_shop'
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазин'

    def __str__(self):
        return f'Товар {self.name_product}'

class Complaint_to_the_CEO(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    claim = models.CharField(max_length = 500, blank = False, null = False)
    date = models.DateField(auto_now_add = True)

    class Meta:
        db_table = 'List_of_complaint_to_the_CEO'
        verbose_name = 'Жалоба генеральному директору'
        verbose_name_plural = 'Жалоба генеральному директору'

    def __str__(self):
        return f'Жалоба студента {self.student} генеральному директору.'

class Student_Reviews(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'ФИО студента')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'ФИО преподавателя')
    subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, verbose_name = 'Предмет который ведет преподаватель')
    comment = models.CharField(max_length = 800, blank = False, null = False, verbose_name = 'Текст о студенте')
    date = models.DateField(auto_now_add = True)

    class Meta:
        db_table = 'List_of_student_review'
        verbose_name = 'Отзыв о студенте'
        verbose_name_plural = 'Отзывы о студенте'

    def __str__(self):
        return f'Отзыв о студенте {self.student}.'

class Event(models.Model):
    EVENT_TYPES = [
        ('holiday', 'Праздник'),
        ('exam', 'Экзамен'),
        ('meeting', 'Собрание'),
        ('deadline', 'Дедлайн'),
        ('other', 'Другое'),
    ]
    
    title = models.CharField(max_length = 200, verbose_name = 'Название')
    event_type = models.CharField(max_length = 20, choices = EVENT_TYPES, verbose_name = 'Тип события')
    start_date = models.DateTimeField(verbose_name = 'Дата начала')
    end_date = models.DateTimeField(verbose_name = 'Дата окончания')
    description = models.TextField(blank = True, null = True, verbose_name = 'Описание')
    location = models.CharField(max_length = 200, blank = True, null = True, verbose_name = 'Место')
    groups = models.ManyToManyField(Group, blank = True, verbose_name = 'Для групп')
    is_for_all = models.BooleanField(default = False, verbose_name = 'Для всех')
    created_by = models.ForeignKey(Professor, on_delete = models.SET_NULL, null = True, verbose_name = 'Кто создал')
    
    class Meta:
        db_table = 'List_of_events'
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['start_date']
    
    def __str__(self):
        return self.title

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('info', 'Информация'),
        ('warning', 'Предупреждение'),
        ('success', 'Успех'),
        ('error', 'Ошибка'),
    ]
    
    title = models.CharField(max_length = 200, verbose_name = 'Заголовок')
    message = models.TextField(verbose_name = 'Сообщение')
    notification_type = models.CharField(max_length = 20, choices = NOTIFICATION_TYPES, default = 'info', verbose_name = 'Тип')
    created_at = models.DateTimeField(auto_now_add = True)
    is_read = models.BooleanField(default = False, verbose_name = 'Прочитано')
    user = models.ForeignKey(Autoriz, on_delete = models.CASCADE, verbose_name = 'Пользователь')
    
    class Meta:
        db_table = 'List_of_notifications'
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Poll(models.Model):
    title = models.CharField(max_length = 200, verbose_name = 'Название')
    description = models.TextField(blank = True, null = True, verbose_name = 'Описание')
    start_date = models.DateTimeField(verbose_name = 'Дата начала')
    end_date = models.DateTimeField(verbose_name = 'Дата окончания')
    is_active = models.BooleanField(default = True, verbose_name = 'Активно')
    groups = models.ManyToManyField(Group, blank = True, verbose_name = 'Для групп')
    created_by = models.ForeignKey(Professor, on_delete = models.SET_NULL, null = True, verbose_name = 'Кто создал')
    
    class Meta:
        db_table = 'List_of_polls'
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
    
    def __str__(self):
        return self.title

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete = models.CASCADE, related_name = 'options', verbose_name = 'Опрос')
    text = models.CharField(max_length = 200, verbose_name = 'Вариант ответа')
    votes = models.PositiveIntegerField(default = 0, verbose_name = 'Голосов')
    
    class Meta:
        db_table = 'List_of_poll_options'
        verbose_name = 'Вариант опроса'
        verbose_name_plural = 'Варианты опросов'
    
    def __str__(self):
        return self.text

class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete = models.CASCADE, verbose_name = 'Опрос')
    option = models.ForeignKey(PollOption, on_delete = models.CASCADE, verbose_name = 'Вариант')
    user = models.ForeignKey(Autoriz, on_delete = models.CASCADE, verbose_name = 'Пользователь')
    voted_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = 'List_of_poll_votes'
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
        unique_together = ['poll', 'user']

class Chat(models.Model):
    participants = models.ManyToManyField(Autoriz, verbose_name = 'Участники')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'List_of_chats'
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
    
    def __str__(self):
        return f'Чат {self.id}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE, related_name = 'messages', verbose_name = 'Чат')
    sender = models.ForeignKey(Autoriz, on_delete = models.CASCADE, verbose_name = 'Отправитель')
    text = models.TextField(verbose_name = 'Текст сообщения')
    file = models.FileField(upload_to = 'static/image/messages/', blank = True, null = True, verbose_name = 'Файл')
    is_read = models.BooleanField(default = False, verbose_name = 'Прочитано')
    created_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = 'List_of_messages'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']
    
    def __str__(self):
        return f'Сообщение от {self.sender} в {self.created_at}'