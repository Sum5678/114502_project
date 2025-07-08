import os
import django
from pyproj import Transformer

# 設定 Django 專案名稱 ← 把 YOUR_PROJECT 改成實際名稱（如 114502_project）
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings") 
django.setup()






# 匯入模型 ← 把 yourapp 改成實際 app 名稱（如 myapp）
from myapp.models import PoliceAddress

# 建立轉換器：TWD97 TM2 → WGS84
transformer = Transformer.from_crs("EPSG:3826", "EPSG:4326", always_xy=True)

# 批次轉換並寫入
for p in PoliceAddress.objects.all():
    try:
        x, y = p.POINT_X, p.POINT_Y
        lng, lat = transformer.transform(x, y)

        p.POINT_X = lng  # 經度
        p.POINT_Y = lat  # 緯度
        p.save()

        print(f"✅ {p.precinct_name} → ({lat:.6f}, {lng:.6f})")
    except Exception as e:
        print(f"❌ 錯誤 - {p.precinct_name}: {e}")
