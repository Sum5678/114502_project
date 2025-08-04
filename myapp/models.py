# from django.db import models
from django.db import models
from django.utils import timezone


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

class ThisUserProfile(models.Model):
    username = models.CharField(max_length=100)
    gmail = models.EmailField()
    default_nickname1 = models.CharField(max_length=100, blank=True)
    default_nickname2 = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_gmail = models.EmailField(blank=True)
    default_message = models.TextField(blank=True)
    self_intro = models.TextField(blank=True)
    user_images = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status_color = models.CharField(max_length=20, default='#63b3ed')

    class Meta:
        db_table = 'this_user_profile'

    def __str__(self):
        return self.username





from django.shortcuts import render, redirect
from .models import ThisUserProfile
from django.contrib.auth.decorators import login_required

@login_required
def create_user_profile(request):
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        username = request.POST['username']
        gmail = request.POST['gmail']
        default_nickname1 = request.POST.get('default_nickname1', '')
        default_nickname2 = request.POST.get('default_nickname2', '')
        emergency_contact_phone = request.POST.get('emergency_contact_phone', '')
        emergency_contact_gmail = request.POST.get('emergency_contact_gmail', '')
        default_message = request.POST.get('default_message', '')
        self_intro = request.POST.get('self_intro', '')

        # 🔧 重點是這裡！根據目前登入使用者更新或建立 profile
        ThisUserProfile.objects.update_or_create(
            user=request.user,  # 加入這行
            defaults={
                'username': username,
                'gmail': gmail,
                'default_nickname1': default_nickname1,
                'default_nickname2': default_nickname2,
                'emergency_contact_phone': emergency_contact_phone,
                'emergency_contact_gmail': emergency_contact_gmail,
                'default_message': default_message,
                'self_intro': self_intro,
                'user_images': profile_image,
            }
        )

        return redirect('profile')  # 改成你的 profile 頁面名稱

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
class EducationPage(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    image_url = models.BinaryField()

    class Meta:
        db_table = 'education_page'  # 指定實際資料表名稱
        managed = False  # 不讓 Django 管理這張表（不會對它做 migrate）

    def __str__(self):
        return self.title
    


from django.db import models

class TaiwanRegion(models.Model):
    zipcode = models.CharField(max_length=5)
    country_city = models.CharField(max_length=50)
    district_town = models.CharField(max_length=50)

    class Meta:
        db_table = 'taiwan_regions'


from django.db import models

class Region(models.Model):
    zipcode = models.CharField(max_length=10)
    country_city = models.CharField(max_length=50)
    district_town = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.country_city} {self.district_town} ({self.zipcode})"


class PoliceAddress(models.Model):
    precinct_name = models.TextField()
    zipcode = models.CharField(max_length=5)
    address = models.TextField()
    phone = models.TextField()
    POINT_X = models.FloatField()  # DOUBLE 對應 FloatField
    POINT_Y = models.FloatField()

    def __str__(self):
        return f"{self.precinct_name} ({self.zipcode})"

    class Meta:
        db_table = 'PoliceAddress'
# ------------------------- Pemap 回報資料模型（對應 pemap_all 資料表） -------------------------
from django.contrib.auth.models import User
class PemapAll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    p_id = models.AutoField(primary_key=True)
    poster_id = models.CharField(max_length=255)  # 自動生成
    display_name = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    reason = models.TextField()
    address = models.CharField(max_length=255, default="尚未提供") 
    latitude = models.FloatField()
    longitude = models.FloatField()
    img_url = models.TextField(blank=True)  # ✅ 改成 TextField 儲存 base64 字串
    time_created = models.DateTimeField(default=timezone.now)
    time_reviewed = models.DateTimeField(null=True, blank=True)
    review_status = models.CharField(max_length=50, default="待審核")
    admin_id = models.IntegerField(default=99999)
    poster_gmail = models.EmailField(max_length=255, null=True, blank=True)



    class Meta:
        db_table = 'pemap_all'
#-----------------------------------store----------------------------------------------------------
from django.contrib.auth.models import User
class StoreAll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    st_id = models.CharField(max_length=50, primary_key=True)
    poster_id = models.CharField(max_length=255, blank=True)
    store_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, default="尚未提供")
    latitude = models.FloatField()
    longitude = models.FloatField()
    business_hours = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_status = models.CharField(max_length=20, default='pending')  # 審核狀態（預設 pending）
    admin_id = models.IntegerField(default=99999)
    poster_gmail = models.EmailField(max_length=255, null=True, blank=True)



    class Meta:
        db_table = 'store_all'  # << 指定實際的 MySQL 資料表名稱



#-------------------登入資料----------------------------------------------
from django.db import models

class Admins(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=45, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    admin_gmail = models.CharField(max_length=100, unique=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Admins'
        managed = False  # 不讓 Django 嘗試管理這個資料表


from django.contrib.auth.models import User  # ✅ 引入 Django 原生 User
from django.db import models
from django.core.validators import MaxLengthValidator  # ✅ 加入字數限制驗證器

class ChatInteraction(models.Model):
    interaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'  # ✅ 指定欄位名與資料表相符
    )
    nickname = models.CharField(max_length=50)
    bgcolor = models.CharField(max_length=20)
    avatar_style = models.CharField(max_length=50)
    avatar_url = models.URLField(max_length=300)
    title = models.CharField(max_length=50)
    message_content = models.CharField(max_length=300)
    like_heart_count = models.IntegerField(default=0)  # ✅ ❤️ 愛心數欄位（你新增的）
    liked_user_ids = models.TextField(default="[]")  # 儲存 JSON 格式字串


    # ✅ 不用 auto_now_add，讓 MySQL 自動填入時間
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'chat_interaction'  # ✅ 對應資料表名稱
        managed = False  # ✅ 禁止 Django 自行創建或修改這張表


#----------view的
class PemapWithSubkind(models.Model):
    p_id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    subkind = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)
    img_url = models.TextField(blank=True)
    time_created = models.DateTimeField()

    class Meta:
        managed = False  # 不由 Django 管理這個資料表
        db_table = 'pemap_with_subkind'  # 要跟你的 VIEW 名稱一致

