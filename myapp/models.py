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
#-------------------------------------------------------------------------
class TaiwanRegion(models.Model):
    id = models.AutoField(primary_key=True)
    country_city = models.CharField(max_length=50)
    district_town = models.CharField(max_length=50)

    class Meta:
        db_table = "taiwan_regions"  # 告訴 Django 使用你自己的資料表名
        managed = False  # 不讓 Django 嘗試自己建立這個資料表

    def __str__(self):
        return f"{self.country_city} - {self.district_town}"