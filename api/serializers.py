from rest_framework_mongoengine import serializers
from api.models import *

class AdministratorsSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Administrators
        exclude=("password",)

class DoctorsSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Doctors
        exclude=("password",)

class NursesSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Nurses
        exclude=("password",)

class PharmacistsSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Pharmacists
        exclude=("password",)

class PatientsSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Patients
        fields="__all__"

class AdmissionsSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Admissions
        fields="__all__"

class MedicalRecordsSerializer(serializers.DocumentSerializer):
    class Meta:
        model=MedicalRecords
        fields="__all__"

class PaymentsSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Payments
        fields="__all__"