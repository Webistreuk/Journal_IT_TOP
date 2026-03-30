from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Autoriz
from .forms import AutorizForm

def autoriz(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpassword')
        user = Autoriz.objects.filter(user=username).first()
        if user and user.password == password:
            return redirect('Главная')
        else:
            return render(request, 'Authorize.html', {'error': 'Неправильно был введен логин или пароль!'})
    else:
        form = AutorizForm()
        return render(request, 'Authorize.html', {'form': form})
    
def main(request):
    return redirect('Главная')