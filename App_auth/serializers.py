from django.contrib.auth.models import Group
from rest_framework import serializers
from App_auth.models import *
from django.db import transaction


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('password', 'email')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    @transaction.atomic
    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        group_l = self.context.get('groups')
        grp = Group.objects.get_or_create(name=group_l)
        user.save()
        grp[0].user_set.add(user)
        return user


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'groups']


class UserUpdatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class DoctorProfileModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DoctorProfileModel
        fields = '__all__'


class PatientProfileModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PatientProfileModel
        fields = '__all__'
