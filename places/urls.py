from django.urls import path, include
from .views import *


urlpatterns = [
   path('users/', UserGenericView.as_view(), name='user-list'),
   path('users/<int:pk>', UserDetailView.as_view(), name = 'user-details'),
   path('signin/', SignIn.as_view(), name='sign-in'),
   # path('jwtsignin/', JwtSignIn.as_view(), name='jwt-sign-in'),
   path('signout/', SignOut.as_view(),name='sign-out'),
   path('country/', CountryListView.as_view(), name='country-list'),
   path('country/<uuid:pk>/', CountryDetailView.as_view(), name = 'country-details'),
   path('state/', StateListView.as_view(), name='state-list'),
   path('state/<uuid:pk>/', StateDetailView.as_view(), name = 'state-details'),
   path('city/', CityListView.as_view(), name='city-list'),
   path('city/<uuid:pk>/', CityDetailView.as_view(), name = 'city-details'),
   path('send-email', SendEmailNotificationView.as_view())
]