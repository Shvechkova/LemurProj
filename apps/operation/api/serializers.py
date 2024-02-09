from rest_framework import serializers

from apps.operation.models import OperationEntry


class OperationEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationEntry
        fields = "__all__"