from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import PemapAll
from django.utils import timezone
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

@admin.register(PemapAll)
class PemapAllAdmin(admin.ModelAdmin):
    list_display = ('p_id', 'poster_id', 'display_name', 'kind', 'review_status', 'time_reviewed')
    list_filter = ('review_status',)
    change_list_template = "admin/admin999pemap.html"  # 指定自訂模板

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:p_id>/<int:stage>/', self.admin_site.admin_view(self.process_approval), name='pemap_approve'),
        ]
        return custom_urls + urls

    def process_approval(self, request, p_id, stage):
        # stage: 1 or 2，代表第一次或第二次審核
        obj = get_object_or_404(PemapAll, p_id=p_id)
        if stage == 1 and obj.review_status == 0:
            obj.review_status = 1
            obj.time_reviewed = timezone.now()
            obj.save()
            self.message_user(request, f"第一次審核通過: {obj}", messages.SUCCESS)
        elif stage == 2 and obj.review_status == 1:
            obj.review_status = 2
            obj.time_reviewed = timezone.now()
            obj.save()
            self.message_user(request, f"第二次審核通過: {obj}", messages.SUCCESS)
        else:
            self.message_user(request, "審核狀態不符，無法審核", messages.ERROR)
        return redirect(request.META.get('HTTP_REFERER', '/admin/'))

