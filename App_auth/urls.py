from django.urls import path
from App_auth.views import *

app_name = 'App_auth'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="registration"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('doctor-profiles/', DoctorProfileViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('doctor-profiles/<int:pk>/',
         DoctorProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('patient-profiles/', PatientProfileViewSet.as_view({'get': 'retrieve', 'post': 'create'})),
    path('patient-profiles/<int:pk>/',
         PatientProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
