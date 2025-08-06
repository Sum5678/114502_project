import os
import django
import csv

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import ChatRoom  # 換成你的 app 名稱

def import_csv(filename):
    with open(filename, encoding='utf-8') as f:  # 注意這裡是 utf-8
        reader = csv.DictReader(f)
        print("CSV欄位名稱：", reader.fieldnames)
        count = 0
        for row in reader:
            print("讀取到一列資料:", row)
            code = row['\ufeffid'].strip()  # 直接用帶 BOM 的 key
            city = row['city'].strip()
            district = row['district'].strip()

            ChatRoom.objects.update_or_create(
                code=code,
                defaults={
                    'city': city,
                    'district': district,
                    'click_count': 0,
                    'message_count': 0,
                }
            )
            count += 1
        print(f"成功匯入 {count} 筆資料")
