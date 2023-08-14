from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from APP_main.models import CheckupModel
from APP_main.serializers import CheckupModelSerializer
from App_auth.models import DoctorProfileModel, PatientProfileModel
from App_auth.serializers import DoctorProfileModelSerializer


class UserHomeData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        p_id = 0
        user = request.user
        user_groups = user.groups.all()
        group_names = [group.name for group in user_groups]
        if group_names[0] == 'DOCTOR':
            profile = DoctorProfileModel.objects.get(user=user)
            print(profile)
            p_id = profile.id
        elif group_names[0] == 'PATIENT':
            profile = PatientProfileModel.objects.get(user=user)
            p_id = profile.id
        doctors = DoctorProfileModel.objects.filter(verified=True).count()
        patients = PatientProfileModel.objects.all().count()
        checkups = CheckupModel.objects.all().count()
        return Response({
            "p_id": p_id,
            "doctors": doctors,
            "patients": patients,
            "checkups": checkups
        })


class DoctorData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        doctors = DoctorProfileModel.objects.filter(verified=True)
        serializer = DoctorProfileModelSerializer(doctors, many=True)
        return Response({
            "doctors": serializer.data,  
        })


class CheckupViewSet(viewsets.ModelViewSet):
    queryset = CheckupModel.objects.all()
    serializer_class = CheckupModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "Successfully Created"}, status=201)

    def retrieve(self, request, pk, **kwargs):
        checkup = CheckupModel.objects.get(pk=pk)
        serializer = self.serializer_class(checkup)
        return Response(serializer.data)

    def update(self, request, pk, **kwargs):
        checkup = CheckupModel.objects.get(pk=pk)
        serializer = self.serializer_class(checkup, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "Successfully Updated!"})

    def destroy(self, request, pk, **kwargs):
        checkup = CheckupModel.objects.get(pk=pk)
        checkup.delete()
        return Response(status=204)

    def patch(self, request, pk, **kwargs):
        checkup = CheckupModel.objects.get(pk=pk)
        serializer = self.serializer_class(checkup, data=request.data, partial=True,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "Successfully Updated!"})
