from django.urls import path, include
from . import views
from django.contrib import admin
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import PemapAllListView, PemapAllUpdateView

urlpatterns = [
    path('report/', views.report_view, name='report'),#填寫表單
    path('report/list/', views.report_list_view, name='report_list'),
    path('', views.index, name='home'),
    path('index.html', views.index, name='index'),#主畫面
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
    path('harassment_prevention/', views.harassment_prevention, name='harassment_prevention'),
    path('education/', views.education_page, name='education_page'),
    path('nearest-police/', views.nearest_police_view, name='nearest_police'),
    
    path('admin/', admin.site.urls),
    path('admin/region/', views.taiwan_regions_admin, name='taiwan_regions_admin'),
    path('taiwan-regions-admin/', views.taiwan_regions_admin, name='taiwan_regions_admin'),
    path('police-address/', views.police_address_list, name='police_address_list'),
    path('police-address/add/', views.police_address_add, name='police_address_add'),
    path('police-address/edit/<str:pk>/', views.police_address_edit, name='police_address_edit'),
    path('police-address/delete/<str:pk>/', views.police_address_delete, name='police_address_delete'),
    path('education-crud/', views.education_list, name='education_list'),
    path('education-crud/new/', views.education_create, name='education_create'),
    path('education-crud/edit/<int:pk>/', views.education_update, name='education_update'),
    path('education-crud/delete/<int:pk>/', views.education_delete, name='education_delete'),
    path('education-crud/image/<int:pk>/', views.education_image, name='education_image'), 
    path('anonymous-chat/', views.anonymous_chat, name='anonymous-chat'),  # anonymous-chat 頁面
    path('index35/', views.index35, name='index35'),  # 新增 index35.html 路由
    path('map/', views.map_view, name='map'),  # 添加 map.html 路由
    path('001_login/', views.login_page, name='login_page'),  # 讓 /001_login 也能對應
    path('area/', views.area_view, name='area'),
    path('police/', views.region_selector, name='region_selector'),
    path('mail/', views.mail, name='mail'),
    path('autodial/', views.autodial_view, name='autodial'),
    path('mychatroom/', views.mychatroom, name='mychatroom'),
    path('community/', views.community, name='community'),
    path('face_detection/', views.face_detection_view, name='face_detection'), #人臉辨識
    
    



    #想的
    path('announcement/', views.announcement, name='announcement'),
    path('chatroom/', views.chatroom, name='chatroom'),
    path('form/', views.form, name='form'),
    path('safety/', views.safety, name='safety'),
    path('autodial/', views.autodial, name='autodial'),
    path('mymap/', views.mymap, name='mymap'),
    path('0101login/', views.login_page, name='login'),  
    path('settings/', views.settings, name='settings'),
    path('write/', views.settings, name='write'),
    path('01userlogin/', views.user_login_page, name='userlogin'),
    path('profile/', views.profile, name='profile'),
    path('userlogin_out/', views.logout_view, name='01_userlogin_out'),  # 登出路由
    path('this_user_profile', views.create_user_profile, name='create_user_profile'),
    path("this_user_profile", views.ThisUserProfile, name="this_user_profile"),
    path('this_user_profile', views.update_user_profile, name='update_user_profile'),
    path('api/incidents/', views.incident_list, name='incident_list'),#地圖顯示測試
    path('api/fake_incidents/', views.fake_incident_lookup, name='fake_incident_lookup'), #地圖顯示測試
    path('lookup/', views.lookup_page, name='lookup_page'),#地圖顯示測試
    path('fake_incident_lookup/', views.fake_incident_lookup, name='fake_incident_lookup'),#地圖顯示測試
    path('map0257/', views.show_map, name='show_map'),#地圖顯示測試
    path('999map/', views.map_view, name='map_view'),#地圖顯示測試again(pemap_all的)
    path('api/reports/', views.reports_json, name='reports_json'),#地圖顯示測試again(pemap_all的)
    
    path('admin/pemap/approve/<int:p_id>/<int:stage>/', views.pemap_approve, name='pemap_approve'),  ##處理管理員對pemap資料狀態
    path('pemap/', PemapAllListView.as_view(), name='pemap_list'),##處理管理員對pemap資料狀態
    path('pemap/<int:p_id>/edit/', PemapAllUpdateView.as_view(), name='pemap_detail'),##處理管理員對pemap資料狀態

    
    path('99judge/', views.show_judge_page, name='show_judge_page'),#ai檢測
    path('ai_judge/', views.ai_judge, name='ai_judge'),#ai檢測
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_interview/', views.admin_interview, name='admin_interview'),#管理員自介
    path('admin_logout/', views.admin_logout, name='admin_logout'),#管理員登入
    path('pemap_judge/', views.pemap_judge, name='pemap_judge'),#審核事件
    path('pemap_judge_step1/<int:p_id>/', views.pemap_judge_step1, name='pemap_judge_step1'),
    path('admin_index/', views.admin_index, name='admin_index'),
    path('admin_register/', views.admin_register, name='admin_register'),
    
    path('login/redirect/', views.login_redirect, name='login_redirect'),#使用者登入後有甜過基本資料就不用再填



   

    path('<str:room_name>/', views.room, name='room'),

    # 其他路由
    #思璇
     #思璇
    path('api/submit_report/', views.submit_report, name='submit_report'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 原本沒有這些路徑
