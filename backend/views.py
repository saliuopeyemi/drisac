from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers, models
from rest_framework import status



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




class DeleteUserView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.DeleteUserSerializer

    def delete(self,request):
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















class Test(APIView):
    permission_classes = [
                IsAuthenticated,
            ]

    def get(self,request):
        return Response("Installed successfully", status=status.HTTP_200_OK)
