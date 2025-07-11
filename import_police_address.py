import pandas as pd
import mysql.connector
from pyproj import Transformer

# 讀取 ODS 檔案（用 odf 引擎）
df = pd.read_excel(r"C:\Users\lipin\114502_project\文件\1140614-各警察(分)局分駐(派出)所地址電話經緯度資料.ods", engine="odf")


# 初始化 TWD97 TM2 → WGS84 轉換器
transformer = Transformer.from_crs("EPSG:3826", "EPSG:4326", always_xy=True)

# 將 POINT_X, POINT_Y 轉換成經緯度（WGS84）
def convert_coords(row):
    x, y = row['POINT_X'], row['POINT_Y']
    if pd.notnull(x) and pd.notnull(y):
        lon, lat = transformer.transform(x, y)
        return pd.Series([lon, lat])
    else:
        return pd.Series([None, None])

df[['POINT_X', 'POINT_Y']] = df.apply(convert_coords, axis=1)

# 連線到 MySQL（請修改帳號密碼資料庫）
conn = mysql.connector.connect(
    host='140.131.114.242',
    user='114502',
    password='114502Data@',
    database='114-502Data'
)
cursor = conn.cursor()


# 匯入資料到 `Police Address` 表
for index, row in df.iterrows():
    sql = """
    INSERT INTO `Police Address` (precinct_name, zipcode, address, phone, POINT_X, POINT_Y)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = (
        row['中文單位名稱'],
        str(row['郵遞區號']),
        row['地址'],
        row['電話'],
        float(row['POINT_X']) if pd.notnull(row['POINT_X']) else None,
        float(row['POINT_Y']) if pd.notnull(row['POINT_Y']) else None
    )
    cursor.execute(sql, data)

conn.commit()
cursor.close()
conn.close()

print("✅ 成功轉換並匯入 Police Address 表格！")
