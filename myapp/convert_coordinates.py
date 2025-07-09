# convert_coordinates.py
import os
import django
from pyproj import Transformer

# 設定 Django 專案設定模組
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project114502.settings")
django.setup()

# 匯入你的模型
from myapp.models import PoliceAddress

# 建立 TWD97 TM2 → WGS84 經緯度轉換器
transformer = Transformer.from_crs("EPSG:3826", "EPSG:4326", always_xy=True)

# 批次轉換警局座標
for p in PoliceAddress.objects.all():
    try:
        x, y = p.POINT_X, p.POINT_Y
        lng, lat = transformer.transform(x, y)

        # 更新資料
        p.POINT_X = lng
        p.POINT_Y = lat
        p.save()

        print(f"✅ 已轉換 {p.precinct_name}: ({lat:.6f}, {lng:.6f})")
    except Exception as e:
        print(f"❌ 錯誤 - {p.precinct_name}: {e}")
