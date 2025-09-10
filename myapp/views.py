from django.shortcuts import render, get_object_or_404, redirect
from .models import TaiwanRegion, PoliceAddress, PemapAll, StoreAll#資料表的
from django.views.decorators.http import require_GET
from django.http import JsonResponse, HttpResponse
from .forms import AutoDialForm
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from datetime import datetime
from .utils import get_unreviewed_counts  


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


#禮品真的東西(主要是讓下面東西管理的東西要先登入才能編輯)
from functools import wraps

def admin_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        print("admin_login_required 被呼叫")
        if 'admin_id' in request.session:
            print("已登入")
            return view_func(request, *args, **kwargs)
        else:
            print("沒登入，導向登入頁")
            return redirect('admin_login')
    return wrapper

#教育網頁
from .models import EducationPage
from .education_forms import EducationPageUploadForm

def education_page(request):
    pages = EducationPage.objects.all()
    return render(request, 'education_page.html', {'pages': pages})

#教育網頁新增改刪
@admin_login_required
def education_list(request):
    pages = EducationPage.objects.all()
    context = {
        'pages': pages,
    }
    context.update(get_unreviewed_counts())
    return render(request, 'education_list.html', context)

@admin_login_required
def education_create(request):
    if request.method == 'POST':
        form = EducationPageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('education_list')
    else:
        form = EducationPageUploadForm()

    context = {
        'form': form,
    }
    context.update(get_unreviewed_counts())
    return render(request, 'education_form.html', context)

@admin_login_required
def education_update(request, pk):
    page = get_object_or_404(EducationPage, pk=pk)
    if request.method == 'POST':
        form = EducationPageUploadForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('education_list')
    else:
        form = EducationPageUploadForm(instance=page)
    context = {
        'form': form,
    }
    context.update(get_unreviewed_counts())
    return render(request, 'education_form.html', context)

# 顯示確認刪除畫面
def education_delete_confirm(request, pk):
    page = get_object_or_404(EducationPage, pk=pk)
    return render(request, 'education_confirm_delete.html', {'page': page})

# 真正刪除
def education_delete(request, pk):
    page = get_object_or_404(EducationPage, pk=pk)
    if request.method == 'POST':
        page.delete()
        return redirect('education_list')
    return redirect('education_delete_confirm', pk=pk)  # 若不是 POST，就導回確認頁

@admin_login_required
def education_image(request, pk):
    page = get_object_or_404(EducationPage, pk=pk)
    if page.image_url:
        return HttpResponse(page.image_url, content_type="image/png")
    return HttpResponse(status=404)


#最近警局
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
from .taiwan_regions_forms import TaiwanRegionForm

@admin_login_required
def taiwan_regions_admin(request):
    regions = TaiwanRegion.objects.all()
    return render(request, 'taiwan_regions_admin.html', {'regions': regions})

@admin_login_required
def taiwan_regions_add(request):
    if request.method == 'POST':
        form = TaiwanRegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('taiwan_regions_admin')
    else:
        form = TaiwanRegionForm()
    return render(request, 'taiwan_regions_add.html', {'form': form, 'action': '新增'})

@admin_login_required
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
from .police_forms import PoliceAddressForm
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib import messages

@admin_login_required
def police_address_list(request):
    addresses = PoliceAddress.objects.all().order_by('precinct_name')
    return render(request, 'police_address_admin.html', {'addresses': addresses})

@admin_login_required
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

@admin_login_required
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

@require_POST
def police_address_delete(request, pk):
    addr = get_object_or_404(PoliceAddress, pk=pk)
    addr.delete()
    return redirect('police_address_list')  # 刪除後回到列表頁

#用戶管理的東西
from django.db.models import Q
from .models import ThisUserProfile   # 假設你的 Model 名稱是 ThisUserProfile
from django.utils import timezone

# 使用者列表
@admin_login_required
def user_admin_list(request):
    users = ThisUserProfile.objects.all().order_by('id')
    return render(request, 'user_admin_list.html', {'users': users})

# 搜尋用戶
def user_admin_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = ThisUserProfile.objects.filter(
            Q(username__icontains=query) |
            Q(gmail__icontains=query) |
            Q(default_nickname1__icontains=query) |
            Q(default_nickname2__icontains=query)
        )
    return render(request, 'user_admin_list.html', {
        'users': results,
        'query': query,
    })

# 編輯用戶
@admin_login_required
def user_admin_edit(request, user_id):
    user = get_object_or_404(ThisUserProfile, id=user_id)

    if request.method == "POST":
        status_color = request.POST.get("status_color")
        user.status_color = status_color
        user.save()
        return redirect("user_admin_list")

    return render(request, "user_admin_edit.html", {"user": user})

# 刪除用戶
def user_admin_delete(request, user_id):
    user = get_object_or_404(ThisUserProfile, id=user_id)
    user.delete()
    return redirect('user_admin_list')


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




    
def room(request, room_name):
    return render(request, 'test_0610chatroom.html', {'room_name': room_name})
#report_list_view
from django.contrib.auth.decorators import login_required
@login_required(login_url='/01userlogin/')
def report_list_view(request):
    user_reports = list(PemapAll.objects.filter(user=request.user).order_by('-time_created'))
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
        # 'avatar_url': db_profile.user_images or extra_data.get('picture', None),
        'avatar_url': (db_profile.user_images if db_profile else None) or extra_data.get('picture', None),

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


from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import os
from .models import StoreAll, StoreAd, StoreAdImage

@login_required(login_url='/01userlogin/')
@csrf_exempt
def submit_store(request):
    if request.method == 'POST':
        try:
            # 取表單資料
            bs_name = request.POST.get('store_name')
            bs_address = request.POST.get('address')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            business_hours = request.POST.get('business_hours')
            phone = request.POST.get('phone')
            poster_id = int(request.POST.get('poster_id', 1))
            created_at = request.POST.get('created_at')
            ad_content = request.POST.get('ad_content', '')

            st_id = int(request.POST.get('st_id'))

            # 建立商家
            store = StoreAll.objects.create(
                user=request.user,
                st_id=str(st_id),
                poster_id=str(poster_id),
                store_name=bs_name,
                address=bs_address,
                latitude=float(latitude),
                longitude=float(longitude),
                business_hours=business_hours,
                phone=phone,
                created_at=created_at,
                reviewed_at=None,
                review_status="pending",
                admin_id=9999,
                poster_gmail=request.user.email,
            )

            # 建立廣告
            store_ad = StoreAd.objects.create(
                st_id=int(store.st_id),
                ad_content=ad_content,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

            # 處理多張圖片，上傳到 media/ads/
            images = request.FILES.getlist('ad_images')
            ad_folder = os.path.join(settings.MEDIA_ROOT, 'ads')
            os.makedirs(ad_folder, exist_ok=True)

            for img in images:
                # 保存檔案
                file_path = os.path.join(ad_folder, img.name)
                with open(file_path, 'wb+') as f:
                    for chunk in img.chunks():
                        f.write(chunk)
                # 存資料庫 URL
                image_url = f"{settings.MEDIA_URL}ads/{img.name}"
                StoreAdImage.objects.create(
                    st_id=store_ad.st_id,
                    image_url=image_url,
                    created_at=timezone.now()
                )

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})





from django.contrib.auth.decorators import login_required
@login_required(login_url='/01userlogin/')
def business_list_view(request):
    user_stores = list(StoreAll.objects.filter(user=request.user).order_by('-created_at'))
    total = len(user_stores)
    for i, store in enumerate(user_stores):
        store.reverse_id = total - i  # 編號從總數開始往下減
    return render(request, 'business_list.html', {'stores': user_stores})
#----------------聊天室-----------------------------
from django.shortcuts import render

def chatroom_map(request):
    return render(request, 'chatroom.html')  # HTML 檔名可自訂
#------------PWA-------------------------
from django.http import JsonResponse

def manifest(request):
    return JsonResponse({
        "name": "怪怪走開護您安全",
        "short_name": "護您安全",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#4a90e2",
        "icons": [
            {
                "src": "/static/icons/icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icons/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
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



import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ai_judge(request):
    if request.method != 'POST':
        return JsonResponse({'result': 0, 'reason': '請使用 POST 請求'})

    try:
        data = json.loads(request.body)
        description = data.get('description', '').strip()

        if not description:
            return JsonResponse({'result': 1, 'reason': '描述為空，請輸入內容'})

        if len(description) < 10:
            return JsonResponse({'result': 1, 'reason': '描述內容過短，請補充更多細節'})

        prompt = f"""
請判斷以下文字描述是否過於主觀，包含仇恨言論、恐懼煽動，或者不當內容？或是對案件描述太無關？
若沒有，請只回覆「通過」；若有問題，請說明理由。

文字描述：
{description}
"""

        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            return JsonResponse({'result': 0, 'reason': '未設定 GITHUB_TOKEN 環境變數'})

        url = "https://models.inference.ai.azure.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2023-07-01"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        reply = response.json()["choices"][0]["message"]["content"].strip()

        print("AI 回傳全文:", reply)  # <--- 這行會在伺服器終端或日誌中印出


        if "通過" in reply:
            return JsonResponse({'result': 0, 'reason': '描述符合規範，無需人工審核'})
        else:
            return JsonResponse({'result': 2, 'reason': reply})

    except Exception as e:
        return JsonResponse({'result': 0, 'reason': f"系統錯誤：{str(e)}"})


# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import json

# @csrf_exempt
# def ai_judge(request):
#     if request.method != 'POST':
#         return JsonResponse({'result': 2, 'reason': '請使用 POST 請求'})

#     try:
#         data = json.loads(request.body)
#         description = data.get('description', '').strip()

#         if not description or len(description) < 10:
#             return JsonResponse({'result': 1, 'reason': '描述內容過短，不足以判斷'})

#         # 敏感詞分類詞庫
#         sensitive_categories = {
#             '仇恨言論': ['仇恨', '恨死', '殺光', '滅絕'],
#             '暴力': ['暴力', '打死', '砍', '攻擊', '虐待'],
#             '歧視': ['歧視', '種族主義', '排擠', '偏見'],
#         }

#         # 檢查是否含敏感詞
#         has_sensitive_word = any(
#             keyword in description
#             for keywords in sensitive_categories.values()
#             for keyword in keywords
#         )

#         # 案件關聯詞彙
#         case_related_keywords = [
#             '案件', '事件', '警方', '警察', '報警', '報案', '證據',
#             '被跟蹤', '跟蹤', '尾隨', '偷拍', '性騷擾', '偷窺', '侵入',
#             '陌生男子', '紅衣男子', '追蹤', '恐嚇', '求助', '監視'
#         ]
#         is_case_related = any(kw in description for kw in case_related_keywords)

#         if has_sensitive_word or not is_case_related:
#             return JsonResponse({'result': 2, 'reason': '需再由人工審核'})

#         return JsonResponse({'result': 0, 'reason': '人工審核通過'})

#     except Exception as e:
#         return JsonResponse({'result': 2, 'reason': f'系統錯誤：{str(e)}'})





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
from django.db.models import Q
from .utils import get_unreviewed_counts   # 匯入共用函式

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

    context = {
        'form': form,
        'message': message,
        'admin_name': admin.name,
        'admin_id': admin.admin_id,
    }
    context.update(get_unreviewed_counts())  # 🔹 加入紅點數
    return render(request, 'admin_interview.html', context)

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
from .utils import get_unreviewed_counts

def pemap_judge(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')

    if not admin_id:
        return redirect('admin_login')  # 未登入導回登入頁

    all_data = PemapAll.objects.all().order_by('-time_created')  # 最新的在上

    context = {
        'data': all_data,
        'admin_id': admin_id,
        'admin_name': admin_name,
    }
    context.update(get_unreviewed_counts())
    return render(request, 'pemap_judge.html',context )



from django.shortcuts import render, redirect
from .models import StoreAll
from .utils import get_unreviewed_counts

def store_judge(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name')

    if not admin_id:
        return redirect('admin_login')  # 尚未登入，導向登入頁

    store_list = StoreAll.objects.all().order_by('-created_at')  # 最新在最上面

    context =  {
        'store_list': store_list,
        'admin_id': admin_id,
        'admin_name': admin_name,
    }
    context.update(get_unreviewed_counts())
    return render(request, 'store_judge.html',context)



#--step1

from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from .models import PemapAll

def pemap_judge_step1(request, p_id):
    form_data = get_object_or_404(PemapAll, p_id=p_id)

    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name', '未知管理員')

    if not admin_id:
        return redirect('admin_login')

    if request.method == 'POST':
        new_status = request.POST.get('review_status')
        if new_status:  # 直接存文字
            form_data.review_status = new_status
            form_data.time_reviewed = timezone.now()
            form_data.admin_id = admin_id  
            form_data.save()

            if new_status == "人工審核未通過":  # 用文字比對
                url = reverse('admin_send_email', kwargs={'p_id': p_id})
                return redirect(url)

            return redirect('pemap_judge')

    return render(request, 'pemap_judge_step1.html', {
        'item': form_data,
        'admin_id': admin_id,
        'admin_name': admin_name,
    })





from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import StoreAll

from .models import StoreAll, StoreAd

def store_judge_step1(request, st_id):
    store = get_object_or_404(StoreAll, st_id=st_id)

    # 抓對應的廣告（可能沒有廣告就 None）
    store_ad = StoreAd.objects.prefetch_related('images').filter(st_id=store.st_id).first()

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
            store.save()
            return redirect('store_judge')  # 審核完返回列表頁

    return render(request, 'store_judge_step1.html', {
        'store': store,
        'store_ad': store_ad,
        'admin_id': admin_id,
        'admin_name': admin_name,
    })



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
from django.shortcuts import render, redirect
from django.db.models import Q
from .utils import get_unreviewed_counts   # 匯入共用函式

def admin_index(request):
    if 'admin_id' not in request.session:
        return redirect('admin_login')

    context = {
        'admin_id': request.session.get('admin_id'),
        'admin_name': request.session.get('admin_name'),
    }
    context.update(get_unreviewed_counts())  # 🔹 加入紅點數
    return render(request, 'admin_index.html', context)


#---------------管理員註冊-----------------------
from django.shortcuts import render
from .models import Admins  # 根據你的 models 路徑
from django.contrib.auth.hashers import make_password

def admin_register(request):
    
    message = ""
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        admin_gmail = request.POST.get("admin_gmail")
        bio = request.POST.get("bio")
        security_code = request.POST.get("security_code")

        # 允許的安全碼清單
        valid_codes = ["12345654", "698417", "114502"]

        if security_code not in valid_codes:
            message = "安全碼錯誤,註冊失敗"
        else:
            # 檢查帳號是否已存在
            if Admins.objects.filter(admin_gmail=admin_gmail).exists():
                message = "此 Email 已存在"
            else:
                # 建立帳號
                Admins.objects.create(
                    name=name,
                    password=make_password(password),
                    phone=phone,
                    admin_gmail=admin_gmail,
                    bio=bio,
                )
                message = "註冊成功"

    return render(request, "admin_register.html", {"message": message})



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
def approved_locations_api(request):
    approved_p_ids = PemapAll.objects.filter(review_status='3').values_list('p_id', flat=True)
    approved = PemapWithSubkind.objects.filter(p_id__in=approved_p_ids)

    data = []
    for r in approved:
        try:
            pemap_detail = PemapAll.objects.get(p_id=r.p_id)
            reason = pemap_detail.reason or ""
            time_created = pemap_detail.time_created.strftime("%Y-%m-%d %H:%M")
        except PemapAll.DoesNotExist:
            reason = ""
            time_created = "未知"

        data.append({
            'id': r.p_id,
            'display_name': r.display_name,
            'kind': r.kind,
            'subkind': r.subkind,
            'reason': reason,
            'latitude': r.latitude,
            'longitude': r.longitude,
            'time_created': time_created,
            'img_url': r.img_url
        })

    return JsonResponse(data, safe=False)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import PemapWithSubkind, PemapAll


# 可以跑分類的,但是有億點久


from django.shortcuts import render
from datetime import datetime, date

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

# 可以跑分類的,但是有億點久
def reports_with_subkind_json(request):
    queryset = PemapAll.objects.filter(review_status='3').values(
        'p_id', 'display_name', 'kind', 'reason', 'address', 'latitude', 'longitude', 'img_url', 'time_created'
    )

    results = []
    for item in queryset:
        kind_str = item['kind'] or ""
        subkind = kind_str.split('-')[-1].strip() if '-' in kind_str else ""

        results.append({
            "p_id": item['p_id'],
            "display_name": item['display_name'],
            "kind": kind_str,
            "subkind": subkind,
            "latitude": item['latitude'],
            "longitude": item['longitude'],
            "address": item['address'],
            "img_url": item['img_url'],
            "time_created": item['time_created'].strftime("%Y-%m-%d %H:%M") if item['time_created'] else "未知",
            "reason": item['reason'] or "無",
        })

    return JsonResponse(results, safe=False)



    
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

# API：取得審核通過的商家資料（含廣告）
from django.conf import settings

def stores_with_ads_api(request):
    approved_stores = StoreAll.objects.filter(review_status='approved')

    data = []
    for store in approved_stores:
        try:
            ad = StoreAd.objects.get(st_id=store.st_id)
            images = []
            for img in ad.images.all():
                # 移除重複的 'media/'，只保留一個
                img_url = img.image_url.lstrip('/')
                if img_url.startswith('media/'):
                    full_url = request.build_absolute_uri('/' + img_url)
                else:
                    full_url = request.build_absolute_uri(settings.MEDIA_URL + img_url)
                images.append(full_url)
        except StoreAd.DoesNotExist:
            ad = None
            images = []

        data.append({
            'st_id': store.st_id,
            'store_name': store.store_name,
            'address': store.address,
            'phone': store.phone,
            'latitude': store.latitude,
            'longitude': store.longitude,
            'ad_content': ad.ad_content if ad else '',
            'ad_radius': 200,
            'images': images
        })

    return JsonResponse(data, safe=False)



# ------------ 交流區後端（整合版，支援巢狀回覆 / 巢狀按讚 / 回覆編輯刪除 / 留言編輯 by id或time）------------
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from .models import Notification

from .models import ChatInteraction, ThisUserProfile
import json
import bleach
from urllib.parse import quote
from uuid import uuid4
from functools import wraps

# 允許的貼文 HTML（內容/留言都會用 bleach 過濾）
ALLOWED_TAGS = ['a']
ALLOWED_ATTRIBUTES = {'a': ['href', 'target', 'rel']}

# ======== 工具：時間、載入/正規化、搜尋/計數 ========

def _now_str():
    return timezone.now().strftime("%Y-%m-%d %H:%M:%S")

def _get_post_by_any_id(post_id):
    """同時支援 pk 或 interaction_id（都以字串比對）。"""
    pid = str(post_id)
    post = ChatInteraction.objects.filter(Q(pk=pid) | Q(interaction_id=pid)).first()
    if not post:
        raise Http404("Post not found")
    return post

def _load_comments(post):
    """讀取並回傳 list（舊資料自動相容）。"""
    try:
        comments = json.loads(getattr(post, 'comments', '[]') or '[]')
    except json.JSONDecodeError:
        comments = []
    if not isinstance(comments, list):
        comments = []
    return comments

def _ensure_reply_defaults(r):
    """補齊回覆欄位，並對其子回覆遞迴正規化。"""
    r.setdefault('id', r.get('time') or str(uuid4()))
    r.setdefault('identity', 'anonymous')
    r.setdefault('nickname', r.get('nickname') or "(匿名)")
    r.setdefault('content', r.get('content', ''))
    r.setdefault('time', r.get('time') or _now_str())
    r.setdefault('user_id', r.get('user_id'))
    r.setdefault('like_user_ids', [])
    r['like_user_ids'] = [str(x) for x in (r.get('like_user_ids') or [])]
    r['like_count'] = len(r['like_user_ids'])

    replies = r.get('replies') or []
    if not isinstance(replies, list):
        replies = []
    fixed = []
    for rr in replies:
        fixed.append(_ensure_reply_defaults(rr))
    r['replies'] = fixed
    return r

def _ensure_comment_defaults(c):
    """補齊單一留言的欄位，並遞迴正規化其所有回覆。"""
    c.setdefault('id', c.get('time') or str(uuid4()))
    c.setdefault('identity', 'anonymous')
    c.setdefault('nickname', c.get('nickname') or "(匿名)")
    c.setdefault('content', c.get('content', ''))
    c.setdefault('time', c.get('time') or _now_str())
    c.setdefault('user_id', c.get('user_id'))
    c.setdefault('like_user_ids', [])
    c['like_user_ids'] = [str(x) for x in (c.get('like_user_ids') or [])]
    c['like_count'] = len(c['like_user_ids'])

    replies = c.get('replies') or []
    if not isinstance(replies, list):
        replies = []
    fixed = []
    for r in replies:
        fixed.append(_ensure_reply_defaults(r))
    c['replies'] = fixed
    return c

def _find_comment(comments, comment_id_or_time):
    """依 id 或 time 找到留言 dict 與其索引。"""
    key = str(comment_id_or_time)
    for idx, c in enumerate(comments):
        cid = str(c.get('id') or c.get('time'))
        if cid == key or str(c.get('time')) == key:
            return idx, c
    return None, None

def _find_reply_recursive(replies, reply_id_or_time):
    """
    在任意深度的 replies（list）遞迴尋找指定回覆。
    回傳：(parent_list, index, reply_dict)；parent_list 是包含該回覆的 list 物件。
    找不到則回傳 (None, None, None)。
    """
    if not isinstance(replies, list):
        return (None, None, None)
    target_key = str(reply_id_or_time)
    for i, r in enumerate(replies):
        rid = str(r.get('id') or r.get('time'))
        if rid == target_key:
            return (replies, i, r)
        parent, idx, rr = _find_reply_recursive(r.get('replies') or [], target_key)
        if rr is not None:
            return (parent, idx, rr)
    return (None, None, None)

def _mark_is_liked_recursive(replies, user_id_str):
    """把 is_liked 旗標遞迴標在每一層回覆上，供初始渲染。"""
    if not isinstance(replies, list):
        return
    for r in replies:
        like_ids = [str(x) for x in (r.get('like_user_ids') or [])]
        r['is_liked'] = bool(user_id_str and (user_id_str in like_ids))
        _mark_is_liked_recursive(r.get('replies') or [], user_id_str)

def _flatten_replies(replies, level=1):
    """舊：展平成簡易清單（保留以供其他頁使用）。"""
    flat = []
    if not isinstance(replies, list):
        return flat
    for r in replies:
        r = _ensure_reply_defaults(r)
        item = {
            'id': str(r.get('id') or r.get('time')),
            'time': r.get('time'),
            'content': r.get('content', ''),
            'identity': r.get('identity', 'anonymous'),
            'nickname': r.get('nickname') or '(匿名)',
            'user_id': r.get('user_id'),
            'is_liked': r.get('is_liked', False),
            'like_count': len(r.get('like_user_ids') or []),
            'level': level,
        }
        flat.append(item)
        flat.extend(_flatten_replies(r.get('replies') or [], level + 1))
    return flat

# ===== 計數 =====
def _count_replies_recursive(replies):
    total = 0
    if not isinstance(replies, list):
        return 0
    for r in replies:
        r = _ensure_reply_defaults(r)
        total += 1
        total += _count_replies_recursive(r.get('replies') or [])
    return total

def _count_totals(comments):
    """回傳 (top_count, all_count)"""
    top = len(comments or [])
    all_total = top
    for c in (comments or []):
        c = _ensure_comment_defaults(c)
        all_total += _count_replies_recursive(c.get('replies') or [])
    return top, all_total

# ===== 全部留言（含回覆）扁平化，附上「回覆對象」資訊 + 喜歡狀態 =====
def _flatten_all_with_parent(comments, user_id_str=None, indent_step_px=20):
    """
    把所有留言與回覆展平成清單，並帶上：
    - kind: 'comment' / 'reply'
    - id / root_comment_id
    - content / time / nickname / identity / user_id
    - indent_px / level
    - parent_*（如果是回覆）
    - like_count / is_liked（這兩個是本頁渲染需要的）
    """
    items = []

    def _preview(text, length=30):
        text = (text or '')
        return text if len(text) <= length else text[:length] + '…'

    uid = str(user_id_str) if user_id_str else None

    for c in comments or []:
        c = _ensure_comment_defaults(c)
        root_id = str(c.get('id') or c.get('time'))

        # 頂層留言
        c_like_ids = [str(x) for x in (c.get('like_user_ids') or [])]
        items.append({
            'kind': 'comment',
            'id': root_id,
            'root_comment_id': root_id,
            'time': c['time'],
            'content': c['content'],
            'identity': c['identity'],
            'nickname': c.get('nickname') or '(匿名)',
            'user_id': c.get('user_id'),
            'level': 0,
            'indent_px': 0,
            'parent_id': None,
            'parent_time': None,
            'parent_nickname': None,
            'parent_preview': None,
            'like_count': len(c_like_ids),
            'is_liked': bool(uid and uid in c_like_ids),
        })

        # 巢狀回覆遞迴
        def walk(replies, parent_obj, parent_level):
            for r in (replies or []):
                r = _ensure_reply_defaults(r)
                rid = str(r.get('id') or r.get('time'))

                r_like_ids = [str(x) for x in (r.get('like_user_ids') or [])]
                parent_id = str(parent_obj.get('id') or parent_obj.get('time'))
                parent_nick = parent_obj.get('nickname') or '(匿名)'
                parent_time = parent_obj.get('time')
                parent_preview = _preview(parent_obj.get('content'))

                level = parent_level + 1
                items.append({
                    'kind': 'reply',
                    'id': rid,
                    'root_comment_id': root_id,
                    'time': r['time'],
                    'content': r['content'],
                    'identity': r['identity'],
                    'nickname': r.get('nickname') or '(匿名)',
                    'user_id': r.get('user_id'),
                    'level': level,
                    'indent_px': level * indent_step_px,
                    'parent_id': parent_id,
                    'parent_time': parent_time,
                    'parent_nickname': parent_nick,
                    'parent_preview': parent_preview,
                    'like_count': len(r_like_ids),
                    'is_liked': bool(uid and uid in r_like_ids),
                })
                walk(r.get('replies') or [], r, level)

        walk(c.get('replies') or [], c, 0)

    return items

# ================== 通知功能 ==================

@login_required(login_url='/01userlogin/')
def notif_dropdown(request):
    """回傳使用者最近 10 則通知"""
    notifs = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')[:10]

    data = [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "link_url": n.link_url,
            "is_read": n.is_read,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for n in notifs
    ]

    return JsonResponse({"notifications": data})

# ================== 貼文 CRUD / 展示 ==================

@login_required(login_url='/01userlogin/')
def post(request):
    prof = ThisUserProfile.objects.filter(gmail=request.user.email).first()
    # --- 後備查法：維持原邏輯，僅在找不到時補救 ---
    if not prof and request.user.is_authenticated:
        prof = ThisUserProfile.objects.filter(user=request.user).first() \
               or ThisUserProfile.objects.filter(gmail__iexact=(request.user.email or "")).first()
    nick1 = (prof.default_nickname1 or "").strip() if prof else ""
    nick2 = (prof.default_nickname2 or "").strip() if prof else ""

    if request.method == 'POST':
        identity = request.POST.get('post_identity', 'anonymous')
        if identity == 'nickname1' and nick1:
            nickname = nick1
        elif identity == 'nickname2' and nick2:
            nickname = nick2
        else:
            nickname = "(匿名)"

        bgcolor = request.POST.get('bgcolor')
        avatar_style = request.POST.get('avatar_style')
        title = request.POST.get('title') or ""
        raw_content = request.POST.get('content') or ""

        clean_content = bleach.clean(
            raw_content,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=['http', 'https'],
            strip=True
        )

        seed = quote(nickname)
        avatar_url = f"https://api.dicebear.com/7.x/{avatar_style}/svg?seed={seed}&backgroundColor={bgcolor}"

        ChatInteraction.objects.create(
            user=request.user,
            nickname=nickname,
            bgcolor=bgcolor,
            avatar_style=avatar_style,
            avatar_url=avatar_url,
            title=title,
            message_content=clean_content,
            like_heart_count=0,
            liked_user_ids='[]',
            saved_user_ids='[]',
            comments='[]',
            created_at=timezone.now()
        )
        return redirect('post_display')

    return render(request, 'post.html', {
        'profile_nickname1': nick1,
        'profile_nickname2': nick2,
    })

def post_display(request):
    # 🔸 保守引入 AbuseReport（若沒定義就忽略）
    try:
        from .models import AbuseReport as _AbuseReport
    except Exception:
        _AbuseReport = None

    query = (request.GET.get('q') or '').strip()
    sort = request.GET.get('sort', 'desc')
    order_expr = 'created_at' if sort == 'asc' else '-created_at'

    all_posts_qs = ChatInteraction.objects.all().order_by('-created_at')

    base_qs = ChatInteraction.objects.all()
    if query:
        base_qs = base_qs.filter(
            Q(title__icontains=query) | Q(message_content__icontains=query) | Q(nickname__icontains=query)
        )
    posts = base_qs.order_by(order_expr)

    user_id_str = str(request.user.id) if request.user.is_authenticated else None

    # 🔸 此使用者被駁回過的檢舉目標 key set（target_type, post_id, comment_id, reply_id）
    rejected_keys = set()
    if request.user.is_authenticated and _AbuseReport is not None:
        qs = _AbuseReport.objects.filter(
            reporter=request.user,
            status='rejected'
        ).values('target_type', 'post_id', 'comment_id', 'reply_id')
        for r in qs:
            rejected_keys.add((
                r['target_type'],
                r['post_id'],
                (r['comment_id'] or ''),
                (r['reply_id'] or ''),
            ))

    for post in posts:
        # liked
        try:
            liked_user_ids = json.loads(post.liked_user_ids or '[]')
        except json.JSONDecodeError:
            liked_user_ids = []
        liked_user_ids = [str(x) for x in liked_user_ids]
        post.is_liked = bool(user_id_str and (user_id_str in liked_user_ids))
        post.liked_user_list = liked_user_ids

        # saved
        try:
            saved_user_ids = json.loads(getattr(post, 'saved_user_ids', '[]') or '[]')
        except json.JSONDecodeError:
            saved_user_ids = []
        saved_user_ids = [str(x) for x in saved_user_ids]
        post.is_saved = bool(user_id_str and (user_id_str in saved_user_ids))
        post.saved_user_list = saved_user_ids

        # comments（同時標記「被駁回過→不可再檢舉」的旗標）
        comments = _load_comments(post)
        fixed_comments = []

        for c in comments:
            c = _ensure_comment_defaults(c)

            # is_liked
            c['is_liked'] = bool(user_id_str and (str(user_id_str) in c['like_user_ids']))

            # 標記留言是否已被駁回過（此使用者對此留言的檢舉）
            cid = str(c.get('id') or c.get('time'))
            key_comment = ('comment', getattr(post, 'interaction_id', None), cid, '')
            c['user_rejected_report'] = key_comment in rejected_keys

            # 遞迴標記所有回覆是否已被駁回過，並補 is_liked
            def mark_rejected_on_replies(replies, root_comment_id):
                if not isinstance(replies, list):
                    return []
                out = []
                for r in replies:
                    r = _ensure_reply_defaults(r)
                    rid = str(r.get('id') or r.get('time'))
                    key_reply = ('reply', getattr(post, 'interaction_id', None), root_comment_id, rid)
                    r['user_rejected_report'] = key_reply in rejected_keys

                    like_ids = [str(x) for x in (r.get('like_user_ids') or [])]
                    r['is_liked'] = bool(user_id_str and (user_id_str in like_ids))

                    r['replies'] = mark_rejected_on_replies(r.get('replies') or [], root_comment_id)
                    out.append(r)
                return out

            c['replies'] = mark_rejected_on_replies(c.get('replies') or [], cid)

            # 舊 UI 需要的平面 replies_flat
            _mark_is_liked_recursive(c.get('replies') or [], user_id_str)
            c['replies_flat'] = _flatten_replies(c.get('replies') or [], 1)

            fixed_comments.append(c)

        post.comment_list = fixed_comments
        post.top_comment_count = len(fixed_comments)
        post.total_comment_count = sum(1 + len(c.get('replies_flat', [])) for c in fixed_comments)

        # 🔸 這篇貼文是否被此使用者檢舉且已駁回（用於前端關閉檢舉鈕）
        key_post = ('post', getattr(post, 'interaction_id', None), '', '')
        post.user_rejected_report = key_post in rejected_keys

    my_saved_posts = []
    my_liked_posts = []
    my_commented_posts = []
    my_posts = []
    commented_total_count = 0

    if request.user.is_authenticated:
        for p in all_posts_qs:
            try:
                liked_user_ids_all = json.loads(p.liked_user_ids or '[]')
            except json.JSONDecodeError:
                liked_user_ids_all = []
            liked_user_ids_all = [str(x) for x in liked_user_ids_all]

            try:
                saved_user_ids_all = json.loads(getattr(p, 'saved_user_ids', '[]') or '[]')
            except json.JSONDecodeError:
                saved_user_ids_all = []
            saved_user_ids_all = [str(x) for x in saved_user_ids_all]

            c_all = _load_comments(p)

            if str(p.user_id) == (user_id_str or ''):
                my_posts.append(p)
            if (user_id_str or '') in saved_user_ids_all:
                my_saved_posts.append(p)
            if (user_id_str or '') in liked_user_ids_all:
                my_liked_posts.append(p)

            my_comments_num = sum(1 for c in c_all if str(c.get('user_id')) == (user_id_str or ''))
            if my_comments_num > 0:
                p.comment_list = c_all
                my_commented_posts.append(p)
                commented_total_count += my_comments_num

    nick1 = ""
    nick2 = ""
    if request.user.is_authenticated:
        prof = ThisUserProfile.objects.filter(gmail=request.user.email).first()
        # 後備查法（只在找不到時使用；不影響原有邏輯）
        if not prof:
            prof = ThisUserProfile.objects.filter(user=request.user).first() \
                   or ThisUserProfile.objects.filter(gmail__iexact=(request.user.email or "")).first()
        nick1 = (prof.default_nickname1 or "").strip() if prof else ""
        nick2 = (prof.default_nickname2 or "").strip() if prof else ""

    context = {
        'posts': posts,
        'profile_nickname1': nick1,
        'profile_nickname2': nick2,
    }
    if request.user.is_authenticated:
        context.update({
            'my_saved_posts': my_saved_posts,
            'my_liked_posts': my_liked_posts,
            'my_commented_posts': my_commented_posts,
            'my_posts': my_posts,
            'commented_total_count': commented_total_count,
            'uid': user_id_str,
        })

    return render(request, 'post_display.html', context)

@login_required(login_url='/01userlogin/')
def edit_post(request, post_id):
    post = _get_post_by_any_id(post_id)
    if post.user_id != request.user.id:
        return HttpResponseForbidden("⚠️ 你無權編輯這篇貼文。")

    if request.method == 'POST':
        post.title = request.POST.get('title') or ""
        post.message_content = request.POST.get('content') or ""
        post.created_at = timezone.now()
        post.save(update_fields=['title', 'message_content', 'created_at'])
        return redirect('post_display')

    return render(request, 'edit_post.html', {'post': post})

@login_required(login_url='/01userlogin/')
def delete_post(request, post_id):
    post = _get_post_by_any_id(post_id)
    if post.user_id != request.user.id:
        return HttpResponseForbidden("⚠️ 你無權刪除這篇貼文。")

    if request.method == 'POST':
        post.delete()
        return redirect('post_display')

    return render(request, 'delete_post_confirm.html', {'post': post})

@require_POST
@login_required(login_url='/01userlogin/')
def like_post(request, post_id):
    post = _get_post_by_any_id(post_id)
    user_id_str = str(request.user.id)

    try:
        liked_user_ids = json.loads(post.liked_user_ids or '[]')
    except json.JSONDecodeError:
        liked_user_ids = []

    liked_user_ids = list({str(x) for x in liked_user_ids})

    if user_id_str in liked_user_ids:
        liked_user_ids.remove(user_id_str)
    else:
        liked_user_ids.append(user_id_str)

    post.like_heart_count = len(liked_user_ids)
    post.liked_user_ids = json.dumps(liked_user_ids, ensure_ascii=False)
    post.save(update_fields=['like_heart_count', 'liked_user_ids'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': user_id_str in liked_user_ids, 'count': post.like_heart_count})
    return redirect('post_display')

@require_POST
@login_required(login_url='/01userlogin/')
def save_post(request, post_id):
    post = _get_post_by_any_id(post_id)
    user_id_str = str(request.user.id)

    try:
        saved_user_ids = json.loads(getattr(post, 'saved_user_ids', '[]') or '[]')
    except json.JSONDecodeError:
        saved_user_ids = []

    saved_user_ids = list({str(x) for x in saved_user_ids})

    if user_id_str in saved_user_ids:
        saved_user_ids.remove(user_id_str)
        saved_state = False
    else:
        saved_user_ids.append(user_id_str)
        saved_state = True

    post.saved_user_ids = json.dumps(saved_user_ids, ensure_ascii=False)
    post.save(update_fields=['saved_user_ids'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'saved': saved_state})
    return redirect('post_display')

@require_POST
@login_required(login_url='/01userlogin/')
def add_comment(request, post_id):
    post = _get_post_by_any_id(post_id)
    comment_text = (request.POST.get('comment') or '').strip()
    user_id_str = str(request.user.id)

    if not comment_text:
        return JsonResponse({'error': '留言不能為空'}, status=400)

    safe_text = bleach.clean(comment_text, tags=[], attributes={}, strip=True)
    if len(safe_text) > 300:
        return JsonResponse({'error': '留言超過 300 字上限'}, status=400)

    prof = ThisUserProfile.objects.filter(gmail=request.user.email).first()
    if not prof:
        prof = ThisUserProfile.objects.filter(user=request.user).first() \
               or ThisUserProfile.objects.filter(gmail__iexact=(request.user.email or "")).first()
    nick1 = (prof.default_nickname1 or "").strip() if prof else ""
    nick2 = (prof.default_nickname2 or "").strip() if prof else ""

    identity = request.POST.get('comment_identity', 'anonymous')
    if identity == 'nickname1' and nick1:
        nickname = nick1
    elif identity == 'nickname2' and nick2:
        nickname = nick2
    else:
        nickname = "(匿名)"

    comments = _load_comments(post)

    comment_time = _now_str()
    comment_id = str(uuid4())
    comments.append({
        'id': comment_id,
        'user_id': user_id_str,
        'identity': identity,
        'nickname': nickname,
        'content': safe_text,
        'time': comment_time,
        'like_user_ids': [],
        'replies': []
    })

    post.comments = json.dumps(comments, ensure_ascii=False)
    post.save(update_fields=['comments'])

    top_count, all_count = _count_totals(comments)

    return JsonResponse({
        'success': True,
        'comments': comments,
        'total_comments': top_count,
        'total_including_replies': all_count
    })

@require_POST
@login_required(login_url='/01userlogin/')
def delete_comment(request, post_id):
    post = _get_post_by_any_id(post_id)
    comment_time = (request.POST.get('time') or '').strip()
    user_id_str = str(request.user.id)

    if not comment_time:
        return JsonResponse({'error': '缺少留言時間'}, status=400)

    comments = _load_comments(post)

    target = next((c for c in comments if c.get('time') == comment_time and str(c.get('user_id')) == user_id_str), None)
    if not target:
        return JsonResponse({'error': '留言不存在或你無權刪除'}, status=404)

    comments = [c for c in comments if not (c.get('time') == comment_time and str(c.get('user_id')) == user_id_str)]
    post.comments = json.dumps(comments, ensure_ascii=False)
    post.save(update_fields=['comments'])

    top_count, all_count = _count_totals(comments)

    return JsonResponse({
        'success': True,
        'comments': comments,
        'total_comments': top_count,
        'total_including_replies': all_count
    })

# ★★★ 留言編輯（支援 id 或 time；JSON 或表單皆可）★★★
@require_POST
@login_required(login_url='/01userlogin/')
def edit_comment(request, post_id, key):
    """
    URL: /edit_comment/<post_id>/<key>/
    - key 可放 comment 的 id（推薦）或舊的 time。
    - Body 可為 JSON: {"content": "..."}，或 x-www-form-urlencoded: content=...
      （若同時傳 comment_id 或 time 也可，但以 URL 的 key 優先）
    """
    post = _get_post_by_any_id(post_id)

    # 讀 body（支援 JSON 或表單）
    if request.content_type and 'application/json' in request.content_type:
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "不合法的內容"}, status=400)
        new_content = (payload.get("content") or "").strip()
    else:
        new_content = (request.POST.get("content") or "").strip()

    if not new_content:
        return JsonResponse({"success": False, "error": "內容不能為空"}, status=400)

    safe_text = bleach.clean(new_content, tags=[], attributes={}, strip=True)
    if len(safe_text) > 300:
        return JsonResponse({"success": False, "error": "留言超過 300 字上限"}, status=400)

    comments = _load_comments(post)
    user_id_str = str(request.user.id)

    # 依 key（id 或 time）找目標留言
    c_idx, c = _find_comment(comments, key)
    if c is None:
        return JsonResponse({"success": False, "error": "找不到這則留言"}, status=404)
    if str(c.get("user_id")) != user_id_str:
        return JsonResponse({"success": False, "error": "沒有權限編輯這則留言"}, status=403)

    c["content"] = safe_text
    c["edited_at"] = _now_str()
    comments[c_idx] = c
    post.comments = json.dumps(comments, ensure_ascii=False)
    post.save(update_fields=['comments'])
    return JsonResponse({"success": True, "comment": c})

# 🧵 查看全部留言（分頁；這裡改為：頂層 + 所有回覆都列出）
def post_comments(request, post_id):
    post = _get_post_by_any_id(post_id)

    comments = _load_comments(post)
    top_count, all_count = _count_totals(comments)

    user_id_str = str(request.user.id) if request.user.is_authenticated else None

    # 扁平化（帶 parent / like 狀態）
    flat_items = _flatten_all_with_parent(comments, user_id_str=user_id_str, indent_step_px=20)
    final_total = len(flat_items)

    paginator = Paginator(flat_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ★ 加：把暱稱帶給模板（與 post_display 同步）
    nick1 = ""
    nick2 = ""
    if request.user.is_authenticated:
        prof = ThisUserProfile.objects.filter(gmail=request.user.email).first() or \
               ThisUserProfile.objects.filter(user=request.user).first() or \
               ThisUserProfile.objects.filter(gmail__iexact=request.user.email).first()
        if prof:
            nick1 = (prof.default_nickname1 or "").strip()
            nick2 = (prof.default_nickname2 or "").strip()

    return render(request, 'post_comments.html', {
        'post': post,
        'page_obj': page_obj,
        'total_comments': top_count,
        'total_including_replies': all_count,
        'final_total': final_total,
        'profile_nickname1': nick1,          # ← 新增
        'profile_nickname2': nick2,          # ← 新增
    })


# ============== 巢狀：回覆 & 按讚 & 編輯/刪除 ==============

@require_POST
@login_required(login_url='/01userlogin/')
def reply_comment(request, post_id):
    """
    參數：
      - comment_id: 目標留言 id（或 time）
      - parent_reply_id: 選填；若填，表示「回覆某一則回覆」
      - reply_identity: nickname1 / nickname2 / anonymous
      - reply: 文字內容（<=300）
    """
    post = _get_post_by_any_id(post_id)
    comment_id = (request.POST.get('comment_id') or '').strip()
    parent_reply_id = (request.POST.get('parent_reply_id') or '').strip()
    reply_text = (request.POST.get('reply') or '').strip()
    identity = (request.POST.get('reply_identity') or 'anonymous').strip()
    user_id_str = str(request.user.id)

    if not comment_id:
        return JsonResponse({'success': False, 'error': '缺少 comment_id'}, status=400)
    if not reply_text:
        return JsonResponse({'success': False, 'error': '回覆不能為空'}, status=400)

    safe_text = bleach.clean(reply_text, tags=[], attributes={}, strip=True)
    if len(safe_text) > 300:
        return JsonResponse({'success': False, 'error': '回覆超過 300 字上限'}, status=400)

    prof = ThisUserProfile.objects.filter(gmail=request.user.email).first()
    if not prof:
        prof = ThisUserProfile.objects.filter(user=request.user).first() \
               or ThisUserProfile.objects.filter(gmail__iexact=(request.user.email or "")).first()
    nick1 = (prof.default_nickname1 or "").strip() if prof else ""
    nick2 = (prof.default_nickname2 or "").strip() if prof else ""

    if identity == 'nickname1' and nick1:
        nickname = nick1
    elif identity == 'nickname2' and nick2:
        nickname = nick2
    else:
        nickname = "(匿名)"
        identity = 'anonymous'

    comments = _load_comments(post)
    c_idx, c = _find_comment(comments, comment_id)
    if c is None:
        return JsonResponse({'success': False, 'error': '找不到目標留言'}, status=404)
    c = _ensure_comment_defaults(c)

    reply_dict = {
        'id': str(uuid4()),
        'user_id': user_id_str,
        'identity': identity,
        'nickname': nickname,
        'content': safe_text,
        'time': _now_str(),
        'like_user_ids': [],
        'replies': []
    }

    if parent_reply_id:
        parent_list, idx, target_r = _find_reply_recursive(c.get('replies') or [], parent_reply_id)
        if target_r is None:
            return JsonResponse({'success': False, 'error': '找不到目標回覆'}, status=404)
        target_r = _ensure_reply_defaults(target_r)
        target_r['replies'] = (target_r.get('replies') or [])
        target_r['replies'].append(reply_dict)
        parent_list[idx] = target_r
    else:
        c['replies'] = (c.get('replies') or [])
        c['replies'].append(reply_dict)

    comments[c_idx] = c
    post.comments = json.dumps(comments, ensure_ascii=False)
    post.save(update_fields=['comments'])

    top_count, all_count = _count_totals(comments)

    reply_out = _ensure_reply_defaults(reply_dict)
    return JsonResponse({
        'success': True,
        'reply': reply_out,
        'total_comments': top_count,
        'total_including_replies': all_count
    })

@require_POST
@login_required(login_url='/01userlogin/')
def like_comment(request, post_id):
    post = _get_post_by_any_id(post_id)
    comment_id = (request.POST.get('comment_id') or '').strip()
    reply_id = (request.POST.get('reply_id') or '').strip()
    user_id_str = str(request.user.id)

    if not comment_id:
        return JsonResponse({'success': False, 'error': '缺少 comment_id'}, status=400)

    comments = _load_comments(post)
    c_idx, c = _find_comment(comments, comment_id)
    if c is None:
        return JsonResponse({'success': False, 'error': '找不到目標留言'}, status=404)
    c = _ensure_comment_defaults(c)

    if reply_id:
        parent_list, r_idx, r = _find_reply_recursive(c.get('replies') or [], reply_id)
        if r is None:
            return JsonResponse({'success': False, 'error': '找不到目標回覆'}, status=404)
        r = _ensure_reply_defaults(r)

        likers = set(str(x) for x in (r.get('like_user_ids') or []))
        if user_id_str in likers:
            likers.remove(user_id_str)
            liked = False
        else:
            likers.add(user_id_str)
            liked = True
        r['like_user_ids'] = list(likers)
        r['like_count'] = len(likers)

        parent_list[r_idx] = r
        comments[c_idx] = c
        post.comments = json.dumps(comments, ensure_ascii=False)
        post.save(update_fields=['comments'])
        return JsonResponse({'success': True, 'liked': liked, 'like_count': r['like_count']})

    likers = set(str(x) for x in (c.get('like_user_ids') or []))
    if user_id_str in likers:
        likers.remove(user_id_str)
        liked = False
    else:
        likers.add(user_id_str)
        liked = True
    c['like_user_ids'] = list(likers)
    c['like_count'] = len(likers)

    comments[c_idx] = c
    post.comments = json.dumps(comments, ensure_ascii=False)
    post.save(update_fields=['comments'])
    return JsonResponse({'success': True, 'liked': liked, 'like_count': c['like_count']})

@require_POST
@login_required(login_url='/01userlogin/')
def edit_reply(request, post_id):
    post = _get_post_by_any_id(post_id)

    if request.content_type and 'application/json' in request.content_type:
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': '不合法的內容'}, status=400)
        comment_id = (payload.get('comment_id') or '').strip()
        reply_id   = (payload.get('reply_id') or '').strip()
        new_content = (payload.get('content') or '').strip()
    else:
        comment_id = (request.POST.get('comment_id') or '').strip()
        reply_id   = (request.POST.get('reply_id') or '').strip()
        new_content = (request.POST.get('content') or '').strip()

    if not comment_id or not reply_id:
        return JsonResponse({'success': False, 'error': '缺少 comment_id 或 reply_id'}, status=400)
    if not new_content:
        return JsonResponse({'success': False, 'error': '內容不能為空'}, status=400)

    safe_text = bleach.clean(new_content, tags=[], attributes={}, strip=True)
    if len(safe_text) > 300:
        return JsonResponse({'success': False, 'error': '內容超過 300 字上限'}, status=400)

    comments = _load_comments(post)
    c_idx, c = _find_comment(comments, comment_id)
    if c is None:
        return JsonResponse({'success': False, 'error': '找不到目標留言'}, status=404)
    c = _ensure_comment_defaults(c)

    parent_list, r_idx, r = _find_reply_recursive(c.get('replies') or [], reply_id)
    if r is None:
        return JsonResponse({'success': False, 'error': '找不到目標回覆'}, status=404)
    if str(r.get('user_id')) != str(request.user.id):
        return JsonResponse({'success': False, 'error': '沒有權限編輯這則回覆'}, status=403)

    r['content'] = safe_text
    r['edited_at'] = _now_str()
    parent_list[r_idx] = r
    comments[c_idx] = c
    post.comments = json.dumps(comments, ensure_ascii=False)
    post.save(update_fields=['comments'])

    return JsonResponse({'success': True, 'reply': _ensure_reply_defaults(r)})

@require_POST
@login_required(login_url='/01userlogin/')
def delete_reply(request, post_id):
    post = _get_post_by_any_id(post_id)
    comment_id = (request.POST.get('comment_id') or '').strip()
    reply_id   = (request.POST.get('reply_id') or '').strip()
    if not comment_id or not reply_id:
        return JsonResponse({'success': False, 'error': '缺少 comment_id 或 reply_id'}, status=400)

    comments = _load_comments(post)
    c_idx, c = _find_comment(comments, comment_id)
    if c is None:
        return JsonResponse({'success': False, 'error': '找不到目標留言'}, status=404)
    c = _ensure_comment_defaults(c)

    parent_list, r_idx, r = _find_reply_recursive(c.get('replies') or [], reply_id)
    if r is None:
        return JsonResponse({'success': False, 'error': '找不到目標回覆'}, status=404)
    if str(r.get('user_id')) != str(request.user.id):
        return JsonResponse({'success': False, 'error': '沒有權限刪除這則回覆'}, status=403)

    try:
        del parent_list[r_idx]
    except Exception:
        return JsonResponse({'success': False, 'error': '刪除失敗'}, status=500)

    comments[c_idx] = c
    post.comments = json.dumps(comments, ensure_ascii=False)
    post.save(update_fields=['comments'])

    top_count, all_count = _count_totals(comments)

    return JsonResponse({
        'success': True,
        'total_comments': top_count,
        'total_including_replies': all_count
    })


# ====== 管理員登入保護（沿用你的 session 機制）=========================
from functools import wraps
from urllib.parse import quote

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse, Http404
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
import json, bleach

# 你的模型
try:
    from .models import AbuseReport, Admins
except Exception:
    AbuseReport = None
    Admins = None

# ===== 你專案原有的工具函式（請確保存在；名稱不同就自己對應） =====
# _get_post_by_any_id(post_id)
# _load_comments(post)
# _find_comment(comments, comment_id)
# _find_reply_recursive(replies, reply_id)

def admin_login_required(view_func):
    """以 session['admin_id'] 判斷是否已登入管理員；未登入導至 admin_login。"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('admin_id'):
            return view_func(request, *args, **kwargs)
        login_url = reverse('admin_login')
        next_url = request.get_full_path()  # e.g. /reports/?status=pending
        return redirect(f"{login_url}?next={quote(next_url)}")
    return wrapper


# ===== 內部：產生被檢舉目標快照 =====
def _snapshot_for_target(post, target_type, comment_id='', reply_id=''):
    """回傳目標內容的文字快照，用於審核時避免內容後改找不到。"""
    if target_type == 'post':
        title = getattr(post, 'title', '') or ''
        content = getattr(post, 'message_content', '') or ''
        return f"[{title}]\n{content}".strip()

    comments = _load_comments(post)
    _, c = _find_comment(comments, comment_id)
    if not c:
        return None

    if target_type == 'comment':
        return str(c.get('content', ''))

    _, _, r = _find_reply_recursive(c.get('replies') or [], reply_id)
    return str(r.get('content', '')) if r else None


# ===== 前台送檢舉（需一般使用者登入） =====
@require_POST
def create_report(request):
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return JsonResponse({'ok': False, 'msg': '請先登入才能檢舉'}, status=403)

    if AbuseReport is None:
        return JsonResponse({'ok': False, 'msg': '尚未建立 AbuseReport 模型'}, status=501)

    # 解析 JSON
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'ok': False, 'msg': '格式錯誤（需為 JSON）'}, status=400)

    target_type = (data.get('target_type') or '').strip()
    if target_type not in ('post', 'comment', 'reply'):
        return JsonResponse({'ok': False, 'msg': '不支援的檢舉類型'}, status=400)

    post_id     = (data.get('post_id') or '').strip()
    comment_id  = (data.get('comment_id') or '').strip()
    reply_id    = (data.get('reply_id') or '').strip()
    reason      = (data.get('reason') or 'other').strip()
    details_raw = (data.get('details') or '').strip()

    if not post_id:
        return JsonResponse({'ok': False, 'msg': '缺少 post_id'}, status=400)
    if target_type == 'comment' and not comment_id:
        return JsonResponse({'ok': False, 'msg': '檢舉留言需提供 comment_id'}, status=400)
    if target_type == 'reply' and (not comment_id or not reply_id):
        return JsonResponse({'ok': False, 'msg': '檢舉回覆需提供 comment_id 與 reply_id'}, status=400)

    # 取得貼文
    try:
        post = _get_post_by_any_id(post_id)
    except Http404:
        return JsonResponse({'ok': False, 'msg': '找不到貼文'}, status=404)

    # 產生快照
    snapshot_text = _snapshot_for_target(post, target_type, comment_id, reply_id)
    if snapshot_text is None:
        return JsonResponse({'ok': False, 'msg': '找不到被檢舉的目標內容'}, status=404)

    # 🚫 禁止同一使用者對同一目標在「已駁回」後重複檢舉
    already_rejected = AbuseReport.objects.filter(
        reporter=request.user,
        target_type=target_type,
        post=post,
        comment_id=str(comment_id or ''),
        reply_id=str(reply_id or ''),
        status='rejected',
    ).exists()
    if already_rejected:
        return JsonResponse({'ok': False, 'msg': '此內容你先前的檢舉已被駁回，暫不接受重複檢舉。'}, status=400)

    # 清理補充說明
    details = bleach.clean(details_raw, tags=[], attributes={}, strip=True)

    # 建立檢舉
    try:
        AbuseReport.objects.create(
            target_type=target_type,
            post=post,
            comment_id=str(comment_id or ''),
            reply_id=str(reply_id or ''),
            reason=reason,
            details=details,
            snapshot_text=snapshot_text,
            reporter=request.user,
        )
    except Exception as e:
        return JsonResponse({'ok': False, 'msg': f'建立檢舉失敗：{e}'}, status=400)

    return JsonResponse({'ok': True, 'msg': '已送出檢舉，等待管理員審核'})


# ===== 管理員檢舉清單頁（待審 / 已處置 / 已駁回） =====
@admin_login_required
@require_http_methods(["GET"])
def review_reports(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name') or '管理員'

    if AbuseReport is None:
        return render(request, 'admin_review_reports.html', {
            'error': '尚未建立 AbuseReport 模型，請先確認模型設定。',
            'reports': [], 'status': 'pending', 'q': '',
            'report_counts': {'pending': 0, 'action_taken': 0, 'rejected': 0},
            'latest_reports': [],
            'admin_name': admin_name, 'admin_id': admin_id,
        })

    status = (request.GET.get('status') or 'pending').strip()
    if status not in {'pending', 'action_taken', 'rejected'}:
        status = 'pending'
    q = (request.GET.get('q') or '').strip()

    qs = AbuseReport.objects.all().order_by('-created_at')
    if status:
        qs = qs.filter(status=status)
    if q:
        qs = qs.filter(
            Q(snapshot_text__icontains=q) |
            Q(details__icontains=q) |
            Q(reason__icontains=q)
        )

    reports = list(qs[:200])
    report_counts = {
        'pending': AbuseReport.objects.filter(status='pending').count(),
        'action_taken': AbuseReport.objects.filter(status='action_taken').count(),
        'rejected': AbuseReport.objects.filter(status='rejected').count(),
    }
    latest_reports = list(AbuseReport.objects.all().order_by('-created_at')[:10])

    return render(request, 'admin_review_reports.html', {
        'reports': reports, 'status': status, 'q': q,
        'report_counts': report_counts, 'latest_reports': latest_reports,
        'admin_name': admin_name, 'admin_id': admin_id,
    })


# ===== 管理員「最終審核紀錄」頁（僅顯示 action_taken / rejected） =====
@admin_login_required
@require_http_methods(["GET"])
def report_decide(request):
    admin_id = request.session.get('admin_id')
    admin_name = request.session.get('admin_name') or '管理員'

    if AbuseReport is None:
        return render(request, 'admin_report_decide.html', {
            'reports': [], 'status': '', 'q': '',
            'admin_name': admin_name, 'admin_id': admin_id,
        })

    status = (request.GET.get('status') or '').strip()   # 可選：action_taken / rejected / 空(全部)
    q = (request.GET.get('q') or '').strip()

    qs = AbuseReport.objects.exclude(status='pending').order_by('-decided_at', '-created_at')
    if status in {'action_taken', 'rejected'}:
        qs = qs.filter(status=status)
    if q:
        qs = qs.filter(
            Q(snapshot_text__icontains=q) |
            Q(details__icontains=q) |
            Q(reason__icontains=q)     # ← 修正這裡
        )

    reports = list(qs[:300])

    return render(request, 'admin_report_decide.html', {
        'reports': reports, 'status': status, 'q': q,
        'admin_name': admin_name, 'admin_id': admin_id,
    })


# ===== 管理員動作（採取行動 / 駁回） =====
@admin_login_required
@require_POST
def act_on_report(request):
    if AbuseReport is None:
        return JsonResponse({'ok': False, 'msg': '尚未建立 AbuseReport 模型'}, status=501)

    try:
        report_id = request.POST['report_id']
        action = (request.POST.get('action') or '').strip()
        admin_note = (request.POST.get('admin_note') or '').strip()
    except MultiValueDictKeyError:
        return JsonResponse({'ok': False, 'msg': '缺少必要欄位'}, status=400)

    if action not in ('take_action', 'reject'):
        return JsonResponse({'ok': False, 'msg': '不支援的動作'}, status=400)

    try:
        report = AbuseReport.objects.get(pk=report_id)
    except AbuseReport.DoesNotExist:
        return JsonResponse({'ok': False, 'msg': '找不到檢舉'}, status=404)

    # 更新狀態與備註
    report.status = 'action_taken' if action == 'take_action' else 'rejected'
    report.admin_note = admin_note
    report.decided_at = timezone.now()

    # ✅ 只使用 session 的 admin_id，綁定到 Admins；不再使用 request.user
    sess_admin_id = request.session.get('admin_id')
    if sess_admin_id:
        try:
            # 直接把外鍵欄位寫入 DB 並同步記憶體
            AbuseReport.objects.filter(pk=report.pk).update(admin_id=int(sess_admin_id))
            report.admin_id = int(sess_admin_id)
            # 能對應到 Admins 物件就設；沒有也不阻塞
            if Admins is not None:
                admin_obj = Admins.objects.filter(pk=sess_admin_id).first()
                if admin_obj:
                    report.admin = admin_obj
        except Exception:
            pass

    report.save()

    # ✅ 成功後直接導向審核紀錄頁，並顯示提示
    status_label = '已處置' if report.status == 'action_taken' else '已駁回'
    messages.success(request, f'檢舉 #{report.id} {status_label}。')
    return redirect('report_decide')

# ===== 管理員：編輯審核紀錄（僅允許改 status / admin_note；reason 不可改） =====
@admin_login_required
@require_POST
def edit_report(request, report_id):
    if AbuseReport is None:
        return JsonResponse({'ok': False, 'msg': '尚未建立 AbuseReport 模型'}, status=501)

    # 取資料
    try:
        report = AbuseReport.objects.get(pk=report_id)
    except AbuseReport.DoesNotExist:
        messages.error(request, f'找不到檢舉 #{report_id}')
        return redirect('report_decide')

    # 僅接收狀態與備註
    status_new = (request.POST.get('status') or '').strip()
    admin_note = (request.POST.get('admin_note') or '').strip()

    # 驗證狀態
    allowed_status = {'pending', 'action_taken', 'rejected'}
    if status_new not in allowed_status:
        messages.error(request, '不支援的狀態值')
        return redirect('report_decide')

    # 更新欄位（不動 reason）
    report.status = status_new
    report.admin_note = admin_note

    # 狀態→時間：pending 清空；其餘更新為現在
    report.decided_at = None if status_new == 'pending' else timezone.now()

    # 紀錄處理管理員（沿用 session）
    sess_admin_id = request.session.get('admin_id')
    if sess_admin_id:
        try:
            AbuseReport.objects.filter(pk=report.pk).update(admin_id=int(sess_admin_id))
            report.admin_id = int(sess_admin_id)
            if Admins is not None:
                admin_obj = Admins.objects.filter(pk=sess_admin_id).first()
                if admin_obj:
                    report.admin = admin_obj
        except Exception:
            pass

    report.save()
    messages.success(request, f'已更新檢舉 #{report.id}（狀態：{report.status}）。')
    return redirect('report_decide')
@admin_login_required
@require_POST
def delete_report_target(request, report_id):
    """已處置案件的後續動作：刪除被檢舉目標（貼文 / 留言 / 回覆）"""
    if AbuseReport is None:
        messages.error(request, '尚未建立 AbuseReport 模型')
        return redirect('report_decide')

    # 取檢舉
    try:
        report = AbuseReport.objects.get(pk=report_id)
    except AbuseReport.DoesNotExist:
        messages.error(request, f'找不到檢舉 #{report_id}')
        return redirect('report_decide')

    # 僅允許「已處置」才可刪目標
    if report.status != 'action_taken':
        messages.error(request, '僅限狀態為「已處置」的案件才能刪除目標。')
        return redirect('report_decide')

    # 取貼文
    post = getattr(report, 'post', None)
    if post is None:
        # 後備：以 id 再查一次
        try:
            post = _get_post_by_any_id(getattr(report, 'post_id', ''))
        except Exception:
            post = None
    if post is None and report.target_type != 'post':
        messages.error(request, '找不到對應貼文，無法刪除留言/回覆。')
        return redirect('report_decide')

    target_type = report.target_type
    try:
        if target_type == 'post':
            # 直接刪除整篇貼文
            if post is None:
                messages.error(request, '貼文已不存在。')
                return redirect('report_decide')
            post.delete()
            done_msg = '已刪除貼文'

        elif target_type == 'comment':
            comments = _load_comments(post)
            idx, c = _find_comment(comments, report.comment_id)
            if c is None:
                messages.error(request, '找不到要刪除的留言（可能已被刪除）。')
                return redirect('report_decide')
            del comments[idx]
            post.comments = json.dumps(comments, ensure_ascii=False)
            post.save(update_fields=['comments'])
            done_msg = '已刪除留言'

        elif target_type == 'reply':
            comments = _load_comments(post)
            cidx, c = _find_comment(comments, report.comment_id)
            if c is None:
                messages.error(request, '找不到要刪除的回覆（上層留言可能已被刪除）。')
                return redirect('report_decide')

            parent_list, ridx, r = _find_reply_recursive(c.get('replies') or [], report.reply_id)
            if r is None:
                messages.error(request, '找不到要刪除的回覆（可能已被刪除）。')
                return redirect('report_decide')

            del parent_list[ridx]
            comments[cidx] = c
            post.comments = json.dumps(comments, ensure_ascii=False)
            post.save(update_fields=['comments'])
            done_msg = '已刪除回覆'

        else:
            messages.error(request, '不支援的檢舉類型')
            return redirect('report_decide')

    except Exception as e:
        messages.error(request, f'刪除失敗：{e}')
        return redirect('report_decide')

    # 記錄操作者到 report（沿用你的作法）
    sess_admin_id = request.session.get('admin_id')
    if sess_admin_id:
        try:
            AbuseReport.objects.filter(pk=report.pk).update(admin_id=int(sess_admin_id))
            report.admin_id = int(sess_admin_id)
        except Exception:
            pass

    # 在備註追加一行紀錄（可省略）
    try:
        ts = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        note = (report.admin_note or '').strip()
        note_line = f"[{ts}] {done_msg}"
        report.admin_note = f"{note}\n{note_line}" if note else note_line
        report.save(update_fields=['admin_note'])
    except Exception:
        pass

    messages.success(request, f"檢舉 #{report.id}：{done_msg}")
    return redirect('report_decide')




# ------------ /交流區後端（整合版）------------




















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
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse

# from django.shortcuts import redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail
# from django.http import HttpResponse
# from .models import PemapAll

# # @login_required
# def admin_send_email(request, p_id):
#     item = get_object_or_404(PemapAll, p_id=p_id)

#     if request.method == 'POST':
#         to_email = item.poster_gmail
#         subject = request.POST.get('subject', '關於您的報告審核結果')
#         message = request.POST.get('message', '')

#         try:
#             send_mail(subject, message, '你的發信地址@example.com', [to_email])
#             # 寄信成功後，跳轉到管理員審核列表頁
#             return redirect('admin_decide')
#         except Exception as e:
#             return HttpResponse(f"寄信失敗: {str(e)}")

#     return render(request, 'admin_send_email.html', {
#         'item': item,
#         'to_email': item.poster_gmail,
#     })


# @login_required
def admin_send_email(request, p_id):
    item = get_object_or_404(PemapAll, p_id=p_id)

    if request.method == 'POST':
        to_email = item.poster_gmail
        subject = request.POST.get('subject', '關於您的報告審核結果')
        message = request.POST.get('message', '')

        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
            messages.success(request, "信件已成功寄出！")
            return redirect('admin_decide')
        except Exception as e:
            messages.error(request, f"寄信失敗: {str(e)}")
            return redirect('admin_send_email', p_id=p_id)

    return render(request, 'admin_send_email.html', {
        'item': item,
        'to_email': item.poster_gmail,
        'user_reason': item.reason,   # 把使用者當初的輸入傳給模板
    })



# views.py


# class PemapWithSubkindViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = PemapWithSubkind.objects.all()
#     serializer_class = PemapWithSubkindSerializer




#------------------------聊天室---------------------
from .models import ChatRoom
from django.views.decorators.csrf import csrf_exempt
import json

def chatrooms_api(request):
    rooms = ChatRoom.objects.all().values('id', 'city', 'district', 'click_count')
    return JsonResponse(list(rooms), safe=False)


# 取得聊天室訊息
from .models import ChatMessage

# 取得聊天室訊息
def chat_messages_api(request, room_id):
    if request.method == 'GET':
        messages = ChatMessage.objects.filter(region=room_id).order_by('timestamp')
        data = [{
            'id': msg.id,
            'nickname': msg.nickname or msg.user.username,
            'user_id': msg.user.username if msg.user else '匿名',
            'message': msg.message,
            'reply_to_id': msg.reply_to.id if msg.reply_to else None,
            'reply_to_text': msg.reply_to.message if msg.reply_to else None,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'status_color': msg.user.status_color if msg.user else '#000000'
        } for msg in messages]
        return JsonResponse(data, safe=False)




@login_required
def chat_send_api(request, room_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            if not message:
                return JsonResponse({'status': 'error', 'msg': '訊息不能為空'})

            # 找到 ThisUserProfile
            user_profile = ThisUserProfile.objects.get(gmail=request.user.email)

            chat_msg = ChatMessage.objects.create(
                user=user_profile,
                region=str(room_id),
                message=message
            )

            return JsonResponse({
                'status': 'success',
                'message': {
                    'id': chat_msg.id,
                    'nickname': chat_msg.nickname,
                    'message': chat_msg.message,
                    'timestamp': chat_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'status_color': user_profile.status_color
                }
            })
        except ThisUserProfile.DoesNotExist:
            return JsonResponse({'status': 'error', 'msg': '請先至個人資料設定填寫email'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'msg': str(e)})
    else:
        return JsonResponse({'status': 'error', 'msg': '只接受 POST'}, status=405)



from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

@login_required
@csrf_exempt
def send_message(request, room_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'status': 'error', 'msg': '資料格式錯誤'})

        message_text = data.get('message')
        nickname = data.get('nickname', '').strip()
        reply_to_id = data.get('reply_to_id')

        if not message_text:
            return JsonResponse({'status': 'error', 'msg': '訊息不可為空'})

        try:
            user_profile = ThisUserProfile.objects.get(gmail=request.user.email)
        except ThisUserProfile.DoesNotExist:
            return JsonResponse({'status': 'error', 'msg': '找不到使用者資料'})

        reply_to_msg = None
        if reply_to_id:
            try:
                reply_to_msg = ChatMessage.objects.get(id=reply_to_id)
            except ChatMessage.DoesNotExist:
                pass

        chat_msg = ChatMessage.objects.create(
            user=user_profile,
            region=room_id,
            message=message_text,
            nickname=nickname if nickname else None,
            reply_to=reply_to_msg
        )

        return JsonResponse({
            'status': 'ok',
            'message': {
                'id': chat_msg.id,
                'nickname': chat_msg.nickname,
                'message': chat_msg.message,
                'reply_to_id': reply_to_msg.id if reply_to_msg else None,
                'reply_to_text': reply_to_msg.message if reply_to_msg else None,
                'timestamp': chat_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'status_color': user_profile.status_color
            }
        })

    return JsonResponse({'status': 'error', 'msg': '僅接受 POST'})




#---------看自己收藏的聊天室---------------
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import ThisUserProfile, ChatRoom, FavoriteChatRoom

# ------------- 查看收藏聊天室 -------------
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Count
import json

def chatroom_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "請先登入才能使用聊天室")
        return render(request, "chatroom.html", {
            "user_profile": None,
            "favorites": [],
            "favorite_chatroom_ids": "[]",
            "chatrooms_json": "[]",
        })

    # 已登入，正常流程
    try:
        user_profile = ThisUserProfile.objects.get(gmail=request.user.email)
        favorites = FavoriteChatRoom.objects.filter(user=user_profile).select_related('chat_room')
        favorite_ids = [fav.chat_room.id for fav in favorites]
    except ThisUserProfile.DoesNotExist:
        user_profile = None
        favorites = []
        favorite_ids = []
        messages.warning(request, "找不到您的使用者資料，部分功能可能無法使用")

    chatrooms = ChatRoom.objects.annotate(
        fav_count=Count('favorited_by_users')
    ).order_by('-fav_count')

    chatroom_list = list(chatrooms.values('id', 'city', 'district', 'fav_count'))

    return render(request, 'chatroom.html', {
        'user_profile': user_profile,
        'favorites': favorites,
        'favorite_chatroom_ids': json.dumps(favorite_ids),
        'chatrooms_json': json.dumps(chatroom_list),
    })


# ------------- 加入收藏 -------------
@require_POST
@login_required
def add_to_favorites(request):
    room_id = request.POST.get('room_id')
    chat_room = get_object_or_404(ChatRoom, id=room_id)

    try:
        profile = ThisUserProfile.objects.get(gmail=request.user.email)
    except ThisUserProfile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '使用者資料未建立'})

    favorite, created = FavoriteChatRoom.objects.get_or_create(user=profile, chat_room=chat_room)
    if created:
        return JsonResponse({'status': 'success', 'message': '已加入收藏'})
    else:
        return JsonResponse({'status': 'exists', 'message': '已經收藏過了'})


# ------------- 收藏切換（新增/移除）-------------
@require_POST
@login_required
def toggle_favorite(request):
    try:
        user_profile = ThisUserProfile.objects.get(gmail=request.user.email)
    except ThisUserProfile.DoesNotExist:
        return JsonResponse({'status': 'error', 'msg': '找不到使用者資料'}, status=404)

    room_id = request.POST.get('room_id')
    if not room_id:
        return JsonResponse({'status': 'error', 'msg': '缺少 room_id'}, status=400)

    chat_room = get_object_or_404(ChatRoom, id=room_id)
    fav_obj = FavoriteChatRoom.objects.filter(user=user_profile, chat_room=chat_room).first()

    if fav_obj:
        fav_obj.delete()
        return JsonResponse({'status': 'removed'})
    else:
        FavoriteChatRoom.objects.create(user=user_profile, chat_room=chat_room)
        return JsonResponse({'status': 'added'})





# ----------------看別人的--------------------------

from django.shortcuts import render, get_object_or_404
from .models import ThisUserProfile  # 假設你的使用者資料表叫 UserProfile

def public_profile(request, gmail):
    # 用 gmail 找使用者
    user = get_object_or_404(ThisUserProfile, gmail=gmail)
    return render(request, "public_profile.html", {"profile_user": user})



# --------商家廣告-------s
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import StoreAll, StoreAd, StoreAdImage, StoreAdHistory, StoreAdHistoryImage
from .forms import StoreAdForm
import os
from django.utils import timezone

def upload_store_ad(request):
    if request.method == 'POST':
        form = StoreAdForm(request.POST)
        if form.is_valid():
            st_id = form.cleaned_data['st_id']

            # 取得商家
            try:
                store = StoreAll.objects.get(st_id=st_id)
            except StoreAll.DoesNotExist:
                form.add_error('st_id', '找不到此商家編號')
                return render(request, 'store_upload_ad.html', {'form': form})

            # 建立廣告申請紀錄（History）
            ad_history = StoreAdHistory.objects.create(
                st=store,
                ad_content=form.cleaned_data['ad_content'],
                ad_radius=form.cleaned_data['ad_radius'],
                enabled=form.cleaned_data['enabled'],
                status='pending',
                created_at=timezone.now()
            )

            # 儲存圖片到 HistoryImage
            for img_file in request.FILES.getlist('images'):
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'ads')
                os.makedirs(upload_dir, exist_ok=True)

                filepath = os.path.join(upload_dir, img_file.name)
                with open(filepath, 'wb+') as dest:
                    for chunk in img_file.chunks():
                        dest.write(chunk)

                StoreAdHistoryImage.objects.create(
                    history=ad_history,
                    image_url=f"/media/ads/{img_file.name}"
                )

            # 提交完成後提示送審成功
            return render(request, 'store_upload_ad.html', {
                'form': StoreAdForm(),
                'message': '廣告申請已送審，請等待管理員審核'
            })

    else:
        form = StoreAdForm()

    return render(request, 'store_upload_ad.html', {'form': form})



# --------- API: 根據商家編號取得廣告 ---------

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import StoreAll, StoreAd

def get_store_ad(request):
    st_id = request.GET.get('st_id')
    if not st_id:
        return JsonResponse({'error': 'st_id is required'}, status=400)

    try:
        # 先取得商家
        store = StoreAll.objects.get(st_id=st_id)
    except StoreAll.DoesNotExist:
        return JsonResponse({
            'ad_content': '',
            'images': [],
            'ad_radius': 200,
            'enabled': True,
            'status': None,
        })

    try:
        # 嘗試取得廣告
        ad = StoreAd.objects.get(st=store)
        images = [img.image_url for img in ad.images.all()] if hasattr(ad, 'images') else []
        return JsonResponse({
            'ad_content': ad.ad_content or '',
            'images': images,
            'ad_radius': ad.ad_radius,
            'enabled': ad.enabled,
            'status': ad.status,  # pending / approved / rejected
        })
    except StoreAd.DoesNotExist:
        # 如果商家沒有廣告
        return JsonResponse({
            'ad_content': '',
            'images': [],
            'ad_radius': 200,
            'enabled': True,
            'status': None,
        })



# ------------------審核廣告--------------------
# 顯示所有待審核廣告
def admin_review_ads(request):
    ads = StoreAdHistory.objects.filter(status='pending').order_by('created_at')
    return render(request, 'admin_review_ads.html', {'ads': ads})


# 審核單一廣告
def review_store_ad(request, history_id, action):
    ad = get_object_or_404(StoreAdHistory, pk=history_id)

    if action == "approve":
        ad.status = "approved"
    elif action == "reject":
        ad.status = "rejected"

    ad.save()
    return redirect("admin_review_ads")



# 上傳廣告時建立歷史紀錄
def upload_store_ad(request):
    if request.method == 'POST':
        form = StoreAdForm(request.POST)
        if form.is_valid():
            st_id = form.cleaned_data['st_id']

            # 取得商家
            try:
                store = StoreAll.objects.get(st_id=st_id)
            except StoreAll.DoesNotExist:
                form.add_error('st_id', '找不到此商家編號')
                return render(request, 'store_upload_ad.html', {'form': form})

            # 建立歷史廣告紀錄
            ad_history = StoreAdHistory.objects.create(
                st=store,
                ad_content=form.cleaned_data['ad_content'],
                ad_radius=form.cleaned_data['ad_radius'],
                enabled=form.cleaned_data['enabled'],
                status='pending'
            )

            # 儲存圖片到歷史紀錄資料夾
            for img_file in request.FILES.getlist('images'):
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'ads_history')
                os.makedirs(upload_dir, exist_ok=True)

                filepath = os.path.join(upload_dir, img_file.name)
                with open(filepath, 'wb+') as dest:
                    for chunk in img_file.chunks():
                        dest.write(chunk)

                # 建立對應圖片
                StoreAdImage.objects.create(
                    st=ad_history,  # 這裡改成指向歷史廣告
                    image_url=f"/media/ads_history/{img_file.name}"
                )

            return redirect('store_map')

    else:
        form = StoreAdForm()

    return render(request, 'store_upload_ad.html', {'form': form})


# API: 取得商家廣告
def stores_with_ads(request):
    try:
        stores = StoreAll.objects.all()
        result = []

        for store in stores:
            ad_data = {
                'st_id': store.st_id,
                'store_name': store.store_name,
                'ad_content': '',
                'ad_radius': 200,
                'enabled': False,
                'status': None,
                'images': []
            }

            # 找這個商家所有 approved 廣告
            approved_ads = store.ad_histories.filter(status='approved').order_by('-created_at')

            if approved_ads.exists():
                # 取最新一筆 approved 廣告
                ad = approved_ads.first()
                ad_data.update({
                    'ad_content': ad.ad_content or '',
                    'ad_radius': ad.ad_radius or 200,
                    'enabled': ad.enabled,
                    'status': ad.status,
                    'images': [img.image_url for img in ad.st.ad_histories.first().images.all()]  # 如果你有存 images
                })
            else:
                # 沒有 approved 廣告，但如果 store 本身通過審核也顯示
                if store.review_status == 'approved':
                    ad_data['enabled'] = False  # 沒有廣告，但顯示商家位置

            result.append(ad_data)

        return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 頁面：上傳廣告
def upload_ad_page(request):
    return render(request, "store_upload_ad.html")
