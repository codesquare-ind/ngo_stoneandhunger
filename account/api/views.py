from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import UserRegistrationSerializer, ChangePasswordSerializer, ProfileSerializer, FamilySerializer
from rest_framework.authtoken.models import Token
from account.models import UserProfile
from projects.api.serializers import DonationSerializer
from projects.models import ProjectDonation


@api_view(['POST'],)
@authentication_classes([])
@permission_classes([])
def user_registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        context = {}
        if serializer.is_valid():
            account = serializer.save()
            context['response'] = 'user registration successful'
            context['email'] = account.email
            context['first_name'] = account.first_name
            context['last_name'] = account.last_name
            context['phone_number'] = account.phone_number
            token = Token.objects.get(user=account).key
            context['token'] = token
        else:
            context = serializer.errors

        return Response(context)


@api_view(['POST'],)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request, *args, **kwargs):
    serializer = ChangePasswordSerializer(data=request.data)

    if serializer.is_valid():
        # Check old password
        if not request.user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        # set_password also hashes the password that the user will get
        request.user.set_password(serializer.data.get("new_password"))
        request.user.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }

        return Response(response)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'],)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def complete_profile(request):
    if request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        context = {}
        if serializer.is_valid():
            profile = serializer.save()
            profile.user = request.user
            profile.save()
            context['message'] = "Profile created successfully"
        else:
            context = serializer.errors

        return Response(context)


@api_view(['GET'],)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_profile(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    family_members = profile.familymembers_set.all()
    serialized_family = FamilySerializer(family_members, many=True)
    cases = ProjectDonation.objects.filter(donor=request.user)
    serializer = DonationSerializer(cases, many=True)

    context = {
        'name': f'{request.user.first_name} {request.user.last_name}',
        'email': request.user.email,
        'phone_number': request.user.phone_number,
        'address': profile.address,
        'city': profile.city,
        'country': profile.country,
        'date_of_birth': profile.date_of_birth,
        'house_ownership': profile.house_ownership,
        'rent_amount': profile.rent_amount,
        'gender': profile.gender,
        'family_members': serialized_family.data,
        'donations': serializer.data
    }
    return Response(context)
