import json

from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from doctor.constants import LANGUAGES
from doctor.exceptions import UserCredentialWrongError
from doctor.models import Doctor, SpokenLanguages, Patients


class DoctorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    profile_picture = serializers.ImageField(required=False)
    languages = serializers.CharField()

    class Meta:
        model = Doctor
        fields = "__all__"

    def validate(self, attrs):
        languages = [language.strip() for language in attrs.get('languages', '').split(',')]
        for language in languages:
            if language and language not in LANGUAGES:
                raise serializers.ValidationError("Please select the proper language.")
        return attrs

    def create(self, validated_data):
        languages = [language.strip() for language in validated_data.pop('languages').split(',')]
        doctor = Doctor.objects.create_user(**validated_data)
        for language in languages:
            SpokenLanguages.objects.create(doctor=doctor, language=language)
        return doctor

    def update(self, instance, validated_data):
        languages = [language.strip() for language in validated_data.pop('languages', '').split(',')]
        Doctor.objects.filter(pk=instance.id).update(**validated_data)
        for language in languages:
            SpokenLanguages.objects.get_or_create(doctor=instance, language=language)
        return Doctor.objects.get(pk=instance.id)


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            self.user = Doctor.objects.get(
                email__iexact=authenticate_kwargs['email']
            )
        except Doctor.DoesNotExist as e:
            raise UserCredentialWrongError() from e

        if not self.user.check_password(authenticate_kwargs["password"]):
            raise UserCredentialWrongError()

        refresh = self.get_token(self.user)

        data = {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
            'email': self.user.email,
            'id': self.user.id
        }

        self.user.last_login = timezone.now()
        self.user.save()
        return data


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguages
        fields = ['language']


class PatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = "__all__"

    def validate(self, attrs):
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        email = attrs.get('email', '')
        date_of_birth = attrs.get('date_of_birth', '')

        if not first_name:
            raise serializers.ValidationError("First Name is required")

        if not last_name:
            raise serializers.ValidationError("Last Name is required")

        if not email:
            raise serializers.ValidationError("Email is required")

        if not date_of_birth:
            raise serializers.ValidationError("Date of birth is required")

        return attrs
