# serializers.py
from rest_framework import serializers
from .models import PemapWithSubkind

class PemapWithSubkindSerializer(serializers.ModelSerializer):
    class Meta:
        model = PemapWithSubkind
        fields = ['p_id', 'display_name', 'kind', 'subkind', 'latitude', 'longitude', 'address', 'img_url', 'time_created']
