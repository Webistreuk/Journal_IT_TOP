from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Autoriz
from .forms import AutorizForm

def autoriz(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpassword')
        user = Autoriz.objects.filter(name=username).first()
        if user:
            if user.password == password:
                return redirect('Главная')
            else:
                return HttpResponse()
        
        return render(request, 'main.html')
    else:
        form = AutorizForm()
        return render(request, 'Authorize.html', {'form': form})
    
def main(request):
    return redirect('Главная')