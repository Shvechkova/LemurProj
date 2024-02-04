from rest_framework import routers, serializers, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.client.api.serializers import ClientSerializer, ContractSerializer, ManagerSerializer

from apps.client.models import Client, Contract
from apps.employee.models import Employee

class AddClient(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         obj = serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path=r"manager_list")
    # TODO НИЖНЕЕ ПОДЧЕРКИВАНИЕ и с маленьких букв
    def ManagerList(
        self,
        request,
    ):
        manager = Employee.objects.filter(category_id=1)
        serializer = ManagerSerializer(manager, many=True)
        return Response(serializer.data)


class ContractView(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # def list(self, request):
    #     data=request.data
    #     print(data)
    #     queryset = Contract.objects.filter(client_id=data)
    #     serializer = ContractSerializer(queryset, many=True)
    #     return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_li")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
