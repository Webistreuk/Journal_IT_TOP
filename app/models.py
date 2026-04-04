from django.db import models
from multiselectfield import MultiSelectField
from datetime import timedelta
from django.utils import timezone

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
    leads_the_subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, verbose_name = 'Ведет предмет')
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
    type_estimation = models.IntegerField(choices = CHOICE_OF_ESTIMATION, blank = False, null = False, verbose_name = 'Оценка студенту')

class Add_Сlassroom(models.Model):
    name_classroom = models.CharField(unique = True, blank = False, null = False, verbose_name = 'Название аудитории')

    class Meta:
        db_table = 'List_of_Add_classroom'
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'

    def __str__(self):
        return self.name_classroom


class First_pair(models.Model):
    the_first_pair_of_the_day = 'the_first_pair_of_the_day'

    CHOICE_OF_THE_PAIR = [
        (the_first_pair_of_the_day, '08:30-09:50')
    ]

    type_pair = models.CharField(max_length = 35, choices = CHOICE_OF_THE_PAIR, verbose_name = 'Пара в', default = the_first_pair_of_the_day)
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Подключение')
    professor_name = models.CharField(max_length = 40, verbose_name = 'Преподаватель')
    professor_surname = models.CharField(max_length = 40, verbose_name = 'Фамилия преподавателя')
    professor_patronymic = models.CharField(max_length = 40, verbose_name = 'Отчество преподавателя')
    subject = models.CharField(max_length = 80, verbose_name = 'Предмет который он-(а) ведет')
    classroom = models.ForeignKey(Add_Сlassroom, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Аудитория')
    classroom_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = 'Название аудитории')

    class Meta:
        db_table = 'List_of_first_pair'
        verbose_name = 'Первая пара'
        verbose_name_plural = 'Первая пара'

    def save(self, *args, **kwargs):
        if self.professor:
            self.professor_name = self.professor.name
            self.professor_surname = self.professor.surname
            self.professor_patronymic = self.professor.patronymic
            self.subject = self.professor.leads_the_subject
        if self.classroom:
            self.classroom_name = self.classroom.name_classroom
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Первая пара у преподавателя {self.professor_surname} {self.professor_name[0]}. {self.professor_patronymic[0]}., предмет: {self.subject}, аудитория: {self.classroom_name}'

class Second_pair(models.Model):
    the_second_pair_of_the_day = 'the_second_pair_of_the_day'

    CHOICE_OF_THE_PAIR = [
        (the_second_pair_of_the_day, '10:00-11:20'),
    ]

    type_pair = models.CharField(max_length = 35, choices = CHOICE_OF_THE_PAIR, verbose_name = 'Пара в', default = the_second_pair_of_the_day)
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Подключение')
    professor_name = models.CharField(max_length = 40, verbose_name = 'Преподаватель')
    professor_surname = models.CharField(max_length = 40, verbose_name = 'Фамилия преподавателя')
    professor_patronymic = models.CharField(max_length = 40, verbose_name = 'Отчество преподавателя')
    subject = models.CharField(max_length = 80, verbose_name = 'Предмет который он-(а) ведет')
    classroom = models.ForeignKey(Add_Сlassroom, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Аудитория')
    classroom_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = 'Название аудитории')

    class Meta:
        db_table = 'List_of_second_pair'
        verbose_name = 'Вторая пара'
        verbose_name_plural = 'Вторая пара'

    def save(self, *args, **kwargs):
        if self.professor:
            self.professor_name = self.professor.name
            self.professor_surname = self.professor.surname
            self.professor_patronymic = self.professor.patronymic
            self.subject = self.professor.leads_the_subject
        if self.classroom:
            self.classroom_name = self.classroom.name_classroom
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Вторая пара у преподавателя {self.professor_surname} {self.professor_name[0]}. {self.professor_patronymic[0]}., предмет: {self.subject}, аудитория: {self.classroom_name}'

class Third_pair(models.Model):
    the_third_pair_of_the_day = 'the_third_pair_of_the_day'

    CHOICE_OF_THE_PAIR = [
        (the_third_pair_of_the_day, '11:50-13:10'),
    ]

    type_pair = models.CharField(max_length = 35, choices = CHOICE_OF_THE_PAIR, verbose_name = 'Пара в', default = the_third_pair_of_the_day)
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Подключение')
    professor_name = models.CharField(max_length = 40, verbose_name = 'Преподаватель')
    professor_surname = models.CharField(max_length = 40, verbose_name = 'Фамилия преподавателя')
    professor_patronymic = models.CharField(max_length = 40, verbose_name = 'Отчество преподавателя')
    subject = models.CharField(max_length = 80, verbose_name = 'Предмет который он-(а) ведет')
    classroom = models.ForeignKey(Add_Сlassroom, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Аудитория')
    classroom_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = 'Название аудитории')

    class Meta:
        db_table = 'List_of_third_pair'
        verbose_name = 'Третья пара'
        verbose_name_plural = 'Третья пара'

    def save(self, *args, **kwargs):
        if self.professor:
            self.professor_name = self.professor.name
            self.professor_surname = self.professor.surname
            self.professor_patronymic = self.professor.patronymic
            self.subject = self.professor.leads_the_subject
        if self.classroom:
            self.classroom_name = self.classroom.name_classroom
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Третья пара у преподавателя {self.professor_surname} {self.professor_name[0]}. {self.professor_patronymic[0]}., предмет: {self.subject}, аудитория: {self.classroom_name}'

class Fourth_pair(models.Model):
    the_fourth_pair_of_the_day = 'the_fourth_pair_of_the_day'

    CHOICE_OF_THE_PAIR = [
        (the_fourth_pair_of_the_day, '13:20-14:40'),
    ]

    type_pair = models.CharField(max_length = 35, choices = CHOICE_OF_THE_PAIR, verbose_name = 'Пара в', default = the_fourth_pair_of_the_day)
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Подключение')
    professor_name = models.CharField(max_length = 40, verbose_name = 'Преподаватель')
    professor_surname = models.CharField(max_length = 40, verbose_name = 'Фамилия преподавателя')
    professor_patronymic = models.CharField(max_length = 40, verbose_name = 'Отчество преподавателя')
    subject = models.CharField(max_length = 80, verbose_name = 'Предмет который он-(а) ведет')
    classroom = models.ForeignKey(Add_Сlassroom, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Аудитория')
    classroom_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = 'Название аудитории')

    class Meta:
        db_table = 'List_of_fourth_pair'
        verbose_name = 'Четвертая пара'
        verbose_name_plural = 'Четвертая пара'

    def save(self, *args, **kwargs):
        if self.professor:
            self.professor_name = self.professor.name
            self.professor_surname = self.professor.surname
            self.professor_patronymic = self.professor.patronymic
            self.subject = self.professor.leads_the_subject
        if self.classroom:
            self.classroom_name = self.classroom.name_classroom
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Четвертая пара у преподавателя {self.professor_surname} {self.professor_name[0]}. {self.professor_patronymic[0]}., предмет: {self.subject}, аудитория: {self.classroom_name}'

class Fifth_pair(models.Model):
    the_fifth_pair_of_the_day = 'the_fifth_pair_of_the_day'

    CHOICE_OF_THE_PAIR = [
        (the_fifth_pair_of_the_day, '14:50-16:10'),
    ]

    type_pair = models.CharField(max_length = 35, choices = CHOICE_OF_THE_PAIR, verbose_name = 'Пара в', default = the_fifth_pair_of_the_day)
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Подключение')
    professor_name = models.CharField(max_length = 40, verbose_name = 'Преподаватель')
    professor_surname = models.CharField(max_length = 40, verbose_name = 'Фамилия преподавателя')
    professor_patronymic = models.CharField(max_length = 40, verbose_name = 'Отчество преподавателя')
    subject = models.CharField(max_length = 80, verbose_name = 'Предмет который он-(а) ведет')
    classroom = models.ForeignKey(Add_Сlassroom, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Аудитория')
    classroom_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = 'Название аудитории')

    class Meta:
        db_table = 'List_of_fifth_pair'
        verbose_name = 'Пятая пара'
        verbose_name_plural = 'Пятая пара'

    def save(self, *args, **kwargs):
        if self.professor:
            self.professor_name = self.professor.name
            self.professor_surname = self.professor.surname
            self.professor_patronymic = self.professor.patronymic
            self.subject = self.professor.leads_the_subject
        if self.classroom:
            self.classroom_name = self.classroom.name_classroom
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Пятая пара у преподавателя {self.professor_surname} {self.professor_name[0]}. {self.professor_patronymic[0]}., предмет: {self.subject}, аудитория: {self.classroom_name}'

class Sixth_pair(models.Model):
    the_sixth_pair_of_the_day = 'the_sixth_pair_of_the_day'

    CHOICE_OF_THE_PAIR = [
        (the_sixth_pair_of_the_day, '16:20-17:40'),
    ]

    type_pair = models.CharField(max_length = 35, choices = CHOICE_OF_THE_PAIR, verbose_name = 'Пара в', default = the_sixth_pair_of_the_day)
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Подключение')
    professor_name = models.CharField(max_length = 40, verbose_name = 'Преподаватель')
    professor_surname = models.CharField(max_length = 40, verbose_name = 'Фамилия преподавателя')
    professor_patronymic = models.CharField(max_length = 40, verbose_name = 'Отчество преподавателя')
    subject = models.CharField(max_length = 80, verbose_name = 'Предмет который он-(а) ведет')
    classroom = models.ForeignKey(Add_Сlassroom, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Аудитория')
    classroom_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = 'Название аудитории')

    class Meta:
        db_table = 'List_of_sixth_pair'
        verbose_name = 'Шестая пара'
        verbose_name_plural = 'Шестая пара'

    def save(self, *args, **kwargs):
        if self.professor:
            self.professor_name = self.professor.name
            self.professor_surname = self.professor.surname
            self.professor_patronymic = self.professor.patronymic
            self.subject = self.professor.leads_the_subject
        if self.classroom:
            self.classroom_name = self.classroom.name_classroom
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Шестая пара у преподавателя {self.professor_surname} {self.professor_name[0]}. {self.professor_patronymic[0]}., предмет: {self.subject}, аудитория: {self.classroom_name}'

class Seventh_pair(models.Model):
    the_seventh_pair_of_the_day = 'the_seventh_pair_of_the_day'

    CHOICE_OF_THE_PAIR = [
        (the_seventh_pair_of_the_day, '17:50-19:10')
    ]

    type_pair = models.CharField(max_length = 35, choices = CHOICE_OF_THE_PAIR, verbose_name = 'Пара в', default = the_seventh_pair_of_the_day)
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Подключение')
    professor_name = models.CharField(max_length = 40, verbose_name = 'Преподаватель')
    professor_surname = models.CharField(max_length = 40, verbose_name = 'Фамилия преподавателя')
    professor_patronymic = models.CharField(max_length = 40, verbose_name = 'Отчество преподавателя')
    subject = models.CharField(max_length = 80, verbose_name = 'Предмет который он-(а) ведет')
    classroom = models.ForeignKey(Add_Сlassroom, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Аудитория')
    classroom_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = 'Название аудитории')

    class Meta:
        db_table = 'List_of_seventh_pair'
        verbose_name = 'Седьмая пара'
        verbose_name_plural = 'Седьмая пара'

    def save(self, *args, **kwargs):
        if self.professor:
            self.professor_name = self.professor.name
            self.professor_surname = self.professor.surname
            self.professor_patronymic = self.professor.patronymic
            self.subject = self.professor.leads_the_subject
        if self.classroom:
            self.classroom_name = self.classroom.name_classroom
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Седьмая пара у преподавателя {self.professor_surname} {self.professor_name[0]}. {self.professor_patronymic[0]}., предмет: {self.subject}, аудитория: {self.classroom_name}'

class Mondays_schedule(models.Model):
    first_pair = models.ForeignKey(First_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Первая пара (08:30-09:50)')
    second_pair = models.ForeignKey(Second_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Вторая пара (10:00-11:20)')
    third_pair = models.ForeignKey(Third_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Третья пара (11:50-13:10)')
    fourth_pair = models.ForeignKey(Fourth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Четвертая пара (13:20-14:40)')
    fifth_pair = models.ForeignKey(Fifth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Пятая пара (14:50-16:10)')
    sixth_pair = models.ForeignKey(Sixth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Шестая пара (16:20-17:40)')
    seventh_pair = models.ForeignKey(Seventh_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Седьмая пара (17:50-19:10)')
    
    class Meta:
        db_table = 'List_of_mondays_schedule'
        verbose_name = 'Расписание на понедельник'
        verbose_name_plural = 'Расписание на понедельник'
    
    def __str__(self):
        pairs = []
        if self.first_pair:
            pairs.append(str(self.first_pair))
        if self.second_pair:
            pairs.append(str(self.second_pair))
        if self.third_pair:
            pairs.append(str(self.third_pair))
        if self.fourth_pair:
            pairs.append(str(self.fourth_pair))
        if self.fifth_pair:
            pairs.append(str(self.fifth_pair))
        if self.sixth_pair:
            pairs.append(str(self.sixth_pair))
        if self.seventh_pair:
            pairs.append(str(self.seventh_pair))
        
        if pairs:
            return f'Понедельник: {", ".join(pairs)}'
        return 'Понедельник: нет пар.'

class Tuesdays_schedule(models.Model):
    first_pair = models.ForeignKey(First_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Первая пара (08:30-09:50)')
    second_pair = models.ForeignKey(Second_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Вторая пара (10:00-11:20)')
    third_pair = models.ForeignKey(Third_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Третья пара (11:50-13:10)')
    fourth_pair = models.ForeignKey(Fourth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Четвертая пара (13:20-14:40)')
    fifth_pair = models.ForeignKey(Fifth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Пятая пара (14:50-16:10)')
    sixth_pair = models.ForeignKey(Sixth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Шестая пара (16:20-17:40)')
    seventh_pair = models.ForeignKey(Seventh_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Седьмая пара (17:50-19:10)')
    
    class Meta:
        db_table = 'List_of_tuesdays_schedule'
        verbose_name = 'Расписание на вторник'
        verbose_name_plural = 'Расписание на вторник'
    
    def __str__(self):
        pairs = []
        if self.first_pair:
            pairs.append(str(self.first_pair))
        if self.second_pair:
            pairs.append(str(self.second_pair))
        if self.third_pair:
            pairs.append(str(self.third_pair))
        if self.fourth_pair:
            pairs.append(str(self.fourth_pair))
        if self.fifth_pair:
            pairs.append(str(self.fifth_pair))
        if self.sixth_pair:
            pairs.append(str(self.sixth_pair))
        if self.seventh_pair:
            pairs.append(str(self.seventh_pair))
        
        if pairs:
            return f'Вторник: {", ".join(pairs)}'
        return 'Вторник: нет пар.'

class Wednesdays_schedule(models.Model):
    first_pair = models.ForeignKey(First_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Первая пара (08:30-09:50)')
    second_pair = models.ForeignKey(Second_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Вторая пара (10:00-11:20)')
    third_pair = models.ForeignKey(Third_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Третья пара (11:50-13:10)')
    fourth_pair = models.ForeignKey(Fourth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Четвертая пара (13:20-14:40)')
    fifth_pair = models.ForeignKey(Fifth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Пятая пара (14:50-16:10)')
    sixth_pair = models.ForeignKey(Sixth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Шестая пара (16:20-17:40)')
    seventh_pair = models.ForeignKey(Seventh_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Седьмая пара (17:50-19:10)')
    
    class Meta:
        db_table = 'List_of_wednesdays_schedule'
        verbose_name = 'Расписание на среду'
        verbose_name_plural = 'Расписание на среду'
    
    def __str__(self):
        pairs = []
        if self.first_pair:
            pairs.append(str(self.first_pair))
        if self.second_pair:
            pairs.append(str(self.second_pair))
        if self.third_pair:
            pairs.append(str(self.third_pair))
        if self.fourth_pair:
            pairs.append(str(self.fourth_pair))
        if self.fifth_pair:
            pairs.append(str(self.fifth_pair))
        if self.sixth_pair:
            pairs.append(str(self.sixth_pair))
        if self.seventh_pair:
            pairs.append(str(self.seventh_pair))
        
        if pairs:
            return f'Среда: {", ".join(pairs)}'
        return 'Среда: нет пар.'

class Thursdays_schedule(models.Model):
    first_pair = models.ForeignKey(First_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Первая пара (08:30-09:50)')
    second_pair = models.ForeignKey(Second_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Вторая пара (10:00-11:20)')
    third_pair = models.ForeignKey(Third_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Третья пара (11:50-13:10)')
    fourth_pair = models.ForeignKey(Fourth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Четвертая пара (13:20-14:40)')
    fifth_pair = models.ForeignKey(Fifth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Пятая пара (14:50-16:10)')
    sixth_pair = models.ForeignKey(Sixth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Шестая пара (16:20-17:40)')
    seventh_pair = models.ForeignKey(Seventh_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Седьмая пара (17:50-19:10)')
    
    class Meta:
        db_table = 'List_of_thursdays_schedule'
        verbose_name = 'Расписание на четверг'
        verbose_name_plural = 'Расписание на четверг'
    
    def __str__(self):
        pairs = []
        if self.first_pair:
            pairs.append(str(self.first_pair))
        if self.second_pair:
            pairs.append(str(self.second_pair))
        if self.third_pair:
            pairs.append(str(self.third_pair))
        if self.fourth_pair:
            pairs.append(str(self.fourth_pair))
        if self.fifth_pair:
            pairs.append(str(self.fifth_pair))
        if self.sixth_pair:
            pairs.append(str(self.sixth_pair))
        if self.seventh_pair:
            pairs.append(str(self.seventh_pair))
        
        if pairs:
            return f'Четверг: {", ".join(pairs)}'
        return 'Четверг: нет пар.'

class Fridays_schedule(models.Model):
    first_pair = models.ForeignKey(First_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Первая пара (08:30-09:50)')
    second_pair = models.ForeignKey(Second_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Вторая пара (10:00-11:20)')
    third_pair = models.ForeignKey(Third_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Третья пара (11:50-13:10)')
    fourth_pair = models.ForeignKey(Fourth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Четвертая пара (13:20-14:40)')
    fifth_pair = models.ForeignKey(Fifth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Пятая пара (14:50-16:10)')
    sixth_pair = models.ForeignKey(Sixth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Шестая пара (16:20-17:40)')
    seventh_pair = models.ForeignKey(Seventh_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Седьмая пара (17:50-19:10)')
    
    class Meta:
        db_table = 'List_of_fridays_schedule'
        verbose_name = 'Расписание на пятницу'
        verbose_name_plural = 'Расписание на пятницу'
    
    def __str__(self):
        pairs = []
        if self.first_pair:
            pairs.append(str(self.first_pair))
        if self.second_pair:
            pairs.append(str(self.second_pair))
        if self.third_pair:
            pairs.append(str(self.third_pair))
        if self.fourth_pair:
            pairs.append(str(self.fourth_pair))
        if self.fifth_pair:
            pairs.append(str(self.fifth_pair))
        if self.sixth_pair:
            pairs.append(str(self.sixth_pair))
        if self.seventh_pair:
            pairs.append(str(self.seventh_pair))
        
        if pairs:
            return f'Пятница: {", ".join(pairs)}'
        return 'Пятница: нет пар.'

class Saturdays_schedule(models.Model):
    first_pair = models.ForeignKey(First_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Первая пара (08:30-09:50)')
    second_pair = models.ForeignKey(Second_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Вторая пара (10:00-11:20)')
    third_pair = models.ForeignKey(Third_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Третья пара (11:50-13:10)')
    fourth_pair = models.ForeignKey(Fourth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Четвертая пара (13:20-14:40)')
    fifth_pair = models.ForeignKey(Fifth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Пятая пара (14:50-16:10)')
    sixth_pair = models.ForeignKey(Sixth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Шестая пара (16:20-17:40)')
    seventh_pair = models.ForeignKey(Seventh_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Седьмая пара (17:50-19:10)')
    
    class Meta:
        db_table = 'List_of_saturdays_schedule'
        verbose_name = 'Расписание на субботу'
        verbose_name_plural = 'Расписание на субботу'
    
    def __str__(self):
        pairs = []
        if self.first_pair:
            pairs.append(str(self.first_pair))
        if self.second_pair:
            pairs.append(str(self.second_pair))
        if self.third_pair:
            pairs.append(str(self.third_pair))
        if self.fourth_pair:
            pairs.append(str(self.fourth_pair))
        if self.fifth_pair:
            pairs.append(str(self.fifth_pair))
        if self.sixth_pair:
            pairs.append(str(self.sixth_pair))
        if self.seventh_pair:
            pairs.append(str(self.seventh_pair))
        
        if pairs:
            return f'Суббота: {", ".join(pairs)}'
        return 'Суббота: нет пар.'

class Sundays_schedule(models.Model):
    first_pair = models.ForeignKey(First_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Первая пара (08:30-09:50)')
    second_pair = models.ForeignKey(Second_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Вторая пара (10:00-11:20)')
    third_pair = models.ForeignKey(Third_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Третья пара (11:50-13:10)')
    fourth_pair = models.ForeignKey(Fourth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Четвертая пара (13:20-14:40)')
    fifth_pair = models.ForeignKey(Fifth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Пятая пара (14:50-16:10)')
    sixth_pair = models.ForeignKey(Sixth_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Шестая пара (16:20-17:40)')
    seventh_pair = models.ForeignKey(Seventh_pair, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = 'Седьмая пара (17:50-19:10)')
    
    class Meta:
        db_table = 'List_of_sundays_schedule'
        verbose_name = 'Расписание на воскресенье'
        verbose_name_plural = 'Расписание на воскресенье'
    
    def __str__(self):
        pairs = []
        if self.first_pair:
            pairs.append(str(self.first_pair))
        if self.second_pair:
            pairs.append(str(self.second_pair))
        if self.third_pair:
            pairs.append(str(self.third_pair))
        if self.fourth_pair:
            pairs.append(str(self.fourth_pair))
        if self.fifth_pair:
            pairs.append(str(self.fifth_pair))
        if self.sixth_pair:
            pairs.append(str(self.sixth_pair))
        if self.seventh_pair:
            pairs.append(str(self.seventh_pair))
        
        if pairs:
            return f'Воскресенье: {", ".join(pairs)}'
        return 'Воскресенье: нет пар.'

class Schedule(models.Model):
    monday = models.ForeignKey(Mondays_schedule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Понедельник')
    tuesday = models.ForeignKey(Tuesdays_schedule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Вторник')
    wednesday = models.ForeignKey(Wednesdays_schedule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Среда')
    thursday = models.ForeignKey(Thursdays_schedule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Четверг')
    friday = models.ForeignKey(Fridays_schedule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пятница')
    saturday = models.ForeignKey(Saturdays_schedule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Суббота')
    sunday = models.ForeignKey(Sundays_schedule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Воскресенье')
    course = models.ForeignKey(Courses_of_Students, on_delete=models.CASCADE, verbose_name='Курс/группа')
    week_start_date = models.DateField(verbose_name='Дата начала недели')
    week_end_date = models.DateField(verbose_name='Дата окончания недели')
    is_active = models.BooleanField(default=True, verbose_name='Актуально')
    is_current_week = models.BooleanField(default=False, verbose_name='Текущая неделя')
    note = models.TextField(max_length=500, blank=True, null=True, verbose_name='Примечание к расписанию')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    created_by = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_schedules', verbose_name='Кто создал')
    
    class Meta:
        db_table = 'List_of_schedule'
        verbose_name = 'Расписание на неделю'
        verbose_name_plural = 'Расписания на неделю'
        ordering = ['-week_start_date', 'course']
        unique_together = ['course', 'week_start_date']
    
    def __str__(self):
        return f'Расписание для {self.course} на неделю {self.week_start_date} - {self.week_end_date}'
        
    def save(self, *args, **kwargs):
        if not self.week_end_date and self.week_start_date:
            from datetime import timedelta
            self.week_end_date = self.week_start_date + timedelta(days=6)
        super().save(*args, **kwargs)
    
    def get_pairs_count(self):
        count = 0
        days = [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday]
        for day in days:
            if day:
                for pair in [day.first_pair, day.second_pair, day.third_pair, day.fourth_pair, day.fifth_pair, day.sixth_pair, day.seventh_pair]:
                    if pair:
                        count += 1
        return count
    
    def is_full_week(self):
        days = [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday]
        for day in days:
            if not day:
                return False
        return True

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
    data_created = models.DateField(auto_now_add = True, verbose_name = 'Дата')
    data_updated = models.DateField(auto_now = True, verbose_name = 'Дата изменяемая')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = 'List_of_stative_student'
        verbose_name = 'Состояние студента'
        verbose_name_plural = 'Состояние студентов'

    def __str__(self):
        return self.type

class Add_HW_Professor_to_course(models.Model):
    course = models.ForeignKey(Courses_of_Students, on_delete = models.CASCADE, verbose_name = 'Домашнее задание для курса')
    file = models.FileField(unique = True, upload_to = 'static/image/homeworks_for_students/', null = False, blank = False, verbose_name = 'Файл домашнего задания студентам')
    comment = models.TextField(max_length = 500, verbose_name = 'Комментарий студентам к домашнему заданию')
    date_start = models.DateField(auto_now_add = True, help_text = 'Дата создания домашнего задания.', verbose_name = 'Дата создания д/з')
    date_final = models.DateField(help_text = 'Выберите дату конечной сдачи домашнего задания студентам.', verbose_name = 'Конечная дата выполнения')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Задал-(а) домашнее задание')

    class Meta:
        db_table = 'List_of_add_hw_professor_to_course'
        verbose_name = 'Домашнее задание для курса'
        verbose_name_plural = 'Домашнее задание для курса'

    def __str__(self):
        return f'Домашнее задание от {self.professor} студентам курса {self.course}'

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

class All_payment_of_education(models.Model):
    year = 'year'
    month = 'month'

    CHOICE_YEAR_OR_MONTH = [
        (year, 'Год'),
        (month, 'Месяц')
    ]

    type_payment = models.CharField(choices = CHOICE_YEAR_OR_MONTH, max_length = 5, default = month, verbose_name = 'Выберите тип оплаты обучения')
    amount = models.PositiveIntegerField(blank = False, null = False, default = None, verbose_name = 'Стоимость')
    courses_of_Students = models.ForeignKey(Courses_of_Students, on_delete = models.CASCADE, verbose_name = 'Курс')
    period_of_study = models.IntegerField(blank = False, null = False, default = 40, verbose_name = 'Период обучения(напишите в месяцах)')
    date = models.DateField(blank = False, null = False, verbose_name = 'Начало обучения')

    class Meta:
        db_table = 'List_of_payment_of_education'
        verbose_name = 'Общие настройки оплаты обучения'
        verbose_name_plural = 'Общие настройки оплаты обучения'

    def __str__(self):
        return f'Курс: {self.courses_of_Students}, Тип обучения: {self.type_payment}'
    
class Status_of_payment_of_education(models.Model):
    paid_for = 'paid_for'
    not_paid_for = 'not_paid_for'
    
    CHOICE_STATE_OF_PAYMENT = [
        (paid_for, 'Оплачено'),
        (not_paid_for, 'Не оплачено')
    ]

    type = models.CharField(choices = CHOICE_STATE_OF_PAYMENT, max_length = 12, default = not_paid_for, verbose_name = 'Статус оплаты')
    
class Students_payment_account(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    all_payment_of_education = models.ForeignKey(All_payment_of_education, on_delete = models.CASCADE, verbose_name = 'Обучается в')

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
    price_product_topcoins = models.PositiveSmallIntegerField(blank = False, null = False, verbose_name = 'Цена в топкоинах')
    price_product_topgems = models.PositiveSmallIntegerField(blank = False, null = False, verbose_name = 'Цена в топгемах')

    class Meta:
        db_table = 'List_of_shop'
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазин'

    def __str__(self):
        return f'Товар {self.name_product}'

class Topmoney_student(models.Model):
    topmoney = models.PositiveSmallIntegerField(blank = False, null = False, verbose_name = 'Топмани')
    student = models.ForeignKey(Student, on_delete = models.CASCADE, verbose_name = 'Студент')
    balance_student = models.ForeignKey(balance_topcoins_and_topgems, on_delete = models.CASCADE, verbose_name = 'Баланс')

    class Meta:
        db_table = 'List_of_topmoney_student'
        verbose_name = 'Топмани студента'
        verbose_name_plural = 'Топмани студента'

    def save(self, *args, **kwargs):
        if self.balance_student:
            self.topmoney = self.balance_student.topcoins + self.balance_student.topgems
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Топмани студента {self.student}'

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