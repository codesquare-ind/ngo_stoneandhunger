from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import CaseSerializer, EducationalCaseSerializer, ProvisionalSerializer, MedicineCaseSerializer, MedicalCaseSerializer, GeneralSerializer, CasePolymorphicSerializer, DonationSerializer
from projects.models import Case, ProjectDonation


@api_view(['GET'],)
@authentication_classes([])
@permission_classes([])
def view_case(request, uuid):
    case = Case.objects.get_subclass(uuid=uuid)
    serializer = CasePolymorphicSerializer(case, many=False)
    return Response(serializer.data)


@api_view(['GET'],)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_my_cases(request):
    cases = Case.objects.filter(created_by__user=request.user).select_subclasses()
    serializer = CasePolymorphicSerializer(cases, many=True)
    return Response(serializer.data)


@api_view(['GET'],)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_my_donations(request):
    cases = ProjectDonation.objects.filter(donor=request.user)
    serializer = DonationSerializer(cases, many=True)
    return Response(serializer.data)


@api_view(['GET'],)
@authentication_classes([])
@permission_classes([])
def get_all_active_case(request):
    category = request.GET.get('category', None)
    cases = Case.objects.filter(status='Green').select_subclasses()

    if category:
        cases = cases.filter(type=category)

    serializer = CasePolymorphicSerializer(cases, many=True)
    return Response(serializer.data)


@api_view(['POST'],)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_case(request):
    if request.method == 'POST':
        cat = request.GET.get('category')
        context = {}

        if cat == 'Provisional':
            serializer = ProvisionalSerializer(data=request.data)
        elif cat == 'General':
            serializer = GeneralSerializer(data=request.data)
        elif cat == 'Medicine':
            serializer = MedicineCaseSerializer(data=request.data)
        elif cat == 'Educational':
            serializer = EducationalCaseSerializer(data=request.data)
        elif cat == 'Medical':
            serializer = MedicalCaseSerializer(data=request.data)
        else:
            context['message'] = 'invalid category'
            serializer = None

        if serializer.is_valid():
            case = serializer.save()
            case.created_by = request.user.userprofile_set.first()
            case.save()
            context['message'] = "case created successfully"
        else:
            context = serializer.errors

        return Response(context)


@api_view(['POST'],)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def approve_case(request, uuid):
    case = Case.objects.get(uuid=uuid)
    if request.method == 'POST':
        case.status = 'Green'
        case.verified_by = request.user
        case.save()
        context = {'message': 'case has been approved'}
        return Response(context)