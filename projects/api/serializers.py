from rest_framework import serializers
from projects.models import Case, EducationalCase, MedicalCase, MedicineCase, ProvisionalCase, GeneralCase, ProjectDonation
from rest_polymorphic.serializers import PolymorphicSerializer


class CaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        fields = '__all__'
        extra_kwargs = {
            'uuid': {'read_only': True},
            'verified_by': {'read_only': True},
            'status': {'read_only': True}
        }


class EducationalCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalCase
        fields = '__all__'


class MedicalCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCase
        fields = '__all__'


class MedicineCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCase
        fields = '__all__'


class ProvisionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvisionalCase
        fields = '__all__'


class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralCase
        fields = '__all__'


class CasePolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Case: CaseSerializer,
        EducationalCase: EducationalCaseSerializer,
        ProvisionalCase: ProvisionalSerializer,
        MedicalCase: MedicalCaseSerializer,
        MedicineCase: MedicineCaseSerializer,
        GeneralCase: GeneralSerializer
    }


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDonation
        exclude = ['donor']
        depth = 1