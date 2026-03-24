from django.shortcuts import render
from .models import Autoriz

def Autoriz(reques):
    autoriz = Autoriz.objects.all()
    return render(request, 'index.html', {"autoriz": autoriz})