# from django.db import models
from django.db import models
from django.utils import timezone
from django.conf import settings



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
import json  # ✅ 新增：處理 JSON

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
    like_heart_count = models.IntegerField(default=0)  # ❤️ 愛心數欄位
    liked_user_ids = models.TextField(default="[]")    # 👍 按讚清單
    saved_user_ids = models.TextField(default="[]")    # ⭐ 收藏清單

    # 🆕 新增：留言清單（存 JSON 格式，例如 [{"user_id":1,"text":"內容"}]）
    comments = models.TextField(default="[]")

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


#-----------------------聊天室資料庫------------------------- 
class ChatRoom(models.Model):
    code = models.CharField(max_length=10, unique=True)  # 對應資料表 code 欄位
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    click_count = models.IntegerField(default=0)
    message_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)    # 對應資料表的 created_at
    updated_at = models.DateTimeField(auto_now=True)        # 對應資料表的 updated_at

    def __str__(self):
        return f"{self.city} {self.district} ({self.code})"
    
    class Meta:
        db_table = 'chat_rooms'




class ChatRoomClick(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="點擊聊天室的使用者（未登入為 NULL）"
    )
    region = models.CharField(max_length=50, help_text="區域名稱")
    click_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'chat_room_clicks'
        verbose_name = "聊天室點擊紀錄"
        verbose_name_plural = "聊天室點擊紀錄"

    def __str__(self):
        return f"{self.region} clicked at {self.click_time}"


class ChatMessage(models.Model):
    user = models.ForeignKey(
        'ThisUserProfile',
        on_delete=models.CASCADE,
        db_column='user_id',
        help_text="留言的使用者"
    )
    region = models.CharField(max_length=50, help_text="區域名稱")
    message = models.TextField()
    nickname = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # ✅ 新增回覆功能
    reply_to = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='replies'
    )

    class Meta:
        db_table = 'chat_messages'

    def __str__(self):
        if self.reply_to:
            return f"{self.nickname or self.user.username} 回覆 {self.reply_to.id}: {self.message[:20]}"
        return f"{self.nickname or self.user.username}: {self.message[:20]}"




class FavoriteChatRoom(models.Model):
    user = models.ForeignKey(
        'ThisUserProfile',
        on_delete=models.CASCADE,
        related_name='favorite_chat_rooms',  # optional: 讓 user.favorite_chat_rooms 可以呼叫
    )
    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='favorited_by_users',  # optional: 讓 chat_room.favorited_by_users 呼叫
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorite_chat_rooms'  # ✅ 建議加上資料表名稱
        unique_together = ('user', 'chat_room')
        verbose_name = "使用者收藏聊天室"
        verbose_name_plural = "使用者收藏聊天室"

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.chat_room}"
    
    # class ChatMessage(models.Model):
#     user = models.ForeignKey(
#         'ThisUserProfile',
#         on_delete=models.CASCADE,
#         db_column='user_id',  # 指定外鍵欄位
#         help_text="留言的使用者"
#     )
#     region = models.CharField(max_length=50, help_text="區域名稱")
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'chat_messages'
#         verbose_name = "聊天室訊息"
#         verbose_name_plural = "聊天室訊息"

#     def __str__(self):
#         return f"{self.user} @ {self.region}: {self.message[:20]}"


# ----------------商家廣告--------------------
from django.db import models

class StoreAd(models.Model):
    st_id = models.IntegerField(primary_key=True)
    ad_content = models.TextField(blank=True, null=True)
    ad_radius = models.IntegerField(default=10)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'store_ad'
        managed = False  # Django 不會建立或修改這張表

