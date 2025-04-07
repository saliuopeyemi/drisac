from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers, models
from rest_framework import status

from django.http import Http404



class CreateNewUserView(APIView):
    permission_classes = [
                AllowAny,
            ]
    serializer_class = serializers.CreateNewUserSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)


class AllUsers(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.UserRetrieveSerializer

    def get(self,request):
        user_id = request.user.id
        user_type = models.Users.objects.get(id=user_id).user_type
        if user_type == "admin":
            all_users = models.Users.objects.exclude(email=request.user.email)
            data = self.serializer_class(all_users,many=True).data
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response([],status=status.HTTP_200_OK)




class DeleteUserView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.DeleteUserSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            id = serializer.validated_data["user_id"]
            models.Users.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)




class LoginView(APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [
                AllowAny,
            ]

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            token = RefreshToken.for_user(user)
            output = {
                        "access":str(token.access_token),
                        "refresh":str(token),
                        "user":user.email
                    }
            return Response(output,status=status.HTTP_200_OK)


class UserRetrieveView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.UserRetrieveSerializer

    def get(self,request):
        user_id = request.user.id 
        user = models.Users.objects.get(id=user_id)
        data = self.serializer_class(user,many=False).data
        return Response(data,status=status.HTTP_200_OK)



class ProductView(APIView):
    permission_classes=[
                IsAuthenticated,
            ]
    serializer_class = serializers.ProductSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    def get(self,request):
        param = request.query_params.get("product_id",None)
        if not param:
            data = models.Product.objects.all()
            products = serializers.ProductSerializer(data, many=True)
            #print(products.data)
            return Response(products.data,status=status.HTTP_200_OK)
        else:
            try:
                data = models.Product.objects.get(id=param)
                product = serializers.ProductSerializer(data,many=False)
                return Response(product.data,status=status.HTTP_200_OK)

            except:
                raise Http404({"error":"Inexistent Product ID"})

    def delete(self,request):
        param = request.query_params.get("product_id",None)
        if param:
            if models.Product.objects.filter(id=param).exists():
                models.Product.objects.get(id=param).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise Http404({"error":"Inexistent Product ID"})
        else:
            raise Http404({"error":"No query param"})

class UpdateProductView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.UpdateProductSerializer

    def put(self,request,id):
        if models.Product.objects.filter(id=id).exists():
            product = models.Product.objects.get(id=id)
            serializer = self.serializer_class(data=request.data,instance=product)
            if serializer.is_valid(raise_exception=True):
                output = serializer.save()
                return Response(output,status=status.HTTP_202_ACCEPTED)
        else:
            raise Http404({"error":"Inexistent Product ID"})


class ExpenditureView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.ExpenditureSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    def get(self,request):
        params = request.query_params.get("expenditure_id",None)
        if not params:
            expenditures = models.Expenditure.objects.all().order_by("-date")
            data = self.serializer_class(expenditures,many=True).data
            return Response(data,status=status.HTTP_200_OK)
        else:
            try:
                expenditure = models.Expenditure.objects.get(id=params)
                data = self.serializer_class(expenditure,many=False).data
                return Response(data,status=status.HTTP_200_OK)
            except:
                raise Http404({"error":"Inexistent Expenditure ID"})

    def delete(self,request):
        params = request.query_params.get("expenditure_id",None)
        if params:
            try:
                models.Expenditure.objects.get(id=params).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                raise Http404({"error":"Inexistent Expenditure ID"})
        else:
            raise Http404({"error":"No query param"})

class SaleView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.SaleSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    def get(self,request):
        sales = models.Sales.objects.all().order_by("-date")
        output = serializers.SaleRetrieveSerializer(sales,many=True).data
        return Response(output,status=status.HTTP_200_OK)

    def delete(self,request):
        param = request.query_params.get("sale_id")
        if param:
            try:
                models.Sales.objects.get(id=param).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                raise Http404({"error":"Invalid ID"})
        else:
            raise Http404({"error":"Invalid query parameter!"})


class TotalRevenueView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.TotalRevenueSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            start = data["from_date"]
            end = data["to_date"]
            expenditure = models.Expenditure.objects.filter(date__range=[start,end])
            expenditure_data = serializers.ExpenditureSerializer(expenditure,many=True).data
            expense_total = 0
            if len(expenditure_data) != 0:
                for expense in expenditure_data:
                    expense_total += expense["amount"]
            sales = models.Sales.objects.filter(date__range=[start,end])
            output = serializers.SaleSerializer(sales,many=True).data
            revenue = 0
            if len(output) != 0:
                for sale in output:
                    revenue += sale["revenue"]
            financial_status = revenue - expense_total
            if financial_status < 1:
                summary = "Loss"
            else:
                summary = "Profit"
            output = {
                        "total_expense":expense_total,
                        "total_sale":revenue,
                        "financial_status":financial_status,
                        "summary":summary,
                        "start":start,
                        "end":end
                    }
            return Response(output,status=status.HTTP_200_OK)













class Test(APIView):
    permission_classes = [
                IsAuthenticated,
            ]

    def get(self,request):
        return Response("Installed successfully", status=status.HTTP_200_OK)
