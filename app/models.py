from django.db import models

# Имя, пароль и почта от аккаунта.
class Autoriz(models.Model):
    user = models.CharField(unique = True, max_length = 30, blank = False, null = True, error_messages = {'max_length': 'Длина имени не может содержать более 30 символов', 'blank': 'Напишите имя.', 'null': 'Напишите имя.'}, verbose_name = 'Имя аккаунта')
    password = models.CharField(max_length = 120, blank = False, null = False, error_messages = {'max_length': 'Длина пароля не может содержать более 40 символов', 'blank': 'Напишите пароль.', 'null': 'Напишите пароль.'}, verbose_name = 'Пароль от аккаунта')
    email = models.EmailField(unique = True, max_length=100, blank = False, null = False, error_messages = {'max_length': 'Длина почты не может содержать более 100 символов', 'blank': 'Напишите почту.', 'null': 'Напишите почту.'}, verbose_name = 'Почта от аккаунта')

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
    leads_the_subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, verbose_name = 'Ведет предмет:')
    autoriz = models.ForeignKey(Autoriz, on_delete = models.CASCADE, verbose_name = 'Пользователь')

    class Meta:
        db_table = 'List_of_professors'
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return self.name

class Courses_of_Students(models.Model):
    course = models.CharField(max_length = 40, blank = False, null = False, help_text = '( Курс, группа и название направления пишите в формате: 1/4РПО )', verbose_name = 'Курс')
    
    class Meta:
        db_table = 'List_of_courses_of_students'
        verbose_name = 'Курс студента'
        verbose_name_plural = 'Курс студентов'

    def __str__(self):
        return self.course

# ФИО и группа студента.
class Student(models.Model):
    name = models.CharField(max_length = 30, blank = False, null = False, verbose_name = 'Имя студента')
    surname = models.CharField(max_length = 30, blank = False, null = False, verbose_name = 'Фамилия студента')
    patronymic = models.CharField(max_length = 40, blank = False, null = False, verbose_name = 'Отчество студента')
    autoriz = models.ForeignKey(Autoriz, on_delete = models.CASCADE, verbose_name = 'Пользователь')
    courses_of_students = models.ForeignKey(Courses_of_Students, on_delete = models.CASCADE, null = True, blank = True, verbose_name = 'Обучается на курсе')

    class Meta:
        db_table = 'List_of_students'
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
         return f"{self.surname} {self.name[0]}. {self.patronymic[0]}."

class Marks(models.Model):
    marks = models.IntegerField(blank = False, null = True, verbose_name = 'Оценки студента')

# Типы работ(Домашние задания, лабораторные, контрольные и т.п.)
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

# Состояние студента на паре.
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
    data_created = models.DateField(auto_now_add = True, verbose_name = 'Дата') # Дата которая создается автоматически.
    data_updated = models.DateField(auto_now = True, verbose_name = 'Дата изменяемая') # Если преподаватель ошибочно отметил присутствие/отсутсвие студенту, здесь выставляется правильная дата вручную.
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = 'List_of_stative_student'
        verbose_name = 'Состояние студента'
        verbose_name_plural = 'Состояние студентов'

    def __str__(self):
        return self.type

class Add_HW_Professor(models.Model):
    file = models.FileField(upload_to = 'static/image/homeworks_for_students/', null = False, blank = False, verbose_name = 'Файл домашнего задания студентам')
    comment = models.TextField(max_length = 500, verbose_name = 'Комментарий домашнему заданию')
    date = models.DateField(help_text = 'Выберите дату конечной сдачи домашнего задания студентам.', verbose_name = 'Конечная дата выполнения')

class Information_about_HW_for_students(models.Model):
    issued = models.DateField(auto_now_add = True, verbose_name = 'Дата выдачи домашнего задания')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Преподаватель')
    add_hw_professor = models.ForeignKey(Add_HW_Professor, on_delete = models.CASCADE, verbose_name = 'Добавить домашку')

class balance_topcoins_and_topgems(models.Model):
    topcoins = models.PositiveSmallIntegerField(blank = False, null = False, default = None, verbose_name = 'Топкоины')
    topgems = models.PositiveSmallIntegerField(blank = False, null = False, default = None, verbose_name = 'Топгемы')
    student = models.OneToOneField(Student, on_delete=models.CASCADE, verbose_name = 'Студент')

    class Meta:
        db_table = 'List_of_balance_students'
        verbose_name = 'Баланс студента'
        verbose_name_plural = 'Балансы студентов'

    def __str__(self):
        return "Баланс топгемов и топкоинов студента"

# Модель для создания счетов для видов обучения для разных направлений на месяц/год.
class All_payment_of_education(models.Model):
    year = 'year'
    month = 'month'

    CHOICE_YEAR_OR_MONTH = [
        (year, 'Год'),
        (month, 'Месяц')
    ]
    
    CHOICE_MONTH = [
        (1, 'Январь'),
        (2, 'Февраль'),
        (3, 'Март'),
        (4, 'Апрель'),
        (5, 'Май'),
        (6, 'Июнь'),
        (7, 'Июль'),
        (8, 'Август'),
        (9, 'Сентябрь'),
        (10, 'Октябрь'),
        (11, 'Ноябрь'),
        (12, 'Декабрь'),
    ]

    CHOICE_YEAR = [
        (1, '2026'),
        (2, '2027'),
        (3, '2028'),
        (4, '2029'),
        (5, '2030'),
        (6, '2031'),
        (7, '2032'),
        (8, '2033'),
        (9, '2034'),
        (10, '2035'),
    ]

    type = models.CharField(choices = CHOICE_YEAR_OR_MONTH, max_length = 5, default = month, verbose_name = 'Выберите тип оплаты обучения')
    amount = models.PositiveIntegerField(blank = False, null = False, default = None, verbose_name = 'Стоимость')
    courses_of_Students = models.ForeignKey(Courses_of_Students, on_delete = models.CASCADE, verbose_name = 'Курс')
    period_of_study = models.IntegerField(blank = False, null = False, default = 40, verbose_name = 'Период обучения(напишите в месяцах)')
    month_of_payment = models.IntegerField(choices = CHOICE_MONTH, verbose_name = 'Месяц', help_text = 'Начало обучения')
    year_of_payment = models.IntegerField(choices = CHOICE_YEAR, verbose_name = 'Год', help_text = 'Начало обучения')


    class Meta:
        db_table = 'List_of_payment_of_education'
        verbose_name = 'Общие настройки оплаты обучения'
        verbose_name_plural = 'Общие настройки оплаты обучения'

    def __str__(self):
        return f'Курс: {self.courses_of_Students}, Тип обучения: {self.type}'
    
# Модель состояния оплаты для платежей студента.
class Status_of_payment_of_education(models.Model):
    paid_for = 'paid_for'
    not_paid_for = 'not_paid_for'
    
    CHOICE_STATE_OF_PAYMENT = [
        (paid_for, 'Оплачено'),
        (not_paid_for, 'Не оплачено')
    ]

    type = models.CharField(choices = CHOICE_STATE_OF_PAYMENT, max_length = 12, default = not_paid_for, verbose_name = 'Статус оплаты')
    
# Модель для подкрепления созданного счета к аккаунту студента.
class Students_payment_account(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    all_payment_of_education = models.ForeignKey(All_payment_of_education, on_delete = models.CASCADE, verbose_name = 'Обучается в:')
    
    CHOICE_MONTH = [
        (1, 'Январь'),
        (2, 'Февраль'),
        (3, 'Март'),
        (4, 'Апрель'),
        (5, 'Май'),
        (6, 'Июнь'),
        (7, 'Июль'),
        (8, 'Август'),
        (9, 'Сентябрь'),
        (10, 'Октябрь'),
        (11, 'Ноябрь'),
        (12, 'Декабрь'),
    ]

    CHOICE_YEAR = [
        (1, '2026'),
        (2, '2027'),
        (3, '2028'),
        (4, '2029'),
        (5, '2030'),
        (6, '2031'),
        (7, '2032'),
        (8, '2033'),
        (9, '2034'),
        (10, '2035'),
    ]

    month_of_payment = models.IntegerField(choices = CHOICE_MONTH, verbose_name = 'Месяц')
    year_of_payment = models.IntegerField(choices = CHOICE_YEAR, verbose_name = 'Год')

    class Meta:
        db_table = 'List_of_students_payment_account'
        verbose_name = 'Оплата обучения'
        verbose_name_plural = 'Оплаты обучений'

    def __str__(self):
        return f'Настройка оплаты обучения у {self.student}'