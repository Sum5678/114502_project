# 使用 Python 官方映像
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴，解決 mysqlclient 編譯問題
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 複製需求檔案並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 複製整個專案程式
COPY . .

# 設定 Cloud Run PORT
ENV PORT=8080

# 啟動 Django
CMD ["gunicorn", "myproject.wsgi:application", "--bind", ":8080"]
