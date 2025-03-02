from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('tables/', views.tables, name='tables'),
    path('register/', views.register, name='register'),
    path('password/', views.password, name='password'),
    path('login/', views.login, name='login'),
    path('layout-static/', views.layout_static, name='layout-static'),
    path('layout-sidenav-light/', views.layout_sidenav_light, name='layout-sidenav-light'),
    path('charts/', views.charts, name='charts'),
    path('500/', views.error_500, name='500'),
    path('401/', views.error_401, name='401'),
    path('404/', views.error_404, name='404'),
]
