from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from APP_main.models import CheckupModel
from APP_main.serializers import CheckupModelSerializer
from App_auth.models import DoctorProfileModel, PatientProfileModel
from App_auth.serializers import DoctorProfileModelSerializer

from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np


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


class PredictionView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        # Load the model
        model = load_model("APP_main/keras_Model.h5", compile=False)

        # Load the labels
        class_names = open("APP_main/labels.txt", "r").readlines()

        image = request.FILES.get('image')
        # Open the image and preprocess it
        image = Image.open(image).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        # Predict using the model
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Construct the response data
        response_data = {
            "class": class_name[2:],
            "confidence_score": float(confidence_score)
        }

        return Response(response_data)


class CheckupData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = PatientProfileModel.objects.get(user=user)
        checkups = CheckupModel.objects.filter(patient=profile)
        serializer = CheckupModelSerializer(checkups, many=True)
        return Response({
            "checkups": serializer.data,
        })


class PatientEyeData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = DoctorProfileModel.objects.get(user=user)
        checkups = CheckupModel.objects.filter(assigned_doctor=profile)
        serializer = CheckupModelSerializer(checkups, many=True)
        data = []
        for checkup in serializer.data:
            checkup['eye_vision'] = request.build_absolute_uri(checkup['eye_vision'])
            data.append(checkup)
        return Response({"checkups": data})
