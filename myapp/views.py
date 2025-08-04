from django.shortcuts import render
from .models import TaiwanRegion, PoliceAddress #資料表的
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .forms import AutoDialForm
from django.views.decorators.csrf import csrf_exempt
from .models import PemapAll
from .models import StoreAll
from django.utils import timezone
import json
from datetime import datetime


def report_view(request):
    return render(request, 'report.html')

def index(request):
    return render(request, 'index.html')  # 確保 index.html 在 templates/ 內

# 另一個首頁版本（index35.html）
def index35(request):
    return render(request, 'index35.html')

# 表格頁面
def tables(request):
    return render(request, 'tables.html')

# 註冊頁面
def register(request):
    return render(request, 'register.html')

# 密碼頁面
def password(request):
    return render(request, 'password.html')

# 登入頁面
def login(request):
    return render(request, 'login.html')



# 布局 - 靜態頁面
def layout_static(request):
    return render(request, 'layout-static.html')

# 布局 - 輕量側邊欄頁面
def layout_sidenav_light(request):
    return render(request, 'layout-sidenav-light.html')

# 圖表頁面
def charts(request):
    return render(request, 'charts.html')

# 500 錯誤頁面
def error_500(request):
    return render(request, '500.html')

# 500 錯誤頁面
def error_401(request):
    return render(request, '401.html')

# 500 錯誤頁面
def error_404(request):
    return render(request, '404.html')


def harassment_prevention(request):
    return render(request, 'harassment_prevention.html')

def education_page(request):
    return render(request, 'education_page.html')

#教育網頁
from .models import EducationPage

def education_page(request):
    pages = EducationPage.objects.all()
    return render(request, 'education_page.html', {'pages': pages})

#教育網頁新增改刪
from django.shortcuts import render, redirect, get_object_or_404
from .models import EducationPage
from .education_forms import EducationPageUploadForm

def education_list(request):
    pages = EducationPage.objects.all()
    return render(request, 'education_list.html', {'pages': pages})

def education_create(request):
    if request.method == 'POST':
        form = EducationPageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('education_list')
    else:
        form = EducationPageUploadForm()
    return render(request, 'education_form.html', {'form': form})

def education_update(request, pk):
    page = get_object_or_404(EducationPage, pk=pk)
    if request.method == 'POST':
        form = EducationPageUploadForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('education_list')
    else:
        form = EducationPageUploadForm(instance=page)
    return render(request, 'education_form.html', {'form': form})

def education_delete(request, pk):
    page = get_object_or_404(EducationPage, pk=pk)
    if request.method == 'POST':
        page.delete()
        return redirect('education_list')
    return render(request, 'education_confirm_delete.html', {'page': page})

from django.http import HttpResponse

def education_image(request, pk):
    page = get_object_or_404(EducationPage, pk=pk)
    if page.image_url:
        return HttpResponse(page.image_url, content_type="image/png")
    return HttpResponse(status=404)


#最近警局
from django.shortcuts import render
from .models import TaiwanRegion, PoliceAddress
from django.forms.models import model_to_dict


def nearest_police_view(request):
    country_city = request.GET.get('country_city')
    district_town = request.GET.get('district_town')

    countries = TaiwanRegion.objects.values_list('country_city', flat=True).distinct()
    districts = []
    police_data = []

    if country_city:
        districts = TaiwanRegion.objects.filter(country_city=country_city).values_list('district_town', flat=True).distinct()

    if country_city and district_town:
        zipcodes = TaiwanRegion.objects.filter(
            country_city=country_city,
            district_town=district_town
        ).values_list('zipcode', flat=True)

        queryset = PoliceAddress.objects.filter(zipcode__in=zipcodes)
        police_data = [
            model_to_dict(obj, fields=["precinct_name", "address", "phone", "POINT_X", "POINT_Y"])
            for obj in queryset
        ]

    # 不論有沒有選縣市，都要傳全台所有警局，GPS 按鈕會用到
    all_police_data = [
        model_to_dict(obj, fields=["precinct_name", "address", "phone", "POINT_X", "POINT_Y"])
        for obj in PoliceAddress.objects.all()
    ]

    return render(request, 'nearest_police.html', {
        'countries': countries,
        'districts': districts,
        'selected_country': country_city,
        'selected_district': district_town,
        'police_data': police_data,
        'all_police_data': all_police_data,
        'google_maps_api_key': 'AIzaSyAUuPZMMJvgVWftmqVyzfX8mKTwMX4kA6o',  # 換成你的 Key
    })


#縣市後端
# regions/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import TaiwanRegion
from .taiwan_regions_forms import TaiwanRegionForm

def taiwan_regions_admin(request):
    regions = TaiwanRegion.objects.all()
    return render(request, 'taiwan_regions_admin.html', {'regions': regions})

def taiwan_regions_add(request):
    if request.method == 'POST':
        form = TaiwanRegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('taiwan_regions_admin')
    else:
        form = TaiwanRegionForm()
    return render(request, 'taiwan_regions_add.html', {'form': form, 'action': '新增'})

def taiwan_regions_edit(request, id):
    region = get_object_or_404(TaiwanRegion, pk=id)
    if request.method == 'POST':
        form = TaiwanRegionForm(request.POST, instance=region)
        if form.is_valid():
            form.save()
            return redirect('taiwan_regions_admin')
    else:
        form = TaiwanRegionForm(instance=region)
    return render(request, 'taiwan_regions_edit.html', {'form': form, 'action': '編輯'})

def taiwan_regions_delete(request, id):
    region = get_object_or_404(TaiwanRegion, pk=id)
    if request.method in ['POST', 'GET']:
        region.delete()
        return redirect('taiwan_regions_admin')



#警局地址後端
from django.shortcuts import render, get_object_or_404, redirect
from .models import PoliceAddress
from .police_forms import PoliceAddressForm

def police_address_list(request):
    addresses = PoliceAddress.objects.all().order_by('precinct_name')
    return render(request, 'police_address_admin.html', {'addresses': addresses})

from django.shortcuts import render, redirect
from .models import PoliceAddress
from django.urls import reverse
from django.contrib import messages

def police_address_add(request):
    if request.method == 'POST':
        precinct_name = request.POST.get('precinct_name')
        zipcode = request.POST.get('zipcode')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        point_x = request.POST.get('POINT_X')
        point_y = request.POST.get('POINT_Y')

        # 資料驗證可視需求加強
        if precinct_name and zipcode and address and phone and point_x and point_y:
            PoliceAddress.objects.create(
                precinct_name=precinct_name,
                zipcode=zipcode,
                address=address,
                phone=phone,
                POINT_X=point_x,
                POINT_Y=point_y
            )
            messages.success(request, "成功新增警局資料！")
            return redirect('police_address_list')  # 替換為你列表頁的網址名稱
        else:
            messages.error(request, "所有欄位皆為必填，請確認填寫完整。")

    return render(request, 'police_address_add.html')


def police_address_edit(request, pk):
    address = get_object_or_404(PoliceAddress, pk=pk)

    if request.method == 'POST':
        address.precinct_name = request.POST.get('precinct_name')
        address.zipcode = request.POST.get('zipcode')
        address.address = request.POST.get('address')
        address.phone = request.POST.get('phone')
        address.POINT_X = request.POST.get('POINT_X')
        address.POINT_Y = request.POST.get('POINT_Y')

        address.save()
        messages.success(request, "資料已成功更新！")
        return redirect('police_address_list')

    return render(request, 'police_address_edit.html', {'address': address})

def police_address_delete(request, pk):
    address = get_object_or_404(PoliceAddress, pk=pk)
    if request.method == 'POST':
        address.delete()
        return redirect('police_address_list')
    return render(request, 'police_address_confirm_delete.html', {'address': address})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def fake_incident_lookup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            address = data.get('address', '')

            # 模擬查詢結果
            fake_result = {
                'address': address,
                'nearby_incidents': [
                    {'id': 1, 'kind': '騷擾', 'description': '某人尾隨我', 'lat': 25.03, 'lng': 121.56},
                    {'id': 2, 'kind': '偷拍', 'description': '有人拿手機偷拍', 'lat': 25.04, 'lng': 121.55},
                ]
            }

            return JsonResponse(fake_result)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'POST request required'}, status=405)

# 新增的匿名聊天頁面
def anonymous_chat(request):
    person_name = request.GET.get('person', '未知人物')  # 獲取 URL 參數中的人物名稱
    return render(request, 'anonymous-chat.html', {'person_name': person_name})

def map_view(request):
    return render(request, 'map.html')

def region_selector(request):
    return render(request, 'region_page.html')

def mail(request):
    return render(request, 'mail.html')

def mychatroom(request):
    return render(request, 'mychatroom.html')

def community(request):
    return render(request, 'community.html')

#-----------------想-------------------------
def announcement(request):
    return render(request, 'announcement.html')

def chatroom(request):
    return render(request, 'chatroom.html')

def form(request):
    return render(request, 'form.html')

def safety(request):
    return render(request, 'safety.html')

def autodial(request):
    return render(request, 'autodial.html')

def mymap(request):
    return render(request, 'mymap.html')

def login_page(request):
    return render(request, '001_login.html')

def area_view(request):
    return render(request, 'area.html')
    return render(request, '0101login.html')

def settings(request):
    return render(request, 'settings.html')

def write(request):
    return render(request, 'write.html')


#自動撥號
FIXED_PHONE = '0900123456'

def autodial_view(request):
    initial_message = request.session.get('default_message', '')
    form = AutoDialForm(initial={'default_message': initial_message})
    result = None
    confirm_stage = False

    if request.method == 'POST':
        form = AutoDialForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['default_message']
            request.session['default_message'] = message
            action = request.POST.get('action')

            if action == 'call':
                result = f"模擬撥打電話給 {FIXED_PHONE}"
            elif action == 'message':
                # 第一次送出為確認階段
                if request.POST.get('confirm') != 'yes':
                    confirm_stage = True  # 顯示確認畫面
                else:
                    result = f"✅ 成功傳送訊息給 {FIXED_PHONE}，內容是：{message}"

    return render(request, 'autodial.html', {
        'form': form,
        'phone': FIXED_PHONE,
        'result': result,
        'confirm_stage': confirm_stage,
    })


#userloigin
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.hashers import make_password, check_password


def user_login_page(request):
    if request.method == 'POST':
        # ✅ 登入邏輯
        if 'login' in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            try:
                user = UserProfile.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    messages.success(request, "登入成功！")
                    return redirect('login_redirect')  # ✅ 修改這裡
                else:
                    messages.error(request, "密碼錯誤")
            except UserProfile.DoesNotExist:
                messages.error(request, "帳號不存在")

        # ✅ 註冊邏輯
        elif 'register' in request.POST:
            email = request.POST['email']
            nickname = request.POST['nickname']
            password = request.POST['password']

            if UserProfile.objects.filter(email=email).exists():
                messages.error(request, "此帳號已被註冊")
            else:
                hashed_pw = make_password(password)
                user = UserProfile.objects.create(
                    email=email,
                    nickname=nickname,
                    password=hashed_pw
                )
                request.session['user_id'] = user.id
                messages.success(request, "註冊成功，已自動登入")
                return redirect('login_redirect')

    return render(request, '01_userlogin.html')


# def user_login_page(request):
#     if request.method == 'POST':
#         # ✅ 登入邏輯
#         if 'login' in request.POST:
#             email = request.POST['email']
#             password = request.POST['password']
#             try:
#                 user = UserProfile.objects.get(email=email)
#                 if check_password(password, user.password):
#                     request.session['user_id'] = user.id
#                     messages.success(request, "登入成功！")
#                     return redirect('login')  # 這裡是你說的 0101login/ 對應 name='login'
#                 else:
#                     messages.error(request, "密碼錯誤")
#             except UserProfile.DoesNotExist:
#                 messages.error(request, "帳號不存在")

#         # ✅ 註冊邏輯：註冊後直接登入 + 跳首頁
#         elif 'register' in request.POST:
#             email = request.POST['email']
#             nickname = request.POST['nickname']
#             password = request.POST['password']

#             if UserProfile.objects.filter(email=email).exists():
#                 messages.error(request, "此帳號已被註冊")
#             else:
#                 hashed_pw = make_password(password)
#                 user = UserProfile.objects.create(
#                     email=email,
#                     nickname=nickname,
#                     password=hashed_pw
#                 )
#                 request.session['user_id'] = user.id
#                 messages.success(request, "註冊成功，已自動登入")
#                 return redirect('login_redirect')
    
#     return render(request, '01_userlogin.html')



def login_redirect(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login_page')  # 沒登入，導回登入

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return redirect('user_login_page')

    # 判斷是否已有資料
    if ThisUserProfile.objects.filter(gmail__iexact=user.email).exists():
        return redirect('user_data')  # 有資料導去資料頁
    else:
        return redirect('create_user_profile')  # 無資料導去填寫頁




##google登入


def profile(request):
    user = request.user
    if user.is_authenticated:
        try:
            google_login = user.social_auth.filter(provider='google-oauth2').first()
            extra_data = google_login.extra_data if google_login else {}
            return render(request, 'profile.html', {'extra_data': extra_data})
        except Exception as e:
            return render(request, 'profile.html', {'error': str(e)})
    return redirect('login')


# def profile(request):
#     user = request.user
#     if user.is_authenticated:
#         try:
#             google_login = user.social_auth.filter(provider='google-oauth2').first()
#             extra_data = google_login.extra_data
#             google_id = google_login.uid
#             email = user.email
#             name = extra_data.get('name')
#             picture = extra_data.get('picture')

#             return render(request, 'profile.html', {
#                 'google_id': google_id,
#                 'email': email,
#                 'name': name,
#                 'picture': picture,
#             })
#         except UserSocialAuth.DoesNotExist:
#             return render(request, 'profile.html', {
#                 'error': '此帳號不是由 Google 登入',
#             })
#     return redirect('login')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # 登出並清除 session
    return redirect('index')  # 重定向到登入頁



####登入後填表的

# def create_user_profile(request):
#     user = request.user
#     social_user = UserSocialAuth.objects.filter(user=user, provider='google-oauth2').first()
#     if social_user:
#         gmail = social_user.extra_data.get('email', '')
#     else:
#         gmail = ''


#     if request.method == 'POST':
#         # 根據當前登入的使用者資料創建或更新 ThisUserProfile
#         profile, created = ThisUserProfile.objects.update_or_create(
#             gmail=gmail,  # 使用 gmail 作為識別
#             defaults={
#                 'username': request.POST.get('username'),
#                 'default_nickname1': request.POST.get('default_nickname1'),
#                 'default_nickname2': request.POST.get('default_nickname2'),
#                 'emergency_contact_phone': request.POST.get('emergency_contact_phone'),
#                 'emergency_contact_gmail': request.POST.get('emergency_contact_gmail'),
#                 'default_message': request.POST.get('default_message'),
#                 'self_intro': request.POST.get('self_intro'),
#             }
#         )

#         return render(request, 'thank_you.html')

#     return render(request, 'usdata.html', {'gmail': gmail})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ThisUserProfile, UserProfile

from django.shortcuts import get_object_or_404

def create_user_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "請先登入")
        return redirect('userlogin')

    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        gmail = user.email  # 用登入的user email做唯一key
        default_nickname1 = request.POST.get('default_nickname1', '')
        default_nickname2 = request.POST.get('default_nickname2', '')
        emergency_contact_phone = request.POST.get('emergency_contact_phone', '')
        emergency_contact_gmail = request.POST.get('emergency_contact_gmail', '')
        default_message = request.POST.get('default_message', '')
        self_intro = request.POST.get('self_intro', '')
        user_images = request.FILES.get('profile_image')

        ThisUserProfile.objects.update_or_create(
            gmail=gmail,
            defaults={
                'username': username,
                'default_nickname1': default_nickname1,
                'default_nickname2': default_nickname2,
                'emergency_contact_phone': emergency_contact_phone,
                'emergency_contact_gmail': emergency_contact_gmail,
                'default_message': default_message,
                'self_intro': self_intro,
                'user_images': user_images,
            }
        )

        messages.success(request, "資料已成功儲存！")
        return redirect('user_data')

    return render(request, 'usdata.html', {'gmail': user.email})





# def create_user_profile(request):
#     if request.method == 'POST':
#         gmail = request.session.get('google_email')  # 從登入流程取得
#         username = request.POST['username']
#         ...
#         # 透過 session 拿到 email
#         user = UserProfile.objects.get(id=user_id)
#         gmail = user.email  # 🔥 確保 gmail 是對的

#         ThisUserProfile.objects.update_or_create(
#             gmail=gmail,
#             defaults={
#                 'username': request.POST.get('username'),
#                 'default_nickname1': request.POST.get('default_nickname1'),
#                 'default_nickname2': request.POST.get('default_nickname2'),
#                 'emergency_contact_phone': request.POST.get('emergency_contact_phone'),
#                 'emergency_contact_gmail': request.POST.get('emergency_contact_gmail'),
#                 'default_message': request.POST.get('default_message'),
#                 'self_intro': request.POST.get('self_intro'),
#             }
#         )

#         return redirect('user_dashboard')
#     return render(request, 'usdata.html')


def update_user_profile(request):
    if request.method == 'POST':
        # 確保圖片檔案會被儲存
        profile_image = request.FILES.get('profile_image')  # 取得圖片檔案
        username = request.POST['username']
        gmail = request.POST['gmail']
        default_nickname1 = request.POST.get('default_nickname1', '')
        default_nickname2 = request.POST.get('default_nickname2', '')
        emergency_contact_phone = request.POST.get('emergency_contact_phone', '')
        emergency_contact_gmail = request.POST.get('emergency_contact_gmail', '')
        default_message = request.POST.get('default_message', '')
        self_intro = request.POST.get('self_intro', '')

        # 更新資料或創建新資料
        user_profile, created = ThisUserProfile.objects.update_or_create(
            gmail=gmail,
            defaults={
                'username': username,
                'default_nickname1': default_nickname1,
                'default_nickname2': default_nickname2,
                'emergency_contact_phone': emergency_contact_phone,
                'emergency_contact_gmail': emergency_contact_gmail,
                'default_message': default_message,
                'self_intro': self_intro,
                'user_images': profile_image,  # 儲存圖片
            }
        )

        return redirect('profile')  # 根據需要修改返回的 URL

    return render(request, 'thank_you.html')

def user_data_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login_page')

    user = get_object_or_404(UserProfile, id=user_id)
    profile = ThisUserProfile.objects.filter(gmail=user.email).first()
    return render(request, 'user_data.html', {'profile': profile})
# views.py
from django.shortcuts import redirect

def this_user_profile_redirect(request):
    # 你可以判斷條件再決定跳去哪，這裡簡單示範直接跳到 create_user_profile
    return redirect('create_user_profile')  # 導向 /this_user_profile/create/


##登入後顯示資料
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .models import UserProfile, ThisUserProfile

def user_login_page(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = UserProfile.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id  # 記錄 session
                    messages.success(request, "登入成功！")
                    return redirect('login_redirect')  # 登入成功導到判斷頁
                else:
                    messages.error(request, "密碼錯誤")
            except UserProfile.DoesNotExist:
                messages.error(request, "帳號不存在")

        elif 'register' in request.POST:
            email = request.POST.get('email')
            nickname = request.POST.get('nickname')
            password = request.POST.get('password')

            if UserProfile.objects.filter(email=email).exists():
                messages.error(request, "此帳號已被註冊")
            else:
                hashed_pw = make_password(password)
                user = UserProfile.objects.create(
                    email=email,
                    nickname=nickname,
                    password=hashed_pw
                )
                request.session['user_id'] = user.id
                messages.success(request, "註冊成功，已自動登入")
                return redirect('login_redirect')  # 註冊後同樣導到判斷頁

    return render(request, '01_userlogin.html')




def google_login_success(request):
    gmail = request.session.get('google_email')  # 假設你存在 session 裡
    if not gmail:
        return redirect('login')  # 防呆

    try:
        profile = ThisUserProfile.objects.get(gmail=gmail)
        # 有資料，導向使用者主頁
        return redirect('user_dashboard')
    except ThisUserProfile.DoesNotExist:
        # 沒資料，導向填寫基本資料表單
        return redirect('create_user_profile')





from django.http import JsonResponse
from .models import Incident

def incident_list(request):
    incidents = Incident.objects.all().order_by('-time')
    data = [
        {
            'description': incident.description,
            'lat': incident.latitude,
            'lng': incident.longitude,
            'time': incident.time.strftime('%Y-%m-%d %H:%M')
        }
        for incident in incidents
    ]
    return JsonResponse(data, safe=False)


###地圖讀資料測試

from django.shortcuts import render    

def lookup_page(request):
    return render(request, '0257.html')

def show_map(request):
    # 處理邏輯
    return render(request, 'map0257.html')




#--------------------------------01--------------------------------------------------------
# -------------------------------- submit_report（我要填單功能） --------------------------------
# myapp/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from functools import wraps
import json

from .models import PemapAll

# def login_required_session(view_func):
#     @wraps(view_func)
#     def wrapped_view(request, *args, **kwargs):
#         user_id = request.session.get('user_id')
#         print(f"Debug: session user_id = {user_id}")  # 測試用，正式可註解掉
#         if not user_id:
#             print("未登入，導向登入頁")
#             return redirect('userlogin')  # 確認此名稱是你登入頁的url name
#         return view_func(request, *args, **kwargs)
#     return wrapped_view



#!!!!!!!!!!!!!!!!!!!!!好像是思璇的要說!!!!!!!!!!!!!!!!!!!
#
#
# @csrf_exempt
# def submit_report(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)

#             # 自動產生 poster_id（例如用目前時間戳 + email）
#             poster_id = int(timezone.now().strftime("%Y%m%d%H%M%S"))
 
#             display_name = data.get('display_name', '')
#             kind = data.get('kind', '')
#             reason = data.get('reason', '')
#             address = data.get('address', '')

#             # 分離經緯度
#             latitude = 0
#             longitude = 0
#             if ',' in address:
#                 parts = [p.strip() for p in address.split(',')]
#                 if len(parts) >= 2:
#                     try:
#                         latitude = float(parts[0])
#                         longitude = float(parts[1])
#                     except ValueError:
#                         pass  # 維持預設 0

#             img_url = data.get('img_url', '')  # 這就是 base64

#             # 寫入資料表
#             PemapAll.objects.create(
#                 poster_id=poster_id,
#                 display_name=display_name,
#                 kind=kind,
#                 reason=reason,
#                 address=address,
#                 latitude=latitude,
#                 longitude=longitude,
#                 img_url=img_url,
#                 time_created=timezone.now(),
#                 review_status="待審核"
#             )

#             return JsonResponse({"status": "success"})

#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)})
#     else:
#         return JsonResponse({"status": "error", "message": "Invalid method"})
    
def room(request, room_name):
    return render(request, 'test_0610chatroom.html', {'room_name': room_name})
#report_list_view
from django.contrib.auth.decorators import login_required
@login_required(login_url='/01userlogin/')
def report_list_view(request):
    user_reports = list(PemapAll.objects.all().order_by('-time_created'))
    # 加入反向編號（從最大值開始）
    for i, report in enumerate(user_reports):
        report.reverse_id = len(user_reports) - i
    return render(request, 'report_list.html', {'reports': user_reports})

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
import json

from .models import PemapAll

# ✅ 顯示 report.html 表單頁面（未登入會導到登入頁）
@login_required(login_url='/01userlogin/')
def report_view(request):
    return render(request, 'report.html')


# ✅ 接收 POST 資料 API（表單送出時）
# @login_required(login_url='/01userlogin/')
import base64
import numpy as np
import uuid
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import cv2
import os
import json

from myapp.models import PemapAll  # 確保你有引入模型

# 載入人臉辨識模型
face_cascade = cv2.CascadeClassifier(
    os.path.join(settings.BASE_DIR, 'myapp/static/haarcascade_frontalface_default.xml')
)

@login_required(login_url='/01userlogin/')
@csrf_exempt
def submit_report(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user = request.user
            display_name = data.get('display_name', '')
            kind = data.get('kind', '')
            reason = data.get('reason', '')
            address = data.get('address', '')
            poster_gmail = data.get("poster_gmail", "").strip()
            is_anonymous = data.get("anonymous", False)

            # 處理經緯度
            latitude, longitude = 0, 0
            if ',' in address:
                try:
                    parts = [p.strip() for p in address.split(',')]
                    if len(parts) >= 2:
                        latitude = float(parts[0])
                        longitude = float(parts[1])
                except ValueError:
                    pass

            # ========= ✅ 圖片處理區塊 =========
            img_url = ""
            base64_img_str = data.get('img_url', '')

            if base64_img_str.startswith("data:image"):
                header, base64_str = base64_img_str.split(",", 1)
                img_data = base64.b64decode(base64_str)

                # 將圖片轉為 OpenCV 格式
                nparr = np.frombuffer(img_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # 轉灰階並偵測人臉
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 5)

                # 對每張人臉上馬賽克
                for (x, y, w, h) in faces:
                    face_roi = img[y:y + h, x:x + w]
                    small = cv2.resize(face_roi, (10, 10), interpolation=cv2.INTER_LINEAR)
                    mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
                    img[y:y + h, x:x + w] = mosaic

                # 產生唯一檔名
                filename = f"img_{uuid.uuid4().hex}.jpg"
                media_dir = os.path.join(settings.MEDIA_ROOT, "processed_images")
                os.makedirs(media_dir, exist_ok=True)
                processed_img_path = os.path.join(media_dir, filename)

                # 儲存處理後圖片
                cv2.imwrite(processed_img_path, img)

                # 再次轉成 base64 編碼（這是處理後的圖片）
                _, img_encoded = cv2.imencode('.jpg', img)
                img_base64_bytes = base64.b64encode(img_encoded.tobytes()).decode('utf-8')

                # 儲存 base64 字串為文字檔
                base64_txt_path = os.path.join(media_dir, f"{filename}.base64.txt")
                with open(base64_txt_path, "w", encoding="utf-8") as f:
                    f.write(img_base64_bytes)

                # 儲存在 DB 裡的圖片網址
                img_url = f"data:image/jpeg;base64,{img_base64_bytes}"
            # ========= ✅ 圖片處理結束 =========

            # ========== AI 初步審核 ==========
            description = reason.strip()
            sensitive_categories = {
                '仇恨言論': ['仇恨', '恨死', '殺光', '滅絕'],
                '暴力': ['暴力', '打死', '砍', '攻擊', '虐待'],
                '歧視': ['歧視', '種族主義', '排擠', '偏見'],
            }
            case_keywords = [
                '案件', '事件', '警方', '警察', '報警', '報案', '證據',
                '被跟蹤', '跟蹤', '尾隨', '偷拍', '性騷擾', '偷窺', '侵入',
                '陌生男子', '紅衣男子', '追蹤', '恐嚇', '求助', '監視'
            ]

            if not description or len(description) < 10:
                review_status = '描述內容過短，不足以判斷'
            else:
                has_sensitive_word = any(
                    keyword in description
                    for keywords in sensitive_categories.values()
                    for keyword in keywords
                )
                is_case_related = any(kw in description for kw in case_keywords)

                review_status = '需再由人工審核' if has_sensitive_word or not is_case_related else '人工審核通過'

            if is_anonymous:
                poster_gmail = "anonymous@gmail.com"

            # 存入資料庫
            PemapAll.objects.create(
                user=user,
                display_name=display_name,
                kind=kind,
                reason=reason,
                address=address,
                latitude=latitude,
                longitude=longitude,
                img_url=img_url,
                time_created=timezone.now(),
                review_status=review_status,
                admin_id=99999,
                poster_gmail=poster_gmail,
            )

            return JsonResponse({"status": "success", "review_status": review_status})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid method"})

# @csrf_exempt
# def submit_report(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)

#             user = request.user  # ✅ 登入使用者
#             display_name = data.get('display_name', '')
#             kind = data.get('kind', '')
#             reason = data.get('reason', '')
#             address = data.get('address', '')

#             # 經緯度處理
#             latitude = 0
#             longitude = 0
#             if ',' in address:
#                 parts = [p.strip() for p in address.split(',')]
#                 if len(parts) >= 2:
#                     try:
#                         latitude = float(parts[0])
#                         longitude = float(parts[1])
#                     except ValueError:
#                         pass

#             img_url = data.get('img_url', '')

#             # ====== AI 初步審核 ======
#             description = reason.strip()
#             sensitive_categories = {
#                 '仇恨言論': ['仇恨', '恨死', '殺光', '滅絕'],
#                 '暴力': ['暴力', '打死', '砍', '攻擊', '虐待'],
#                 '歧視': ['歧視', '種族主義', '排擠', '偏見'],
#             }
#             case_related_keywords = [
#                 '案件', '事件', '警方', '警察', '報警', '報案', '證據',
#                 '被跟蹤', '跟蹤', '尾隨', '偷拍', '性騷擾', '偷窺', '侵入',
#                 '陌生男子', '紅衣男子', '追蹤', '恐嚇', '求助', '監視'
#             ]

#             if not description or len(description) < 10:
#                 review_status = '描述內容過短，不足以判斷'
#             else:
#                 has_sensitive_word = any(
#                     keyword in description
#                     for keywords in sensitive_categories.values()
#                     for keyword in keywords
#                 )
#                 is_case_related = any(kw in description for kw in case_related_keywords)

#                 if has_sensitive_word or not is_case_related:
#                     review_status = '需再由人工審核'
#                 else:
#                     review_status = '人工審核通過'
                    
#             # =========================

#             PemapAll.objects.create(
#                 user=user,
#                 display_name=display_name,
#                 kind=kind,
#                 reason=reason,
#                 address=address,
#                 latitude=latitude,
#                 longitude=longitude,
#                 img_url=img_url,
#                 time_created=timezone.now(),
#                 review_status=review_status,
#                 admin_id=99999,
#                 poster_gmail=data.get("poster_gmail"),
#             )

#             return JsonResponse({"status": "success", "review_status": review_status})

#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)})
#     else:
#         return JsonResponse({"status": "error", "message": "Invalid method"})

#-----------------about---------------------------
from django.shortcuts import render, redirect
from .models import ThisUserProfile
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
import base64

@login_required(login_url='/01userlogin/')
def about(request):
    user = request.user
    extra_data = {}
    google_login = user.social_auth.filter(provider='google-oauth2').first()
    if google_login:
        extra_data = google_login.extra_data

    if request.method == 'POST':
        data = json.loads(request.body)

        nickname1 = data.get('nickname1', '')
        nickname2 = data.get('nickname2', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        intro = data.get('intro', '')
        default_message = data.get('default_message', '')
        show_name_option = data.get('show_name_option', '1')
        base64_image = data.get('base64_image', '')

        # 以登入使用者的 email 找 profile (不以前端送的 email 找)
        profile, created = ThisUserProfile.objects.get_or_create(gmail=user.email)

        profile.username = extra_data.get('name', user.username)
        profile.gmail = email  # 可以更新 gmail 欄位
        profile.default_nickname1 = nickname1
        profile.default_nickname2 = nickname2
        profile.emergency_contact_phone = phone
        profile.emergency_contact_gmail = email
        profile.default_message = default_message
        profile.self_intro = intro
        profile.status_color = '#63b3ed'

        if base64_image:
            profile.user_images = base64_image  # 存成 base64 字串

        profile.save()

        return JsonResponse({'redirect_url': '/about/'})

    # GET 方法顯示畫面
    db_profile = ThisUserProfile.objects.filter(gmail=user.email).first()
    profile = {
        'google_name': extra_data.get('name', user.username),
        'nickname1': db_profile.default_nickname1 if db_profile else '',
        'nickname2': db_profile.default_nickname2 if db_profile else '',
        'default_message': db_profile.default_message if db_profile else '',
        'email': db_profile.gmail if db_profile else extra_data.get('email', user.email),
        'phone': db_profile.emergency_contact_phone if db_profile else '',
        'intro': db_profile.self_intro if db_profile else '',
        'show_name_option': int(db_profile.status_color) if db_profile and db_profile.status_color.isdigit() else 1,
        'avatar_url': db_profile.user_images or extra_data.get('picture', None),
    }

    return render(request, 'about.html', {
        'user': user,
        'profile': profile,
    })
#----------------store---------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
@login_required(login_url='/01userlogin/')
def business_upload(request):
    return render(request, 'business_upload.html')

@login_required(login_url='/01userlogin/')
@csrf_exempt
def submit_store(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            timestamp = int(timezone.now().timestamp())

            store = StoreAll(
                user=request.user,
                st_id=timestamp,
                poster_id=int(data.get('poster_id')),  # 從前端傳入 1 或 2 等已存在的 ID
                store_name=data.get('store_name') or data.get('bs_name'),
                address=data.get('address') or data.get('bs_address'),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                business_hours=data.get('business_hours'),
                phone=data.get('phone') or data.get('bs_phone'),
                created_at=data.get('created_at'),
                reviewed_at=None,
                review_status="pending",
                admin_id = 9999,
                poster_gmail=data.get("poster_gmail"),
            )
            store.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

from django.contrib.auth.decorators import login_required
@login_required(login_url='/01userlogin/')
def business_list_view(request):
    user_stores = list(StoreAll.objects.all().order_by('-created_at'))  # 依照 created_at 遞減排序
    total = len(user_stores)
    for i, store in enumerate(user_stores):
        store.reverse_id = total - i  # 編號從總數開始往下減
    return render(request, 'business_list.html', {'stores': user_stores})



#test_0610chatroom 試寫聊天室
from django.shortcuts import render

def room(request, room_name):
    return render(request, 'test_0610chatroom.html', {
        'room_name': room_name
    })


##測試資料能不能放到地圖上
##暫時使用的是沒審核的pemap_all資料庫
# from django.http import JsonResponse
# from .models import Report

# def reports_json(request):
#     reports = Report.objects.filter(review_status='已審核').values(
#         'latitude', 'longitude', 'display_name', 'reason', 'time_created'
#     )
#     data = list(reports)
#     return JsonResponse(data, safe=False)

def reports_json(request):
    data = PemapAll.objects.filter(review_status='3').order_by('-time_reviewed')
    results = []
    for item in data:
        if item.latitude is not None and item.longitude is not None:
            results.append({
                'latitude': float(item.latitude),
                'longitude': float(item.longitude),
                'display_name': item.display_name,
                'reason': item.reason,
                'time_created': item.time_created.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse(results, safe=False)


# from django.http import JsonResponse
# from .models import PemapAll  # 改成引用 PemapAll

# def reports_json(request):
#     reports = PemapAll.objects.filter(review_status='0').values(
#         'latitude', 'longitude', 'display_name', 'reason', 'time_created'
#     )
#     data = list(reports)
#     return JsonResponse(data, safe=False)



##處理管理員對pemap資料狀態
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import PemapAll


def pemap_approve(request, p_id, stage):
    obj = get_object_or_404(PemapAll, p_id=p_id)
    if stage == 1 and obj.review_status == 0:
        obj.review_status = 1
        obj.time_reviewed = timezone.now()
        obj.save()
        messages.success(request, f"第一次審核通過: {obj}")
    elif stage == 2 and obj.review_status == 1:
        obj.review_status = 2
        obj.time_reviewed = timezone.now()
        obj.save()
        messages.success(request, f"第二次審核通過: {obj}")
    else:
        messages.error(request, "審核狀態不符，無法審核")
    return redirect(request.META.get('HTTP_REFERER', '/admin/'))\
    

from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import PemapAll

# @method_decorator(staff_member_required, name='dispatch')
class PemapAllListView(ListView):
    model = PemapAll
    template_name = 'pemapall_list.html'
    context_object_name = 'pemap_list'

# @method_decorator(staff_member_required, name='dispatch')
class PemapAllUpdateView(UpdateView):
    model = PemapAll
    fields = ['review_status']
    template_name = 'pemapall_update.html'
    pk_url_kwarg = 'p_id'
    success_url = reverse_lazy('pemap_list')

    def form_valid(self, form):
        form.instance.time_reviewed = timezone.now()
        return super().form_valid(form)


#================================================================================================
# #仇恨言論檢測模組

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def show_judge_page(request):
    return render(request, '99judge.html')



import openai
from openai import OpenAI

#OpenAI API 金鑰

client = OpenAI(api_key="我的先拿下")




from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def ai_judge(request):
    if request.method != 'POST':
        return JsonResponse({'result': 2, 'reason': '請使用 POST 請求'})

    try:
        data = json.loads(request.body)
        description = data.get('description', '').strip()

        if not description or len(description) < 10:
            return JsonResponse({'result': 1, 'reason': '描述內容過短，不足以判斷'})

        # 敏感詞分類詞庫
        sensitive_categories = {
            '仇恨言論': ['仇恨', '恨死', '殺光', '滅絕'],
            '暴力': ['暴力', '打死', '砍', '攻擊', '虐待'],
            '歧視': ['歧視', '種族主義', '排擠', '偏見'],
        }

        # 檢查是否含敏感詞
        has_sensitive_word = any(
            keyword in description
            for keywords in sensitive_categories.values()
            for keyword in keywords
        )

        # 案件關聯詞彙
        case_related_keywords = [
            '案件', '事件', '警方', '警察', '報警', '報案', '證據',
            '被跟蹤', '跟蹤', '尾隨', '偷拍', '性騷擾', '偷窺', '侵入',
            '陌生男子', '紅衣男子', '追蹤', '恐嚇', '求助', '監視'
        ]
        is_case_related = any(kw in description for kw in case_related_keywords)

        if has_sensitive_word or not is_case_related:
            return JsonResponse({'result': 2, 'reason': '需再由人工審核'})

        return JsonResponse({'result': 0, 'reason': '人工審核通過'})

    except Exception as e:
        return JsonResponse({'result': 2, 'reason': f'系統錯誤：{str(e)}'})





###容易爆額度先關
# 原本要用openai的chatgpt但我沒付費額度會不夠
# 就先用上面比較簡單的判斷方式

# @csrf_exempt
# def ai_judge(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             description = data.get('description', '')

#             if not description.strip():
#                 return JsonResponse({'result': 0, 'reason': '描述為空'})

#             prompt = f"""
# 請判斷以下文字描述是否過於主觀，包含仇恨言論、恐懼煽動，或者不當內容？或是對與案件描述太無關？
# 若沒有，請只回覆「通過」；若有問題，請說明理由。

# 文字描述：
# {description}
# """

#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0
#             )

#             reply = response.choices[0].message.content.strip()

#             if "通過" in reply:
#                 return JsonResponse({'result': 1})
#             else:
#                 return JsonResponse({'result': 0, 'reason': reply})

#         except Exception as e:
#             return JsonResponse({'result': 0, 'reason': f"系統錯誤：{str(e)}"})

#     return JsonResponse({'result': 0, 'reason': '請使用 POST 請求'})
###容易爆額度先關


#================================================================================================
#管理者登入
from django.shortcuts import render, redirect
from .models import Admins

from django.shortcuts import render, redirect
from .models import Admins

def admin_login(request):
    if request.method == 'POST':
        admin_gmail = request.POST.get('admin_gmail')
        password = request.POST.get('password')

        try:
            admin = Admins.objects.get(admin_gmail=admin_gmail)
            if admin.password == password:
                # 登入成功，寫入 session
                request.session['admin_id'] = admin.admin_id
                request.session['admin_name'] = admin.name
                return redirect('admin_interview')  # 成功跳轉
            else:
                return render(request, 'admin_login.html', {'error': '密碼錯誤'})
        except Admins.DoesNotExist:
            return render(request, 'admin_login.html', {'error': '帳號不存在'})

    return render(request, 'admin_login.html')


#--------管理員自介-------
from .forms import AdminProfileForm

def admin_interview(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('admin_login')

    try:
        admin = Admins.objects.get(admin_id=admin_id)
    except Admins.DoesNotExist:
        return redirect('admin_login')

    if request.method == 'POST':
        form = AdminProfileForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            message = "✅ 資料已更新成功"
        else:
            message = "❌ 資料更新失敗，請檢查輸入"
    else:
        form = AdminProfileForm(instance=admin)
        message = None

    return render(request, 'admin_interview.html', {
    'form': form,
    'message': message,
    'admin_name': admin.name,
    'admin_id': admin.admin_id,
    })


#-------管理員登出-----
from django.shortcuts import redirect

def admin_logout(request):
    request.session.flush()  # 清空所有 session 資料
    return redirect('admin_login')  # 登出後導向登入頁


#---------------事件審核的--------------------------------------------------------------------
# from django.shortcuts import render
# from .models import PemapAll

# def pemap_judge(request):
#     all_data = PemapAll.objects.all().order_by('-time_created')  # 最新的在上
#     return render(request, 'pemap_judge.html', {'data': all_data})
from django.shortcuts import render, redirect
from .models import PemapAll, Admins

def pemap_judge(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')

    if not admin_id:
        return redirect('admin_login')  # 未登入導回登入頁

    all_data = PemapAll.objects.all().order_by('-time_created')  # 最新的在上

    return render(request, 'pemap_judge.html', {
        'data': all_data,
        'admin_id': admin_id,
        'admin_name': admin_name,
    })



from django.shortcuts import render, redirect
from .models import StoreAll

def store_judge(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')

    if not admin_id:
        return redirect('admin_login')  # 尚未登入，導向登入頁

    store_list = StoreAll.objects.all().order_by('-created_at')  # 最新在最上面

    return render(request, 'store_judge.html', {
        'store_list': store_list,
        'admin_id': admin_id,
        'admin_name': admin_name,
    })



#--step1
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import PemapAll

# def pemap_judge_step1(request, p_id):
#     form_data = get_object_or_404(PemapAll, p_id=p_id)

#     if request.method == 'POST':
#         new_status = request.POST.get('review_status')
#         if new_status is not None and new_status.isdigit():
#             form_data.review_status = int(new_status)
#             form_data.time_reviewed = timezone.now()

#             # 👉 記錄修改人（例如存 log、或印出 log）
#             admin_name = request.session.get('admin_name', '未知管理員')
#             print(f"表單 {p_id} 被 {admin_name} 修改狀態為 {new_status}")

#             form_data.save()
#             return redirect('pemap_judge')  # 完成後回事件清單頁

#     return render(request, 'pemap_judge_step1.html', {
#         'item': form_data
#     })



from django.urls import reverse

def pemap_judge_step1(request, p_id):
    form_data = get_object_or_404(PemapAll, p_id=p_id)

    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name', '未知管理員')

    if not admin_id:
        return redirect('admin_login')

    if request.method == 'POST':
        new_status = request.POST.get('review_status')
        if new_status is not None and new_status.isdigit():
            new_status_int = int(new_status)
            form_data.review_status = new_status_int
            form_data.time_reviewed = timezone.now()
            form_data.admin_id = admin_id  

            print(f"表單 {p_id} 被 {admin_name} 修改狀態為 {new_status_int}")

            form_data.save()

            if new_status_int == 4:  # 人工審核未通過
                url = reverse('admin_send_email') + f'?p_id={p_id}'
                return redirect(url)

            return redirect('pemap_judge')

    return render(request, 'pemap_judge_step1.html', {
        'item': form_data,
        'admin_id': admin_id,
        'admin_name': admin_name,
    })

# from django.shortcuts import render, get_object_or_404, redirect
# from .models import PemapAll
# from django.utils import timezone  # ⚠️ 別忘記引入這行！

# def pemap_judge_step1(request, p_id):
#     form_data = get_object_or_404(PemapAll, p_id=p_id)

#     # ✅ 抓出 session 中的管理員資料
#     admin_id = request.session.get('admin_id')
#     admin_name = request.session.get('admin_name', '未知管理員')

#     if not admin_id:
#         return redirect('admin_login')  # 尚未登入就導向登入頁

#     if request.method == 'POST':
#         new_status = request.POST.get('review_status')
#         if new_status is not None and new_status.isdigit():
#             form_data.review_status = int(new_status)
#             form_data.time_reviewed = timezone.now()
#             form_data.admin_id = admin_id  


#             print(f"表單 {p_id} 被 {admin_name} 修改狀態為 {new_status}")

#             form_data.save()
#             return redirect('pemap_judge')

#     return render(request, 'pemap_judge_step1.html', {
#         'item': form_data,
#         'admin_id': admin_id,
#         'admin_name': admin_name,
#     })


from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import StoreAll

def store_judge_step1(request, st_id):
    store = get_object_or_404(StoreAll, st_id=st_id)

    # 抓登入管理員資訊
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name', '未知管理員')

    # 如果尚未登入，導向登入頁
    if not admin_id:
        return redirect('admin_login')

    if request.method == 'POST':
        new_status = request.POST.get('review_status')
        if new_status:
            store.review_status = new_status
            store.reviewed_at = timezone.now()
            store.admin_id = admin_id

            print(f"店家 {st_id} 被 {admin_name} 審核為 {new_status}")
            store.save()
            return redirect('store_judge')  # 審核完返回列表頁

    return render(request, 'store_judge_step1.html', {
        'store': store,
        'admin_id': admin_id,
        'admin_name': admin_name,
    })



#--商家表單拒絕後--
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import StoreAll

# def store_judge_view(request, st_id):
#     store = get_object_or_404(StoreAll, st_id=st_id)

#     if request.method == 'POST':
#         review_status = request.POST.get('review_status')
#         store.review_status = review_status
#         store.save()

#         if review_status == 'rejected':
#             return redirect('store_step2', st_id=store.st_id)  # 導向 step2

#         return redirect('store_judge')  # 若非拒絕就回清單

#     return render(request, 'store_judge_step1.html', {'store': store})


# def store_step2_view(request, st_id):
#     store = get_object_or_404(StoreAll, st_id=st_id)
#     return render(request, 'store_step2.html', {'store': store})
# views.py

#--商家表單拒絕後--
from django.shortcuts import render, get_object_or_404, redirect
from .models import StoreAll

def store_judge_view(request, st_id):
    store = get_object_or_404(StoreAll, st_id=st_id)

    if request.method == 'POST':
        review_status = request.POST.get('review_status')
        store.review_status = review_status
        store.save()

        if review_status == 'rejected':
            return redirect('store_step2', st_id=store.st_id)

        return redirect('store_judge')

    return render(request, 'store_judge_step1.html', {'store': store})


def store_step2_view(request, st_id):
    store = get_object_or_404(StoreAll, st_id=st_id)
    return render(request, 'store_step2.html', {'store': store})








import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import PemapAll

#--------- 使用 Google Maps API 反查地址 ----------
def reverse_geocode_google(lat, lng):
    api_key = 'AIzaSyAUuPZMMJvgVWftmqVyzfX8mKTwMX4kA6o'
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            if result['results']:
                return result['results'][0]['formatted_address']
    except Exception as e:
        print("Google Maps 反查失敗：", e)
    return "無法取得地址"

#--------- 顯示單筆資料的細節頁面 ----------
def review_detail(request, pk):
    item = get_object_or_404(PemapAll, pk=pk)

    try:
        lat_str, lng_str = map(str.strip, item.address.split(","))
        lat = float(lat_str)
        lng = float(lng_str)
        item.human_address = reverse_geocode_google(lat, lng)
    except Exception as e:
        print("經緯度解析失敗：", e)
        item.human_address = "無法解析經緯度"

    return render(request, 'pemap_judge.html', {
        'item': item,
    })

#--------- 管理員登入後首頁 ----------
def admin_index(request):
    if 'admin_id' not in request.session:
        return redirect('admin_login')

    context = {
        'admin_id': request.session.get('admin_id'),
        'admin_name': request.session.get('admin_name'),
    }

    return render(request, 'admin_index.html', context)

#---------------管理員註冊-----------------------
from django.shortcuts import render
from .models import Admins  # 根據你的 models 路徑
from django.db import IntegrityError

def admin_register(request):
    message = None
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        admin_gmail = request.POST.get('admin_gmail')
        bio = request.POST.get('bio')

        try:
            admin = Admins(
                name=name,
                password=password,
                phone=phone,
                admin_gmail=admin_gmail,
                bio=bio
            )
            admin.save() 
            message = "註冊成功！"

        except IntegrityError:
            message = "Email 已存在，請使用其他 Email 註冊。"

    return render(request, 'admin_register.html', {'message': message})


#--------管理員看自己審核的-------

from django.shortcuts import render, redirect
from .models import PemapAll

def admin_decide_view(request):
    # 從 session 抓出登入的管理員 id
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name', '未知管理員')

    # 如果沒登入，導向登入頁
    if not admin_id:
        return redirect('admin_login')

    # 查出這個管理員有改過的資料（已經改過 review_status 的）
    decided_list = PemapAll.objects.filter(admin_id=admin_id).order_by('-time_reviewed')

    return render(request, 'admin_decide.html', {
        'admin_id': admin_id,
        'admin_name': admin_name,
        'decided_list': decided_list
    })
    

from .models import StoreAll

def store_decide(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')

    if not admin_id:
        return redirect('admin_login')

    decided_list = StoreAll.objects.filter(
        review_status__in=['approved', 'rejected'],  # 根據你 review_status 的設定來調整
        admin_id=admin_id
    ).order_by('-reviewed_at')

    return render(request, 'admin_decide_st.html', {
        'decided_list': decided_list,
        'admin_id': admin_id,
        'admin_name': admin_name,
    })

    
#----------------使用者 事件地圖--------------
from django.http import JsonResponse
from .models import PemapAll

def approved_locations_api(request):
    approved = PemapAll.objects.filter(review_status='已通過')  # 只取審核通過的
    data = []

    for item in approved:
        data.append({
            'id': item.p_id,
            'title': item.display_name,
            'kind': item.kind,
            'reason': item.reason,
            'lat': item.latitude,
            'lng': item.longitude,
        })

    return JsonResponse(data, safe=False)




# def map_view(request):
#     return render(request, '999map.html')
import json
from django.shortcuts import render
from datetime import datetime, date
from .models import PemapWithSubkind  # 或你的模型名稱

def datetime_handler(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def map_view(request):
    # 取出你需要的欄位，調整欄位名稱和模型
    reports = PemapWithSubkind.objects.values(
        "display_name", "kind", "subkind", "latitude", "longitude", "address", "img_url", "time_created"
    )
    reports_list = list(reports)

    # 將包含 datetime 的 list 用 json.dumps 並轉成 ISO 格式字串
    reports_json = json.dumps(reports_list, default=datetime_handler, ensure_ascii=False)

    return render(request, "999map.html", {
        "reports_json": reports_json
    })


    
#-----------使用者 商家地圖-----------
from django.http import JsonResponse
from django.shortcuts import render
from .models import StoreAll

# 頁面：商家地圖顯示頁面
def store_map_view(request):
    return render(request, 'store_map.html')

# API：取得審核通過的商家資料
def store_data_api(request):
    approved_stores = StoreAll.objects.filter(review_status='approved')

    data = [
        {
            'st_id': store.st_id,
            'store_name': store.store_name,
            'address': store.address,
            'phone': store.phone,
            'latitude': store.latitude,
            'longitude': store.longitude,
        }
        for store in approved_stores
        if store.latitude is not None and store.longitude is not None
    ]
    return JsonResponse(data, safe=False)



# from .models import StoreAll

# def store_data_api(request):
#     approved_stores = StoreAll.objects.filter(review_status='approved')
#     data = [
#         {
#             'st_id': store.st_id,
#             'store_name': store.store_name,
#             'address': store.address,
#             'phone': store.phone,
#             'latitude': store.latitude,
#             'longitude': store.longitude,
#         }
#         for store in approved_stores
#         if hasattr(store, 'latitude') and hasattr(store, 'longitude')  # 如果你有這兩欄
#     ]
#     return JsonResponse(data, safe=False)

# def store_map_view(request):
#     return render(request, 'store_map.html')


#------------交流區貼文的部分-------

from .models import ChatInteraction
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
import bleach

ALLOWED_TAGS = ['a']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'target', 'rel']
}

# 發文
@login_required(login_url='/01userlogin/')
def post(request):
    if request.method == 'POST':
        nickname = "(匿名)"
        bgcolor = request.POST.get('bgcolor')
        avatar_style = request.POST.get('avatar_style')
        title = request.POST.get('title')
        raw_content = request.POST.get('content')

        clean_content = bleach.clean(
            raw_content,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=['http', 'https'],
            strip=True
        )

        avatar_url = f"https://api.dicebear.com/7.x/{avatar_style}/svg?seed={nickname}&backgroundColor={bgcolor}"

        ChatInteraction.objects.create(
            user=request.user,
            nickname=nickname,
            bgcolor=bgcolor,
            avatar_style=avatar_style,
            avatar_url=avatar_url,
            title=title,
            message_content=clean_content,
            created_at=timezone.now()
        )

        return redirect('post_display')

    return render(request, 'post.html')


# 貼文展示
def post_display(request):
    posts = ChatInteraction.objects.all().order_by('-created_at')
    return render(request, 'post_display.html', {'posts': posts})


# 編輯貼文（只能編輯自己的）
@login_required(login_url='/01userlogin/')
def edit_post(request, post_id):
    post = get_object_or_404(ChatInteraction, pk=post_id)

    if post.user_id != request.user.id:
        return HttpResponseForbidden("⚠️ 你無權編輯這篇貼文。")

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.message_content = request.POST.get('content')
        post.created_at = timezone.now()
        post.save()
        return redirect('post_display')

    return render(request, 'edit_post.html', {'post': post})


# 刪除貼文（只能刪除自己的）
@login_required(login_url='/01userlogin/')
def delete_post(request, post_id):
    post = get_object_or_404(ChatInteraction, pk=post_id)

    if post.user_id != request.user.id:
        return HttpResponseForbidden("⚠️ 你無權刪除這篇貼文。")

    if request.method == 'POST':
        post.delete()
        return redirect('post_display')

    return render(request, 'delete_post_confirm.html', {'post': post})




# from .models import ChatInteraction  # ✅ 不再匯入 ThisUserProfile
# from datetime import datetime
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# import bleach  # ✅ 引入 bleach 套件
# ALLOWED_TAGS = ['a']
# ALLOWED_ATTRIBUTES = {
#     'a': ['href', 'target', 'rel']
# }

# # ✅ bleach 白名單設定：只允許 <a> 並限制安全屬性

# @login_required(login_url='/01userlogin/')
# def post(request):
#     if request.method == 'POST':
#         # ✅ 固定暱稱為 (匿名)
#         nickname = "(匿名)"
#         bgcolor = request.POST.get('bgcolor')
#         avatar_style = request.POST.get('avatar_style')
#         title = request.POST.get('title')
#         raw_content = request.POST.get('content')

#         # ✅ 透過 bleach 淨化 HTML，僅保留安全 <a> 標籤
#         clean_content = bleach.clean(
#             raw_content,
#             tags=ALLOWED_TAGS,
#             attributes=ALLOWED_ATTRIBUTES,
#             protocols=['http', 'https'],
#             strip=True
#         )

#         avatar_url = f"https://api.dicebear.com/7.x/{avatar_style}/svg?seed={nickname}&backgroundColor={bgcolor}"

#         # ✅ 儲存進資料庫
#         ChatInteraction.objects.create(
#             user=request.user,
#             nickname=nickname,
#             bgcolor=bgcolor,
#             avatar_style=avatar_style,
#             avatar_url=avatar_url,
#             title=title,
#             message_content=clean_content,
#             created_at=datetime.now()
#         )

#         return redirect('post_display')  # 發文成功轉跳至展示頁

#     return render(request, 'post.html')


# ✅ 展示頁保持不變（但顯示時可用 |safe，前提是內容已淨化）


#------------事件表單拒絕後傳送-------
from django.core.mail import send_mail
from django.http import HttpResponse

@login_required
def admin_send_email(request):
    p_id = request.GET.get('p_id')
    item = PemapAll.objects.filter(p_id=p_id).first()
    if not item:
        return HttpResponse("找不到該筆資料", status=404)

    if request.method == 'POST':
        to_email = item.poster_gmail
        subject = request.POST.get('subject', '關於您的報告審核結果')
        message = request.POST.get('message', '')

        # 寄信 (請先設定好 Django EMAIL 設定)
        try:
            send_mail(subject, message, '你的發信地址@example.com', [to_email])
            return HttpResponse("郵件已寄出")
        except Exception as e:
            return HttpResponse(f"寄信失敗: {str(e)}")

    return render(request, 'admin_send_email.html', {
        'item': item,
        'to_email': item.poster_gmail,
    })



# views.py
from rest_framework import viewsets
from .models import PemapWithSubkind
from .serializers import PemapWithSubkindSerializer

class PemapWithSubkindViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PemapWithSubkind.objects.all()
    serializer_class = PemapWithSubkindSerializer


from django.http import JsonResponse
from .models import PemapWithSubkind

def reports_with_subkind_json(request):
    # 從資料庫取得所有帶有 kind / subkind 的事件
    data = list(PemapWithSubkind.objects.values())
    return JsonResponse(data, safe=False)
