from django.urls import path
from APP_main.views import *

app_name = 'App_main'

urlpatterns = [
    path('user-home-data/', UserHomeData.as_view(), name='user-home-data'),
    path('doctor-data/', DoctorData.as_view(), name='doctor-data'),
    path('checkup-data/', CheckupData.as_view(), name='checkup-data'),
    path('eye-data/', PatientEyeData.as_view(), name='eye-data'),
    path('upload/', PredictionView.as_view()),
    path('checkups/', CheckupViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('checkups/<int:pk>/', CheckupViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('checkup-update/<int:pk>/mark_as_rejected/', CheckupUpdateViewSet.as_view({'put': 'mark_as_rejected'})),
]
