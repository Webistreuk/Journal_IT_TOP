from .models import Autoriz

class Autoriz(forms.ModelForm):
    name = forms.CharField(required = True, blank = False, null = False, error_messages = {'blank': 'Введите имя.', 'required': 'Введите имя.'})
    password = forms.CharField(required = True, blank = False, null = False, error_messages = {'required': 'Введите пароль.'}, widget = forms.PassworInput())

    class Meta:
        model = Autoriz
        fields = ['name', 'password']