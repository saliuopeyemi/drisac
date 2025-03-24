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
            raise serializers.ValidationError({"error":validity})

    def validate_email(self,value):
        if models.Users.objects.filter(email=value).exists():
            raise serializers.ValidationError({"error":"Email exists"})
        else:
            return value

    def validate(self,data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"error":"Password Mismatch"})
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
