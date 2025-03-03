from django.urls import path
from . import views

urlpatterns = [
    path('index.html', views.index, name='index'),
    # path('index.html', views.index, name='index')
    # 對,我也不知道有時換這個反而能跑,有時又不能跑    
    path('tables.html', views.tables, name='tables'),
    path('register.html', views.register, name='register'),
    path('password.html', views.password, name='password'),
    path('login.html', views.login, name='login'),
    path('layout-static.html', views.layout_static, name='layout-static'),
    path('layout-sidenav-light.html', views.layout_sidenav_light, name='layout-sidenav-light'),
    path('charts.html', views.charts, name='charts'),
    path('500.html', views.error_500, name='500'),
    path('401.html', views.error_401, name='401'),
    path('404.html', views.error_404, name='404'),
]

# 原本沒有這些路徑