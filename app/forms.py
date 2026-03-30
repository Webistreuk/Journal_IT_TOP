from .models import Autoriz
from django import forms

class AutorizForm(forms.ModelForm):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Autoriz
        fields = ['user', 'password']

class AutorizForm_remove_password(forms.ModelForm):
    email = forms.EmailInput()

    class Meta:
        model = Autoriz
        fields = ['email']