from django.db import models

# Имя, пароль и почта от аккаунта.
class Autoriz(models.Model):
    user = models.CharField(unique = True, max_length = 30, blank = False, null = True, error_messages = {'max_length': 'Длина имени не может содержать более 30 символов', 'blank': 'Напишите имя.', 'null': 'Напишите имя.'})
    password = models.CharField(max_length = 120, blank = False, null = False, error_messages = {'max_length': 'Длина пароля не может содержать более 40 символов', 'blank': 'Напишите пароль.', 'null': 'Напишите пароль.'})
    email = models.EmailField(unique = True, max_length=100, blank = False, null = False, error_messages = {'max_length': 'Длина почты не может содержать более 100 символов', 'blank': 'Напишите почту.', 'null': 'Напишите почту.'})

    class Meta:
        db_table = 'List_of_users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user

class Subjects(models.Model):
    name_subject = models.CharField(unique = True, max_length = 100, blank = False, null = False)

    class Meta:
        db_table = 'List_of_subjects'
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name_subject

class Professor(models.Model):
    name = models.CharField(max_length = 30, blank = False, null = False)
    surname = models.CharField(max_length = 30, blank = False, null = False)
    patronymic = models.CharField(max_length = 40, blank = False, null = False)
    leads_the_subject = models.ForeignKey(Subjects, on_delete = models.CASCADE)
    autoriz = models.ForeignKey(Autoriz, on_delete = models.CASCADE)

    class Meta:
        db_table = 'List_of_professors'
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return self.name

class Courses_of_Students(models.Model):
    course = models.CharField(max_length = 40, blank = False, null = False, help_text = '( Курс, группа и название направления пишите в формате: 1/4РПО )')
    
    class Meta:
        db_table = 'List_of_courses_of_students'
        verbose_name = 'Курс студента'
        verbose_name_plural = 'Курс студентов'

    def __str__(self):
        return self.course

# ФИО и группа студента.
class Student(models.Model):
    name = models.CharField(max_length = 30, blank = False, null = False)
    surname = models.CharField(max_length = 30, blank = False, null = False)
    patronymic = models.CharField(max_length = 40, blank = False, null = False)
    autoriz = models.ForeignKey(Autoriz, on_delete = models.CASCADE)
    courses_of_students = models.ForeignKey(Courses_of_Students, on_delete=models.CASCADE, null = True, blank = True)

    class Meta:
        db_table = 'List_of_students'
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
         return f"{self.surname} {self.name[0]}. {self.patronymic[0]}."

class Marks(models.Model):
    marks = models.IntegerField(blank=False, null=True)

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
    
    type = models.CharField(max_length=4, choices=CHOICE_TYPE_WORK, default=HW)

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

    type = models.CharField(max_length = 8, choices = CHOICE_TYPE_PRESENCE, default = presence)
    data_created = models.DateField(auto_now_add = True) # Дата которая создается автоматически.
    data_updated = models.DateField(auto_now = True) # Если преподаватель ошибочно отметил присутствие/отсутсвие студенту, здесь выставляется дата вручную.
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = 'List_of_stative_student'
        verbose_name = 'Состояние студента'
        verbose_name_plural = 'Состояние студентов'

    def __str__(self):
        return self.type

class Add_HW_Professor(models.Model):
    file = models.FileField(upload_to = 'static/image/homeworks_for_students/', null = False, blank = False)
    comment = models.TextField(max_length = 500)
    date = models.DateField(help_text = 'Выберите дату конечной сдачи домашнего задания студентам.')

class Information_about_HW_for_students(models.Model):
    Issued = models.DateField(auto_now_add = True)
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE)
    add_hw_professor = models.ForeignKey(Add_HW_Professor, on_delete = models.CASCADE)