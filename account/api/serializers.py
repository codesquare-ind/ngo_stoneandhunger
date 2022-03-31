from rest_framework import serializers
from account.models import AccountUser, UserProfile
from projects.models import FamilyMembers


class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = AccountUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = AccountUser(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Your passwords did not match'})

        account.set_password(password)
        account.save()
        return account


class ChangePasswordSerializer(serializers.Serializer):
    model = AccountUser

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMembers
        fields = ['name', 'age', 'monthly_income', 'relation', 'user']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['address', 'city', 'state', 'country', 'pan', 'date_of_birth', 'house_ownership', 'rent_amount', 'gender']

    def create(self, validated_data):
        profile = UserProfile.objects.create(**validated_data)
        return profile
