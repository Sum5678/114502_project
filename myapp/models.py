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
    total_paid = models.IntegerField(default=0)           # 累積付費金額
    membership_level = models.IntegerField(default=0)     # 會員等級 0~5

    class Meta:
        db_table = 'this_user_profile'

    def __str__(self):
        return self.username

    def membership_name(self):
        """回傳會員名稱對應等級"""
        level_names = {
            0: '普通',
            1: '銅牌',
            2: '銀牌',
            3: '金牌',
            4: '白金',
            5: '鑽石'
        }
        return level_names.get(self.membership_level, '普通')






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
        help_text="留言的使用者"
    )
    # ✅ 保持使用 region 欄位，與你的資料庫表一致
    region = models.CharField(max_length=50, help_text="區域名稱") 
    message = models.TextField()
    nickname = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    reply_to = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='replies'
    )
    # ✅ 由於你的資料庫沒有這些欄位，我們在模型中也不定義。
    # reply_to_text = models.TextField(null=True, blank=True)
    # reply_to_id = models.IntegerField(null=True, blank=True)

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
    


# ----------------商家廣告--------------------

class StoreAll(models.Model):
    st_id = models.AutoField(primary_key=True)
    poster_id = models.IntegerField(blank=True, null=True)
    store_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    business_hours = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    review_status = models.CharField(max_length=50, default='unreviewed')
    admin_id = models.IntegerField()
    user_id = models.IntegerField()
    poster_gmail = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  # 已經有 SQL 建表
        db_table = 'store_all'


class StoreAd(models.Model):
    st = models.OneToOneField(
        StoreAll,
        on_delete=models.CASCADE,
        db_column='st_id',
        primary_key=True,
        related_name='ad'
    )
    ad_content = models.TextField(blank=True, null=True)
    ad_radius = models.IntegerField(default=10)
    enabled = models.BooleanField(default=True)
    
    STATUS_CHOICES = [
        ('pending', '待審核'),
        ('approved', '已批准'),
        ('rejected', '已拒絕'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'store_ad'


class StoreAdImage(models.Model):
    img_id = models.AutoField(primary_key=True)
    st = models.ForeignKey(StoreAd, on_delete=models.CASCADE, db_column="st_id", related_name="images")
    image_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "store_ad_image"
        managed = False


# ----------------商家廣告歷史--------------------
class StoreAdHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    st = models.ForeignKey(StoreAll, on_delete=models.CASCADE, related_name='ad_histories')
    ad_content = models.TextField(blank=True, null=True)
    ad_radius = models.IntegerField(default=10)
    enabled = models.BooleanField(default=True)
    
    STATUS_CHOICES = [
        ('pending', '待審核'),
        ('approved', '已批准'),
        ('rejected', '已拒絕'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    admin_id = models.IntegerField(blank=True, null=True)

    # ✅ 新增付款外鍵
    payment = models.ForeignKey(
        'UserPayment',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='ad_histories'
    )

    class Meta:
        db_table = "store_ad_history"
        managed = False  # 如果你已經用 SQL 建表，可以保持 False



class StoreAdHistoryImage(models.Model):
    img_id = models.AutoField(primary_key=True)
    history = models.ForeignKey(StoreAdHistory, on_delete=models.CASCADE, db_column="history_id", related_name="images")
    image_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "store_ad_history_image"
        managed = False






# myapp/models.py
from django.db import models
from django.conf import settings

class AbuseReport(models.Model):
    """
    交流區檢舉單。
    - target_type：被檢舉的是 貼文/留言/回覆
    - post：對應的貼文（若 target 是留言/回覆，一樣會指向其所屬貼文）
    - comment_id / reply_id：前端留言樹用的識別字串（可為空）
    - reason：檢舉理由（提供常見選項，保留 other）
    - details：檢舉人補充說明
    - snapshot_text：當下被檢舉內容的快照（避免後續被修改而查不到）
    - reporter：檢舉人（可為匿名 -> null）
    - status：審核狀態（待審/已處置/已駁回）
    - admin / admin_note / decided_at：處理者、備註與處理時間（admin 連到 Admins.admin_id）
    """

    # === 枚舉 ===
    class TargetType(models.TextChoices):
        POST    = "post", "貼文"
        COMMENT = "comment", "留言"
        REPLY   = "reply", "回覆"

    class Status(models.TextChoices):
        PENDING      = "pending", "待審"
        ACTION_TAKEN = "action_taken", "已處置"
        REJECTED     = "rejected", "已駁回"

    class Reason(models.TextChoices):
        SPAM       = "spam", "垃圾訊息/廣告"
        ABUSE      = "abuse", "辱罵/騷擾"
        HATE       = "hate", "仇恨/歧視"
        VIOLENCE   = "violence", "暴力/威脅"
        NUDITY     = "nudity", "裸露/色情"
        ILLEGAL    = "illegal", "違法內容"
        DOXXING    = "doxxing", "人身資訊外流"
        MISINFO    = "misinfo", "錯誤資訊"
        OTHER      = "other", "其他"

    # === 關聯/主欄位 ===
    target_type = models.CharField(
        max_length=20,
        choices=TargetType.choices,
        db_index=True,
    )
    # ⬇️ 若你的貼文模型不是 ChatInteraction，請改成正確的模型名稱字串
    post = models.ForeignKey(
        "ChatInteraction",
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="abuse_reports",
    )
    comment_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    reply_id   = models.CharField(max_length=64, blank=True, default="", db_index=True)

    reason        = models.CharField(
        max_length=32,
        choices=Reason.choices,
        default=Reason.OTHER,
        db_index=True,
    )
    details       = models.TextField(blank=True, default="")
    snapshot_text = models.TextField(blank=True, default="")

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="reports_made",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    # ★ 連到 Admins，沿用資料庫欄位 admin_id
    admin = models.ForeignKey(
        "Admins",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column="admin_id",
        related_name="reports_handled",
    )

    admin_note = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    # === 顯示與索引 ===
    def __str__(self):
        return f"[{self.get_target_type_display()}] #{self.pk} - {self.reason}"

    class Meta:
        managed = False                      # ✅ 不讓 Django 建表/改表
        db_table = "myapp_abusereport"             # ✅ 資料庫實際表名
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["reason"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["comment_id"]),
            models.Index(fields=["reply_id"]),
        ]
        verbose_name = "檢舉"
        verbose_name_plural = "檢舉"
        
        
        

# myapp/models.py
from django.db import models
from django.conf import settings

class Notification(models.Model):
    class Type(models.TextChoices):
        REPORT = 'report', '檢舉'
        SYSTEM = 'system', '系統'
        LIKE = 'like', '按讚'
        COMMENT = 'comment', '留言'

    # 接收者
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    # 通知類型
    ntype = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.SYSTEM
    )

    # 通知標題（主文）
    title = models.CharField(max_length=120)

    # 通知訊息（補充內容，可空）
    message = models.TextField(blank=True)

    # 點通知要去的頁面（可空）
    link_url = models.CharField(max_length=300, blank=True)

    # 是否已讀
    is_read = models.BooleanField(default=False)

    # 建立時間
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['recipient', '-created_at']),
        ]

    def __str__(self):
        return f"{self.title} -> {self.recipient}"


# -------使用者付費--------
class UserPayment(models.Model):
    """付款紀錄表"""
    user = models.ForeignKey(
        ThisUserProfile,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='payments'
    )
    amount = models.IntegerField()
    item = models.CharField(max_length=100, default="未知品項")  # 新增品項欄位
    is_used = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_refunded = models.BooleanField(default=False)  # 是否已退款
    refunded_at = models.DateTimeField(null=True, blank=True)  # 退款時間
    st_id = models.IntegerField(null=True, blank=True) 

    class Meta:
        db_table = 'user_payments'

    def __str__(self):
        return f"{self.user.username} - {self.amount} 元 - {self.item} - {self.transaction_id}"


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
