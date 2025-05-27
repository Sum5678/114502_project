from django.shortcuts import render
from .models import TaiwanRegion, PoliceAddress #資料表的
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .forms import AutoDialForm


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

def nearest_police(request):
    # 顯示下拉選單與地圖的主頁面
    return render(request, 'nearest_police.html')

def get_cities(request):
    cities = TaiwanRegion.objects.values_list('country_city', flat=True).distinct()
    return JsonResponse(list(cities), safe=False)

def get_city_district_data(request):
    # 從資料庫撈出所有縣市與區
    data = {}
    regions = TaiwanRegion.objects.all()
    for region in regions:
        city = region.county_city
        district = region.district_town
        if city not in data:
            data[city] = []
        data[city].append(district)
    return JsonResponse(data)

def get_districts(request):
    city = request.GET.get('city')
    districts = TaiwanRegion.objects.filter(country_city=city).values_list('district_town', flat=True).distinct()
    return JsonResponse(list(districts), safe=False)

def get_police_by_district(request):
    district = request.GET.get('district')
    print(f"收到 district: {district}")  # ← 加這個看看有沒有收到資料

    data = []
    if district:
        results = TaiwanRegion.objects.filter(district_town=district)
        for r in results:
            data.append({
                'station': r.police_station,
                'phone': r.phone,
                'lat': r.latitude,
                'lng': r.longitude,
            })
    return JsonResponse({'data': data})

@require_GET
def get_police_by_district(request):
    district = request.GET.get('district')
    if not district:
        return JsonResponse([], safe=False)

    # 假設 district 是字串，可以直接過濾
    police_stations = PoliceAddress.objects.filter(district=district)

    data = []
    for station in police_stations:
        data.append({
            'name': station.name,
            'phone': station.phone,
            'latitude': station.latitude,
            'longitude': station.longitude,
        })

    return JsonResponse(data, safe=False)

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

# views.py

from django.shortcuts import render
from django.core.files.storage import default_storage
import cv2
import os

# 載入人臉辨識模型（記得在 settings.py 設定 STATICFILES_DIRS）
face_cascade = cv2.CascadeClassifier('myapp\static\haarcascade_frontalface_default.xml')

def face_detection_view(request):
    result_img = None

    if request.method == 'POST' and request.FILES.get('image'):
        file = request.FILES['image']
        input_path = os.path.join('myapp', 'static', 'input.jpg')
        with open(input_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        img = cv2.imread(input_path)
        if img is None:
            return render(request, 'index0527.html', {'result_img': None, 'error': '無法讀取圖片，請重新上傳'})

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        output_path = os.path.join('myapp', 'static', 'output.jpg')
        cv2.imwrite(output_path, img)
        result_img = 'output.jpg'

    return render(request, 'index0527.html', {'result_img': result_img})






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
                    return redirect('login')  # 這裡是你說的 0101login/ 對應 name='login'
                else:
                    messages.error(request, "密碼錯誤")
            except UserProfile.DoesNotExist:
                messages.error(request, "帳號不存在")

        # ✅ 註冊邏輯：註冊後直接登入 + 跳首頁
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
                return redirect('login')  # 這裡一樣指向 0101login/
    
    return render(request, '01_userlogin.html')



##google登入
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth

def profile(request):
    user = request.user
    if user.is_authenticated:
        try:
            google_login = user.social_auth.filter(provider='google-oauth2').first()
            extra_data = google_login.extra_data
            google_id = google_login.uid
            email = user.email
            name = extra_data.get('name')
            picture = extra_data.get('picture')

            return render(request, 'profile.html', {
                'google_id': google_id,
                'email': email,
                'name': name,
                'picture': picture,
            })
        except UserSocialAuth.DoesNotExist:
            return render(request, 'profile.html', {
                'error': '此帳號不是由 Google 登入',
            })
    return redirect('login')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # 登出並清除 session
    return redirect('login')  # 重定向到登入頁



####登入後填表的
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from .models import ThisUserProfile
from django.contrib.auth.models import User
 

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ThisUserProfile
from social_django.models import UserSocialAuth

def create_user_profile(request):
    user = request.user
    try:
        # 嘗試從 Google 登入獲取 Gmail 地址
        social_user = UserSocialAuth.objects.get(user=user, provider='google-oauth2')
        gmail = social_user.extra_data.get('email', '')
    except UserSocialAuth.DoesNotExist:
        # 如果沒有綁定 Google，則為空或使用其他方式獲取 Gmail
        gmail = ''

    if request.method == 'POST':
        # 根據當前登入的使用者資料創建或更新 ThisUserProfile
        profile, created = ThisUserProfile.objects.update_or_create(
            gmail=gmail,  # 使用 gmail 作為識別
            defaults={
                'username': request.POST.get('username'),
                'default_nickname1': request.POST.get('default_nickname1'),
                'default_nickname2': request.POST.get('default_nickname2'),
                'emergency_contact_phone': request.POST.get('emergency_contact_phone'),
                'emergency_contact_gmail': request.POST.get('emergency_contact_gmail'),
                'default_message': request.POST.get('default_message'),
                'self_intro': request.POST.get('self_intro'),
            }
        )

        return render(request, 'thank_you.html')

    return render(request, 'usdata.html', {'gmail': gmail})


from django.shortcuts import render, redirect
from .models import ThisUserProfile

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

    return render(request, 'your_template.html')




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


#--------------------------------01--------------------------------------------------------
# -------------------------------- submit_report（我要填單功能） --------------------------------
# myapp/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import PemapAll

@csrf_exempt  # 暫時關閉 CSRF 驗證，之後可用 token 或前端設置
def submit_report(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # 從前端資料抓欄位
            poster_id = data.get('poster_id', 'anonymous')  # 你可以依需求調整
            display_name = data.get('display_name', '匿名')
            kind = data.get('kind')
            reason = data.get('reason')
            address = data.get('address')
            latitude = float(data.get('latitude', 0))
            longitude = float(data.get('longitude', 0))
            img_url = data.get('img_url', '')

            # 建立資料庫紀錄
            report = PemapAll.objects.create(
                poster_id=poster_id,
                display_name=display_name,
                kind=kind,
                reason=reason,
                address=address,
                latitude=latitude,
                longitude=longitude,
                img_url=img_url,
                review_status='待處理'
            )

            return JsonResponse({'status': 'success', 'message': '回報成功'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': '只支援POST'})
