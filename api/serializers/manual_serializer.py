from rest_framework import serializers
from api.models import Manual

class ManualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manual
        fields = ['id', 'title', 'file', 'uploaded_at', 'result']
