from django.shortcuts import render
from .models import TaiwanRegion, PoliceAddress #資料表的
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .forms import AutoDialForm
from django.views.decorators.csrf import csrf_exempt



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
    return render(request, 'education_crud/education_list.html', {'pages': pages})

def education_create(request):
    if request.method == 'POST':
        form = EducationPageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('education_list')
    else:
        form = EducationPageUploadForm()
    return render(request, 'education_crud/education_form.html', {'form': form})

def education_update(request, pk):
    page = get_object_or_404(EducationPage, pk=pk)
    if request.method == 'POST':
        form = EducationPageUploadForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('education_list')
    else:
        form = EducationPageUploadForm(instance=page)
    return render(request, 'education_crud/education_form.html', {'form': form})

def education_delete(request, pk):
    page = get_object_or_404(EducationPage, pk=pk)
    if request.method == 'POST':
        page.delete()
        return redirect('education_list')
    return render(request, 'education_crud/education_confirm_delete.html', {'page': page})

#地圖顯示資料 0528
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


#縣市後端
# regions/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import TaiwanRegion
from .region_forms import TaiwanRegionForm

def taiwan_regions_admin(request):
    if request.method == 'POST':
        if 'edit_id' in request.POST and request.POST['edit_id']:
            region = get_object_or_404(TaiwanRegion, id=request.POST['edit_id'])
            form = TaiwanRegionForm(request.POST, instance=region)
        else:
            form = TaiwanRegionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('taiwan_regions_admin')
    elif 'delete_id' in request.GET:
        TaiwanRegion.objects.filter(id=request.GET['delete_id']).delete()
        return redirect('taiwan_regions_admin')

    data = TaiwanRegion.objects.all().order_by('country_city', 'district_town')
    return render(request, 'taiwan_regions_admin.html', {'regions': data})

#警局地址後端
from django.shortcuts import render, get_object_or_404, redirect
from .models import PoliceAddress
from .police_forms import PoliceAddressForm

def police_address_list(request):
    addresses = PoliceAddress.objects.all().order_by('precinct_name')
    return render(request, 'police_address_admin.html', {'addresses': addresses})

def police_address_add(request):
    if request.method == 'POST':
        form = PoliceAddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('police_address_list')
    else:
        form = PoliceAddressForm()
    return render(request, 'police_address_edit.html', {'form': form, 'action': '新增'})

def police_address_edit(request, pk):
    address = get_object_or_404(PoliceAddress, pk=pk)
    if request.method == 'POST':
        form = PoliceAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('police_address_list')
    else:
        form = PoliceAddressForm(instance=address)
    return render(request, 'police_address_edit.html', {'form': form, 'action': '編輯'})

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

# views.py

from django.shortcuts import render
from django.core.files.storage import default_storage
import cv2
import os

# 載入人臉辨識模型（記得在 settings.py 設定 STATICFILES_DIRS）
face_cascade = cv2.CascadeClassifier('myapp/static/haarcascade_frontalface_default.xml')

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
            # 取得人臉區域
            face_roi = img[y:y+h, x:x+w]

            # 縮小再放大做馬賽克
            small = cv2.resize(face_roi, (10, 10), interpolation=cv2.INTER_LINEAR)
            mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

            # 替換原圖區域為馬賽克
            img[y:y+h, x:x+w] = mosaic

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
    social_user = UserSocialAuth.objects.filter(user=user, provider='google-oauth2').first()
    if social_user:
        gmail = social_user.extra_data.get('email', '')
    else:
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

    return render(request, 'thank_you.html')

##登入後顯示資料
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ThisUserProfile  # 假設你的使用者資料模型叫這個

@login_required
def profile(request):
    user = request.user
    try:
        profile = ThisUserProfile.objects.get(user=user)
    except ThisUserProfile.DoesNotExist:
        profile = None

    return render(request, 'thank_you.html', {
        'user': user,
        'profile': profile
    })




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

from django.shortcuts import render

def map_view(request):
    return render(request, '999map.html')



from django.http import JsonResponse
from .models import PemapAll  # 改成引用 PemapAll

def reports_json(request):
    reports = PemapAll.objects.filter(review_status='0').values(
        'latitude', 'longitude', 'display_name', 'reason', 'time_created'
    )
    data = list(reports)
    return JsonResponse(data, safe=False)



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

def admin_login(request):
    if request.method == "POST":
        gmail = request.POST.get('admin_gmail')
        password = request.POST.get('password')

        try:
            admin = Admins.objects.get(admin_gmail=gmail, password=password)
            request.session['admin_id'] = admin.admin_id
            request.session['admin_name'] = admin.name  # 如果你後面會用到名字
            return redirect('show_judge_page')
        except Admins.DoesNotExist:
            return render(request, 'admin_login.html', {'error': '帳號或密碼錯誤'})

    return render(request, 'admin_login.html')



