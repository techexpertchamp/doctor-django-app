from django.urls import path

from doctor.views import status_check, LoginViewSet, RetrieveUpdateDoctorViewSet, RegisterDoctorViewSet, \
    AppointmentsViewSet

urlpatterns = [
    path('', status_check, name='status_check'),
    path('register/', RegisterDoctorViewSet.as_view({"post": "create"}), name='register'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('doctor/<int:pk>/', RetrieveUpdateDoctorViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
    path('doctor/appointment/', AppointmentsViewSet.as_view({'post': 'create', 'get': 'list'}), name='appointment')
]
