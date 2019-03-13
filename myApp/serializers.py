from rest_framework import serializers
from myApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, )

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryByUser
        fields = '__all__'


class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = '__all__'
