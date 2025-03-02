from django.shortcuts import render
# myapp/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, World!")

def index(request):
    return render(request, 'index.html')

def tables(request):
    return render(request, 'tables.html')

def register(request):
    return render(request, 'register.html')

def password(request):
    return render(request, 'password.html')

def login(request):
    return render(request, 'login.html')

def layout_static(request):
    return render(request, 'layout-static.html')

def layout_sidenav_light(request):
    return render(request, 'layout-sidenav-light.html')

def charts(request):
    return render(request, 'charts.html')

def error_500(request):
    return render(request, '500.html')

def error_401(request):
    return render(request, '401.html')

def error_404(request):
    return render(request, '404.html')
