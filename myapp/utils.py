# -------- utils.py--------
from django.db.models import Q
from myapp.models import PemapAll, StoreAll, AbuseReport

def get_unreviewed_counts():
    """回傳事件、商家、交流區的未審核數量"""
    unreviewed_events_count = PemapAll.objects.filter(
        Q(review_status="待審核") |
        Q(review_status="描述內容過短，不足以判斷") |
        Q(review_status="需再由人工審核") |
        Q(review_status="未審核") |
        Q(review_status="AI 審核未通過，需人工審核")
    ).count()

    unreviewed_stores_count = StoreAll.objects.filter(review_status="pending").count()
    unreviewed_review_count = AbuseReport.objects.filter(status="pending").count()

    return {
        'unreviewed_events_count': unreviewed_events_count,
        'unreviewed_stores_count': unreviewed_stores_count,
        'unreviewed_review_count': unreviewed_review_count,
    }
