from functools import partial
import re
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from ..serializers.users import *
from rest_framework.response import Response
import requests
from ..models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


# Create your views here.

client_id = "CJDIuqRSvWi8JQ4OBj42fVl2uixvoCBn3RsTIxGU"
client_secret = "jtQC3YfFONhxEHGDXp1KQAuABosClUbBfKER2fQwNxO7bJ27C9XbepfZ4y7yryjSJSimZz3cwZN9yi3AyIsVh6ynWhgdVRKBGegj48ie44wJ5cLAktBrXDm8bwbgt5Ou"

class UserLoginApiView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid(raise_exception=True):

            url = "http://localhost:8000/auth/token/"
            data = {"username":serializer.validated_data['email'],"password":serializer.validated_data['password'],
                    "grant_type":"password","client_id":client_id,"client_secret":client_secret}
            r = requests.post(url,data)
            return Response(r.json(),status=r.status_code)
        return Response(serializer.errors,status=400)


class RefreshTokenApiView(GenericAPIView):
    serializer_class = RefreshTokenSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            url = "http://localhost:8000/auth/token"

            data = {
                "grant_type":"refresh_token",
                "client_id":client_id,
                "client_secret":client_secret,
                "refresh_token":serializer.validated_data["refresh_token"]
            }
            r = requests.post(url,data)
            return Response(r.json(),status=r.status_code)
        return Response(serializer.errors,status=400)


class UserLogoutApiView(GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            url = "http://localhost:8000/auth/revoke-token"
            data = {
                "client_id":client_id,
                "client_secret":client_secret,
                "token":serializer.validated_data['access_token']
            }
            r = requests.post(url,data)
            if r.status_code==204:
                return Response(status=r.status_code)
            else:
                return Response(r.json(),status=r.status_code)
        return Response(serializer.errors,status=400)


class UserRegisterApiView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = {
                'full_name':serializer.validated_data.get('full_name'),
                'email':serializer.validated_data.get('email'),
                'contact_no':serializer.validated_data.get('contact_no'),
                'password':serializer.validated_data.get('password')
            }
            user = User.objects.create(**data)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data,status=201)
        return Response(serializer.errors,status=400)
    


class MyAccountApiView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyAccountSerializer
    def put(self,request):
        user = request.user
        serializer = self.serializer_class(data=request.data,instance=user,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def get(self,request):
        serializer = self.serializer_class(request.user,many=False)
        
        return Response(serializer.data)



class AddressApiView(GenericAPIView):
    
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = self.serializer_class(request.user.address)
        return Response(serializer.data)
    def put(self,request):
        serializer = self.serializer_class(data=request.data,instance=request.user.address)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)


class ChangePasswordApi(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self,request):
        serializer = self.serializer_class(data=request.data)
        if not check_password(request.data.get('old_password'),request.user.password):
            return Response({"old_password":["old password does not match"]},status=400)

        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data['password']
            request.user.password = password
            request.user.save()
            return Response()

        return Response(serializer.errors,status=400)


class UserApiView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class =  UserSerializer