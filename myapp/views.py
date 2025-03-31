from django.shortcuts import render

def report_view(request):
    return render(request, 'report.html')

def index(request):
    return render(request, 'index.html')  # 確保 index.html 在 templates/ 內

# 另一個首頁版本（index35.html）
def index35(request):
    return render(request, 'index35.html')

# 表格頁面
def tables(request):
    return render(request, 'tables.html')

# 註冊頁面
def register(request):
    return render(request, 'register.html')

# 密碼頁面
def password(request):
    return render(request, 'password.html')

# 登入頁面
def login(request):
    return render(request, 'login.html')

# 布局 - 靜態頁面
def layout_static(request):
    return render(request, 'layout-static.html')

# 布局 - 輕量側邊欄頁面
def layout_sidenav_light(request):
    return render(request, 'layout-sidenav-light.html')

# 圖表頁面
def charts(request):
    return render(request, 'charts.html')

# 500 錯誤頁面
def error_500(request):
    return render(request, '500.html')

# 500 錯誤頁面
def error_401(request):
    return render(request, '401.html')

# 500 錯誤頁面
def error_404(request):
    return render(request, '404.html')


def harassment_prevention(request):
    return render(request, 'harassment_prevention.html')

def education_page(request):
    return render(request, 'education_page.html')

def nearest_police(request):
    return render(request, 'nearest_police.html')

# 新增的匿名聊天頁面
def anonymous_chat(request):
    person_name = request.GET.get('person', '未知人物')  # 獲取 URL 參數中的人物名稱
    return render(request, 'anonymous-chat.html', {'person_name': person_name})

def map_view(request):
    return render(request, 'map.html')


def login_page(request):
    return render(request, '001_login.html')