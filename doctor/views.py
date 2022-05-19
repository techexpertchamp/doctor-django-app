from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from doctor.models import Doctor, Patients
from doctor.serializers import LoginSerializer, DoctorSerializer, PatientsSerializer


@api_view(['GET'])
def status_check(request):
    return JsonResponse({"message": "Ok"})


class RegisterDoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = Doctor.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDoctorViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DoctorSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = Doctor.objects.all()

    def retrieve(self, request, pk=None, *args, **kwargs):
        return super(RetrieveUpdateDoctorViewSet, self).retrieve(request=request, pk=pk)

    def partial_update(self, request, pk=None, *args, **kwargs):
        super(RetrieveUpdateDoctorViewSet, self).partial_update(request=request, pk=pk)
        return self.retrieve(request, pk)


class LoginViewSet(TokenObtainPairView):
    serializer_class = LoginSerializer


class AppointmentsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PatientsSerializer

    def create(self, request, *args, **kwargs):
        request.data['doctor'] = request.user.id
        serializer = PatientsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        patients = Patients.objects.filter(doctor=request.user)
        serializer = PatientsSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
