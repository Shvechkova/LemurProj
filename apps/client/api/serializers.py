from rest_framework import serializers

from apps.client.models import Client, Contract
from apps.employee.models import Employee



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

    # def create(self, validated_data):
    #     client_name, created = Client.objects.update_or_create(
    #         id=validated_data.get('id', None),
    #         defaults={'client_name': validated_data.get('client_name', None)})
    #     return client_name


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"

    def create(self, data):
        return Contract.objects.create(**data)


# class ClientAddSerializer(serializers.Serializer):
#     client = ClientSerializer(read_only=True, many=True)
#     contract = ContractSerializer(read_only=True, many=True)

#     # class Meta:
#     #     model = Client
#     #     fields = "__all__"
#     # fields = ["id","client_name",]

#     def create(self, data):
#         client_request = data.get("client")
#         print(client_request)
#         # client_request = Client.objects.create(client)

#         # return client
