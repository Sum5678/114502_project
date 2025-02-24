
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # 確保 index.html 在 templates/ 內
