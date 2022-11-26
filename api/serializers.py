from rest_framework import serializers
from api.models import *

class PatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patients
        fields="__all__"

class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctors
        exclude=("password",)

class NursesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Nurses
        exclude=("password",)

class PharmacistsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pharmacists
        exclude=("password",)

class AdmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Admissions
        fields="__all__"

class MedicalRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model=MedicalRecords
        fields="__all__"

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payments
        fields="__all__"