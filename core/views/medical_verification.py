from rest_framework.viewsets import ModelViewSet

from core.models import MedicalVerification
from core.serializers import MedicalVerificationSerializer


class MedicalVerificationView(ModelViewSet):
    queryset = MedicalVerification.objects.all()
    serializer_class = MedicalVerificationSerializer
