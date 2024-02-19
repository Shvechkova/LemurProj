from rest_framework import serializers

from apps.operation.models import Operation, OperationEntry, OperationOut


class OperationEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationEntry
        fields = "__all__"
        
        
class OperationOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationOut
        fields = "__all__"    
        
class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = "__all__"               