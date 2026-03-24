from django.db import models

class Autoriz(models.Model):
    name = models.CharField(max_length = 30, blank = False, null = False, error_messages = {'max_length': 'Длина имени не может содержать более 30 символов', 'blank': 'Напишите имя.', 'null': 'Напишите имя.'})
    password = models.CharField(max_length = 40, blank = False, null = False, error_messages = {'max_length': 'Длина пароля не может содержать более 40 символов', 'blank': 'Напишите пароль.', 'null': 'Напишите пароль.'})