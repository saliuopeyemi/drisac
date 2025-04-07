from rest_framework import serializers
from . import models

import uuid
from .Hasher import hasher 

hasher = hasher()


user_type_choices = (
            ("user","user"),
            ("admin","admin")
        )

class CreateNewUserSerializer(serializers.Serializer):
    #username = serializers.CharField(max_length=250)
    email = serializers.CharField(max_length=250)
    first_name = serializers.CharField(max_length=250)
    last_name = serializers.CharField(max_length=250)
    user_type = serializers.ChoiceField(choices=user_type_choices)
    password = serializers.CharField(max_length=200)
    password2 = serializers.CharField(max_length=200)

    def validate_password(self,value):
        validity = hasher.password_validity(value)
        if validity == True:
            return value
        else:
            raise serializers.ValidationError(validity)

    def validate_email(self,value):
        if models.Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Exists.")
        else:
            return value

    def validate(self,data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Password Mismatch")
        else:
            return data

    def create(self,validated_data):
        validated_data.pop("password2")
        validated_data["username"] = uuid.uuid4()
        user = models.Users.objects.create(**validated_data)
        output = {
                    "email": user.email,
                    "user_type": user.user_type
                }
        return output

class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = ["id","email",'user_type','first_name','last_name']

class DeleteUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate(self,data):
        user = self.context["user"]
        user_instance = models.Users.objects.get(id=user.id)
        if user_instance.user_type != "admin":
            raise serializers.ValidationError({"error":"Not Permitted"})
        else:
            if models.Users.objects.filter(id=data["user_id"]).exists():
                return data
            else:
                raise serializers.ValidationError({"error":"Inexistent User"})

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

    def validate(self,data):
        email = data.get("email")
        password = data.get("password")
        if models.Users.objects.filter(email=email).exists():
            if models.Users.objects.get(email=email).password == password:
                user = models.Users.objects.get(email=email)
                return user
            else:
                raise serializers.ValidationError({"error":"Wrong Password"})
        else:
            raise serializers.ValidationError({"error":"Inexistent User"})


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ["id","title","description","unit_price"]

        read_only_fields = ["id"]

    def create(self,validated_data):
        product = models.Product.objects.create(**validated_data)
        output = {
                    "title":product.title,
                    "description":product.description,
                    "unit_price":product.unit_price
                }
        return output

class UpdateProductSerializer(serializers.Serializer):
    #id = serializers.IntegerField()
    title = serializers.CharField(max_length=300,required=False)
    description = serializers.CharField(max_length=2500,required=False)
    unit_price = serializers.IntegerField(required=False)

    def update(self,instance,validated_data):
        instance.title = validated_data.get("title",instance.title)
        instance.description = validated_data.get("description",instance.description)
        instance.unit_price = validated_data.get("unit_price",instance.unit_price)
        instance.save()
        output = {
                    "id":instance.id,
                    "title":instance.title,
                    "description":instance.description,
                    "unit_price":instance.unit_price
                }
        return output

class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expenditure
        fields = ["id","title","description","amount","date"]

        read_only_fields = ["id","date"]

    def create(self,validated_data):
        expenditure = models.Expenditure.objects.create(**validated_data)
        output = {
                    "title":expenditure.title,
                    "description":expenditure.description,
                    "amount":expenditure.amount,
                    "date":expenditure.date
                }
        return output


class SaleSerializer(serializers.ModelSerializer):
    #product = ProductSerializer()
    product = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all())
    class Meta:
        model = models.Sales
        fields = ["id","product","quantity","revenue","date"]

        read_only_fields = ["id","revenue","date"]

    def create(self,validated_data):
        product = validated_data.get("product")
        quantity = validated_data.get("quantity")
        unit_price = models.Product.objects.get(id=product.id).unit_price
        validated_data["revenue"] = quantity * unit_price
        sale = models.Sales.objects.create(**validated_data)
        output = {
                    "product":product.title,
                    "quantity":quantity,
                    "revenue":sale.revenue,
                    "date":sale.date
                }
        return output


class SaleRetrieveSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = models.Sales
        fields = ["id","product","quantity","revenue","date"]


class TotalRevenueSerializer(serializers.Serializer):
    from_date = serializers.DateField()
    to_date = serializers.DateField()
