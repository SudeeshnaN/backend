from django.shortcuts import render
from django.views import View
from rest_framework import generics
from django.contrib.auth import get_user_model, logout
from .serializers import UserSerializer, CountrySerializer, StateSerializer, CitySerializer
from rest_framework import permissions, authentication
from rest_framework.pagination import CursorPagination
from .models import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import TokenAuthentication
import requests
import yagmail


class CustomCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-date_joined' 

class UserGenericView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    pagination_class = CustomCursorPagination
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

# Using Token Authentication
class SignIn(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(SignIn, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data, 'message': 'Successfully logged in'})

class SignOut(APIView):
    # permission_classes =[permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
           Token.objects.get(key=token)
           logout(self.request)
           return Response({'message': 'Successfully logged out'})
        else:
           return Response({'message': 'Unauthorized user'})


class CountryListView(generics.ListCreateAPIView):
    serializer_class = CountrySerializer
    # permission_classes=[permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Country.objects.filter(my_user__email=self.request.user.username)
    

class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return Country.objects.filter(my_user__email=self.request.user.username)
    
    # def retrieve(self, request, *args, **kwargs):
    #     serializer = self.serializer_class
    #     return Response(serializer.data)
    


class StateListView(generics.ListCreateAPIView):
    serializer_class = StateSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes=[permissions.IsAuthenticated]

    
    def get_queryset(self):
        return State.objects.filter(country__my_user=self.request.user)
    


class StateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StateSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        return State.objects.filter(country__my_user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class
        return Response(serializer.data)



class CityListView(generics.ListCreateAPIView):
    serializer_class = CitySerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes=[permissions.IsAuthenticated]

    
    def get_queryset(self):
        return City.objects.filter(state__country__my_user=self.request.user)
    


class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CitySerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return City.objects.filter(state__country__my_user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class
        return Response(serializer.data)
    
class SendEmailNotificationView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        yag = yagmail.SMTP("support@altiushub.com", "Moc69237")
        yag.send(to="sudeeshna.r@altiushub.com", subject="Subject", contents="Message")