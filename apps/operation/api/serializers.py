from rest_framework import serializers

from apps.operation.models import OperationEntry, OperationOut


class OperationEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationEntry
        fields = "__all__"
        
        
class OperationOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationOut
        fields = "__all__"        