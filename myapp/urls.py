from django.urls import path, include
from . import views
from django.contrib import admin
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import PemapAllListView, PemapAllUpdateView
from django.views.generic import TemplateView
from .views import edit_report 

urlpatterns = [
    # #思璇
    # path('chatrooms/', views.chatroom_map, name='chatroom_map'),
    path('', include('pwa.urls')),  # PWA support
    path('admin/', admin.site.urls),

    # manifest.json 用 views.py 回傳
    path('manifest.json', views.manifest, name='manifest'),

    # service-worker.js 用 TemplateView 讀模板
    path(
        'service-worker.js',
        TemplateView.as_view(
            template_name='service-worker.js',
            content_type='application/javascript'
        ),
        name='service-worker'
    ),
    path('api/submit_report/', views.submit_report, name='submit_report'),
    path('api/submit_store/', views.submit_store, name='submit_store'),
    path('business/upload/', views.business_upload, name='business_upload'),
    path('business/list/', views.business_list_view, name='business_list'),
    path('about/', views.about, name='about'),
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
    
    path('admin/', admin.site.urls),

    #用戶管理的部分
    path('users/', views.user_admin_list, name='user_admin_list'),
    path('search/', views.user_admin_search, name='user_admin_search'),
    path('edit/<int:user_id>/', views.user_admin_edit, name='user_admin_edit'),
    path('delete/<int:user_id>/', views.user_admin_delete, name='user_admin_delete'),

    #台灣縣市和行政區/最近警局/教育網頁的部分
    path('harassment_prevention/', views.harassment_prevention, name='harassment_prevention'),
    path('education/', views.education_page, name='education_page'),
    path('nearest-police/', views.nearest_police_view, name='nearest_police'),
    path('taiwan-regions-admin/', views.taiwan_regions_admin, name='taiwan_regions_admin'),
    path('taiwan-regions/add/', views.taiwan_regions_add, name='taiwan_regions_add'),
    path('taiwan-regions/edit/<int:id>/', views.taiwan_regions_edit, name='taiwan_regions_edit'),
    path('taiwan-regions/delete/<int:id>/', views.taiwan_regions_delete, name='taiwan_regions_delete'),
    path('police-address/', views.police_address_list, name='police_address_list'),
    path('police_address/add/', views.police_address_add, name='police_address_add'),
    path('police-address/edit/<str:pk>/', views.police_address_edit, name='police_address_edit'),
    path('police-address/delete/<str:pk>/', views.police_address_delete, name='police_address_delete'),
    path('education-crud/', views.education_list, name='education_list'),
    path('education-crud/new/', views.education_create, name='education_create'),
    path('education-crud/edit/<int:pk>/', views.education_update, name='education_update'),
    path('education/delete/<int:pk>/confirm/', views.education_delete_confirm, name='education_delete_confirm'),
    path('education/delete/<int:pk>/', views.education_delete, name='education_delete'),
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
    path('post/', views.post, name='post'),
    path('post_display/', views.post_display, name='post_display'),
   # 文章
    path('edit_post/<str:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<str:post_id>/', views.delete_post, name='delete_post'),
    path('like_post/<str:post_id>/', views.like_post, name='like_post'),
    path('save_post/<str:post_id>/', views.save_post, name='save_post'),
    # 留言
    path('post/<str:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<str:post_id>/comment/delete/', views.delete_comment, name='delete_comment'),
    path('post/<str:post_id>/comments/', views.post_comments, name='post_comments'),
    path('post/<str:post_id>/comment/reply/', views.reply_comment, name='reply_comment'),
    path('post/<str:post_id>/comment/like/', views.like_comment, name='like_comment'),
    path('post/<str:post_id>/reply/delete/', views.delete_reply, name='delete_reply'),

    # ✅ 留言編輯（你已經有）
    path('edit_comment/<str:post_id>/<str:key>/', views.edit_comment, name='edit_comment'),

    # ✅ 新增/確認：回覆編輯
    path('post/<str:post_id>/reply/edit/', views.edit_reply, name='edit_reply'),
        # 交流區檢舉（前台送出）
    path('report/create/', views.create_report, name='create_report'),
    path("reports/", views.review_reports, name="review_reports"),   # ← 交流區檢舉審核
    path("reports/act/", views.act_on_report, name="act_on_report"), # ← 管理員動作
    path('report/create/', views.create_report, name='create_report'),
    path('reports/decide/', views.report_decide, name='report_decide'),
    # 交流區檢舉：編輯紀錄（只改 status / reason / admin_note）
    path("reports/edit/<int:report_id>/", views.edit_report, name="edit_report"),
    # 交流區檢舉：刪除被檢舉的目標（僅限已處置後）
    path("reports/delete-target/<int:report_id>/", views.delete_report_target, name="delete_report_target"),
    path('notifications/unread_count/', views.notif_unread_count, name='notif_unread_count'),
    path('notifications/dropdown/', views.notif_dropdown, name='notif_dropdown'),
    path('notifications/mark_all/', views.notif_mark_all, name='notif_mark_all'),
    path('notifications/mark_all_unread/', views.notif_mark_all_unread, name='notif_mark_all_unread'),
    path("post/<str:post_id>/", views.post_detail, name="post_detail"),
    path("notifications/delete/<int:notif_id>/", views.notif_delete, name="notif_delete"),
    path("notifications/mark_read/<int:notif_id>/", views.notif_mark_read, name="notif_mark_read"),






    #想的
    # 一般頁面
    path('announcement/', views.announcement, name='announcement'),
    path('form/', views.form, name='form'),
    path('safety/', views.safety, name='safety'),
    path('autodial/', views.autodial, name='autodial'),
    # path('mymap/', views.mymap, name='mymap'),
    #path('settings/', views.settings, name='settings'),
    #path('write/', views.settings, name='write'),  # 同 settings，可保留或合併

    # 登入/登出相關
    # path('0101login/', views.login_page, name='login'),  # 另一登入頁
    path('01userlogin/', views.user_login_page, name='userlogin'),
    path('userlogin/', views.user_login_page),  # 可做第二路徑，不一定要name
    path('userlogout/', views.logout_view, name='userlogout'),  # 命名統一成 userlogout
    path('userlogin_out/', views.logout_view, name='01_userlogin_out'),  # 登出路由

    # 用戶資料
    path('this_user_profile/create/', views.create_user_profile, name='create_user_profile'),
    path('this_user_profile/update/', views.update_user_profile, name='update_user_profile'),
    path('this_user_profile/', views.this_user_profile_redirect, name='this_user_profile'),
    path('user_data/', views.user_data_view, name='user_data'),  #   非第一次登入看資料頁
    path("user/<int:pk>/", views.public_profile, name="public_profile"), #給別人看的
    path('public_profile/gmail/<str:gmail>/', views.public_profile, name='public_profile'),#給別人看的
    # 商家廣告：上傳處理
    path("store/upload-ad/", views.upload_store_ad, name="upload_store_ad"),
    # 商家廣告：上傳頁面
    path("store/upload-ad-page/", views.upload_ad_page, name="upload_store_ad_page"),
    # API
    path("api/get_store_ad/", views.get_store_ad, name="api_get_store_ad"),
    path("api/stores-with-ads/", views.stores_with_ads, name="stores_with_ads"),
    path('test_payment/', views.test_payment, name='test_payment'),  # 模擬付款頁面
    path('test_payment_done/', views.test_payment_done, name='test_payment_done'),  # 模擬付款頁面完成



    path('profile/', views.profile, name='profile'),

    # API & 地圖相關
    path('api/incidents/', views.incident_list, name='incident_list'),#地圖顯示測試
    path('api/fake_incidents/', views.fake_incident_lookup, name='fake_incident_lookup'), #地圖顯示測試
    path('lookup/', views.lookup_page, name='lookup_page'),#地圖顯示測試
    path('fake_incident_lookup/', views.fake_incident_lookup, name='fake_incident_lookup'),  # 重複可刪一個
    path('map0257/', views.show_map, name='show_map'),
    path('mymap/', views.map_view, name='map_view'),
    path('api/reports/', views.reports_json, name='reports_json'),#地圖顯示測試again(pemap_all的)
    path('api/submit_report/', views.submit_report, name='submit_report'),
    path('api/approved-locations/', views.approved_locations_api, name='approved_locations_api'),#事件地圖
    path('store_map/', views.store_map_view, name='store_map'),#商家地圖
    path('api/stores/', views.store_data_api, name='store_data_api'),#商家地圖
    # path('api/reports_with_subkind/', views.reports_with_subkind_json, name='reports_with_subkind_json'),
    path('api/reports_with_subkind_json/', views.reports_with_subkind_json, name='reports_with_subkind_json'),
    path('api/stores-with-ads/', views.stores_with_ads_api, name='stores_with_ads_api'),
    path('api/get_store_ad/', views.get_store_ad, name='get_store_ad'),



   #聊天室相關
    path('api/chatrooms/', views.chatrooms_api, name='chatrooms_api'),
    path('chatrooms_api/', views.chatrooms_api, name='chatrooms_api'),
    path('chat/messages/<int:room_id>/', views.chat_messages_api, name='chat_messages_api'),
    path('chat/send/<int:room_id>/', views.send_message, name='chat_send_api'),
    path('favorites/add/', views.add_to_favorites, name='add_to_favorites'),
    path('chat/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('chatrooms/', views.chatroom_view, name='chatroom_page'),
    path('api/reports.json', views.reports_with_subkind_json, name='reports_with_subkind_json'),
    path('chat/check_message/', views.check_message, name='check_message'),


    # Pemap 管理員相關
    path('pemap/approve/<int:p_id>/<int:stage>/', views.pemap_approve, name='pemap_approve'),#處理管理員對pemap資料狀態
    # path('admin/pemap/approve/<int:p_id>/<int:stage>/', views.pemap_approve, name='pemap_approve'),#處理管理員對pemap資料狀態
    path('pemap/', PemapAllListView.as_view(), name='pemap_list'),  ##處理管理員對pemap資料狀態
    path('pemap/<int:p_id>/edit/', PemapAllUpdateView.as_view(), name='pemap_detail'),#處理管理員對pemap資料狀態
    path('pemap_judge/', views.pemap_judge, name='pemap_judge'),#審核事件
    path('pemap_judge_step1/<int:p_id>/', views.pemap_judge_step1, name='pemap_judge_step1'),


    # AI 判斷
    path('99judge/', views.show_judge_page, name='show_judge_page'),
    path('ai_judge/', views.ai_judge, name='ai_judge'), #ai檢測

    # 管理員專用頁面
    path('admin_login/', views.admin_login, name='admin_login'),#管理員登入
    path('admin_interview/', views.admin_interview, name='admin_interview'),#管理員自介
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_index/', views.admin_index, name='admin_index'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('admin_reviews/', views.admin_decide_view, name='admin_decide'),#顯示出該管理員審核過的資料
    path('store/judge/', views.store_judge, name='store_judge'),
    path('store/judge/<str:st_id>/', views.store_judge_step1, name='store_judge_step1'),
    path('store_decide/', views.store_decide, name='store_decide'),#顯示出該管理員審核過的資料
    path('store/judge/<str:st_id>/', views.store_judge_view, name='store_judge_view'),
    path('store/reject/<str:st_id>/', views.store_step2_view, name='store_step2'),   #商家幾天
    # path('send-email/', views.admin_send_email, name='admin_send_email'), #事件拒絕後跳轉頁面
    path("adminad/review-ads/", views.admin_review_ads, name="admin_review_ads"),
    # 將 st_id 改為 history_id
    path("adminad/review-ads/<int:history_id>/<str:action>/", views.review_store_ad, name="review_store_ad"),  #廣告審核



    # urls.py
    path('send-email/<int:p_id>/', views.admin_send_email, name='admin_send_email'), 

    

    # 登入後判斷跳轉
    path('login/redirect/', views.login_redirect, name='login_redirect'),

    # 動態聊天室房間（需放最底下，避免路由衝突）
    path('<str:room_name>/', views.room, name='room'),


    # 其他路由



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# 原本沒有這些路徑


# 整理#想的
#     path('announcement/', views.announcement, name='announcement'),
#     path('chatroom/', views.chatroom, name='chatroom'),
#     path('form/', views.form, name='form'),
#     path('safety/', views.safety, name='safety'),
#     path('autodial/', views.autodial, name='autodial'),
#     path('mymap/', views.mymap, name='mymap'),
#     path('0101login/', views.login_page, name='login'),  
#     path('settings/', views.settings, name='settings'),
#     path('write/', views.settings, name='write'),
#     path('01userlogin/', views.user_login_page, name='userlogin'),
#     path('profile/', views.profile, name='profile'),
#     path('userlogin/', views.user_login_page, name='user_login_page'),
#     path('01userlogin/', views.user_login_page),  # 第二條可選路徑，不需 name
#     path('userlogin_out/', views.logout_view, name='01_userlogin_out'),  # 登出路由

#     path('this_user_profile/', views.create_user_profile, name='create_user_profile'),
#     path('this_user_profile', views.create_user_profile, name='create_user_profile'),
#     path("this_user_profile", views.ThisUserProfile, name="this_user_profile"),
#     path('this_user_profile', views.update_user_profile, name='update_user_profile'),

#     path('api/incidents/', views.incident_list, name='incident_list'),#地圖顯示測試
#     path('api/fake_incidents/', views.fake_incident_lookup, name='fake_incident_lookup'), #地圖顯示測試
#     path('lookup/', views.lookup_page, name='lookup_page'),#地圖顯示測試
#     path('fake_incident_lookup/', views.fake_incident_lookup, name='fake_incident_lookup'),#地圖顯示測試
#     path('map0257/', views.show_map, name='show_map'),#地圖顯示測試
#     path('999map/', views.map_view, name='map_view'),#地圖顯示測試again(pemap_all的)
#     path('api/reports/', views.reports_json, name='reports_json'),#地圖顯示測試again(pemap_all的)
    
#     path('admin/pemap/approve/<int:p_id>/<int:stage>/', views.pemap_approve, name='pemap_approve'),  ##處理管理員對pemap資料狀態
#     path('pemap/', PemapAllListView.as_view(), name='pemap_list'),##處理管理員對pemap資料狀態
#     path('pemap/<int:p_id>/edit/', PemapAllUpdateView.as_view(), name='pemap_detail'),##處理管理員對pemap資料狀態

    
#     path('99judge/', views.show_judge_page, name='show_judge_page'),#ai檢測
#     path('ai_judge/', views.ai_judge, name='ai_judge'),#ai檢測
#     path('admin_login/', views.admin_login, name='admin_login'),
#     path('admin_interview/', views.admin_interview, name='admin_interview'),#管理員自介
#     path('admin_logout/', views.admin_logout, name='admin_logout'),#管理員登入
#     path('pemap_judge/', views.pemap_judge, name='pemap_judge'),#審核事件
#     path('pemap_judge_step1/<int:p_id>/', views.pemap_judge_step1, name='pemap_judge_step1'),
#     path('admin_index/', views.admin_index, name='admin_index'),
#     path('admin_register/', views.admin_register, name='admin_register'),
    
#     path('login/redirect/', views.login_redirect, name='login_redirect'),#使用者登入後有甜過基本資料就不用再填
#     path('user_data/', views.user_data_view, name='user_data'),  # 非第一次登入看資料頁


   

#     path('<str:room_name>/', views.room, name='room'),

#     # 其他路由
#     #思璇
#      #思璇
#     path('api/submit_report/', views.submit_report, name='submit_report'),