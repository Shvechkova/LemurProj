 from django.forms import ValidationError
from rest_framework import routers, serializers, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.client.api.serializers import (

    ClientSerializer, 
    ContractSerializer,
    ManagerSerializer,
)

from apps.client.models import Client, Contract
from apps.employee.models import Employee

# клиент


class AddClient(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["get", "post", "put"]

    # менеджер клиента для заполненного
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/manager_li")
    def client_manager_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Client.objects.filter(id=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # список менеджеров для выбора при заполнении
    @action(detail=False, methods=["get"], url_path=r"manager_list")
    def manager_list(
        self,
        request,
    ):
        manager = Employee.objects.filter(category_id=1)
        serializer = ManagerSerializer(manager, many=True)
        return Response(serializer.data)
    
    
    # кленты по сервисам для страниц service
    @action(detail=False, methods=["get"], url_path=r"client_filter_list")
    def client_filter_list(
        self,
        request,
    ):
        category = request.query_params.get("service")
        queryset = Client.objects.filter(contract__service=category)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


# контракт
class ContractView(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_li")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)
# контрактtesttesttesttesttesttesttesttesttest
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]

class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
class ContractViewtest(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put"]

    # список контрактов клиента
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_litesttest")
    def client_contract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = Contract.objects.filter(client=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # создание контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
    def create_contracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # изменение контрактов

    @action(detail=False, methods=["post", "put"], url_path=r"upd_contracts")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        
        for contracts in data:
            contract_id = contracts["id"]
            if contract_id == "":
                serializer = self.serializer_class(data=contracts)
              
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                

            else:
                contract = Contract.objects.get(pk=contract_id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    # конракты для клиентов по сервисам для страницы Service
    @action(detail=False, methods=["get"], url_path=r"contract_filter_list")
    def contract_filter_list(
        self,
        request,
    ):

        client = request.query_params.get("client")

        category = request.query_params.get("service")
        queryset = Contract.objects.filter(client=client,service=category)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

# class AdditionalContractView(viewsets.ModelViewSet):
#     queryset = AdditionalContract.objects.all()
#     serializer_class = AdditionalContractSerializer
#     http_method_names = ["get", "post", "put"]
