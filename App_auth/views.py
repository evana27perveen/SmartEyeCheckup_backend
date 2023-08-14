from rest_framework import viewsets, permissions, generics
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from App_auth.serializers import *
from rest_framework.generics import CreateAPIView
from rest_framework import renderers
import json


# Create your views here.
class RegisterAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        group = request.data.get('group')  # Get the group from request data
        serializers_ = self.get_serializer(data=request.data, context={"groups": group})
        if serializers_.is_valid():
            user = self.perform_create(serializers_)
            if group == 'PATIENT':
                # Create the profile after the user instance is saved
                PatientProfileModel.objects.create(user=user)
            else:
                # Create the profile after the user instance is saved
                DoctorProfileModel.objects.create(user=user)

            return Response(serializers_.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers_.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save()


def getToken(user):
    refreshToken = RefreshToken.for_user(user)
    return {
        'refresh': str(refreshToken),
        'access': str(refreshToken.access_token)
    }


class UserRendering(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'error': data})
        else:
            response = json.dumps(data)

        return response


class UserLoginView(TokenObtainPairView):
    renderer_classes = [UserRendering]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        if user:
            refreshToken = RefreshToken.for_user(user)
            groups = Group.objects.filter(user=user)
            group_names = [group.name for group in groups][0]
            return Response({
                'refreshToken': str(refreshToken),
                'accessToken': str(refreshToken.access_token),
                'alert': 'Login Success',
                'group': group_names,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"alert": "Failed!"}, status=status.HTTP_404_NOT_FOUND)


class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfileModel.objects.all()
    serializer_class = DoctorProfileModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({"status": "Successfully Created"}, status=201)

    def retrieve(self, request, pk, **kwargs):
        profile = DoctorProfileModel.objects.get(pk=pk)
        serializer = self.serializer_class(profile)
        return Response(serializer.data)

    def update(self, request, pk, **kwargs):
        profile = DoctorProfileModel.objects.get(pk=pk)
        serializer = self.serializer_class(profile, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({"status": "Successfully Updated!"})

    def destroy(self, request, pk, **kwargs):
        profile = DoctorProfileModel.objects.get(pk=pk)
        profile.delete()
        return Response(status=204)

    def patch(self, request, pk, **kwargs):
        profile = DoctorProfileModel.objects.get(pk=pk)
        serializer = self.serializer_class(profile, data=request.data, partial=True,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({"status": "Successfully Updated!"})


class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfileModel.objects.all()
    serializer_class = PatientProfileModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({"status": "Successfully Created"}, status=201)

    def retrieve(self, request, pk, **kwargs):
        profile = PatientProfileModel.objects.get(pk=pk)
        serializer = self.serializer_class(profile)
        return Response(serializer.data)

    def update(self, request, pk, **kwargs):
        profile = PatientProfileModel.objects.get(pk=pk)
        serializer = self.serializer_class(profile, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({"status": "Successfully Updated!"})

    def destroy(self, request, pk, **kwargs):
        profile = PatientProfileModel.objects.get(pk=pk)
        profile.delete()
        return Response(status=204)

    def patch(self, request, pk, **kwargs):
        profile = PatientProfileModel.objects.get(pk=pk)
        serializer = self.serializer_class(profile, data=request.data, partial=True,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({"status": "Successfully Updated!"})


