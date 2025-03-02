"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # 讓應用程式的路由生效
]

# 讓 Django 在開發模式下提供靜態檔案
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# myproject/urls.py

# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     # 管理後台路徑
#     path('admin/', admin.site.urls),
    
    
# ]

# from django.http import HttpResponse
# from django.urls import path

# # 定義一個簡單的首頁視圖
# def home(request):
#     return HttpResponse("<h1>Hello, Django!</h1>")

# urlpatterns = [
#     path('', home),  # 設定首頁 URL
# ]



# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
