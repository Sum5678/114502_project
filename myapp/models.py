# from django.db import models
from django.db import models



# Create your models here.








#-------------------------想 user_login--------------------------------
from django.db import models

class UserProfile(models.Model):
    email = models.EmailField(unique=True)  # 當帳號
    google_name = models.CharField(max_length=100, blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255)  # 儲存加密後密碼
    show_name_option = models.IntegerField(default=3)  # 1帳號/2暱稱/3匿名
    avatar_url = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    intro = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)




####登入後填表的
from django.db import models
from django.contrib.auth.models import User


from django.db import models

from django.db import models

class ThisUserProfile(models.Model):
    username = models.CharField(max_length=100)
    gmail = models.EmailField()
    default_nickname1 = models.CharField(max_length=100, blank=True)
    default_nickname2 = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_gmail = models.EmailField(blank=True)
    default_message = models.TextField(blank=True)
    self_intro = models.TextField(blank=True)
    user_images = models.ImageField(upload_to='user_images/', blank=True, null=True)

    class Meta:
        db_table = 'this_user_profile'  # 🔧 加這行就會對應到你手動建的表

    def __str__(self):
        return self.username

    

from django.shortcuts import render, redirect
from .models import ThisUserProfile

def create_user_profile(request):
    if request.method == 'POST':
        # 取得表單資料
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

    return render(request, 'usdata.html')


from django.db import models

class Incident(models.Model):
    description = models.TextField()  # 事件描述
    latitude = models.FloatField()    # 緯度
    longitude = models.FloatField()   # 經度
    time = models.DateTimeField()     # 發生時間
    created_at = models.DateTimeField(auto_now_add=True)  # 回報時間

    def __str__(self):
        return f"{self.description} ({self.latitude}, {self.longitude})"


#-------------------------------------------------------------------------
class TaiwanRegion(models.Model):
    zipcode = models.CharField(max_length=10)
    country_city = models.CharField(max_length=50)
    district_town = models.CharField(max_length=50)

class PoliceAddress(models.Model):
    分局名稱 = models.CharField(max_length=100)
    郵遞區號 = models.CharField(max_length=10)
    地址 = models.CharField(max_length=200)
    電話 = models.CharField(max_length=50)
    POINT_X = models.FloatField()  # 經度
    POINT_Y = models.FloatField()  # 緯度

    def __str__(self):
        return self.分局名稱
    
# ------------------------- Pemap 回報資料模型（對應 pemap_all 資料表） -------------------------

class PemapAll(models.Model):
    p_id = models.AutoField(primary_key=True)
    poster_id = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    kind = models.CharField(max_length=50)
    reason = models.TextField()
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    img_url = models.CharField(max_length=255, blank=True, null=True)  # 如果儲存圖片路徑
    time_created = models.DateTimeField(auto_now_add=True)
    time_reviewed = models.DateTimeField(blank=True, null=True)
    review_status = models.CharField(max_length=50, default='待處理')

    class Meta:
        db_table = 'pemap_all'