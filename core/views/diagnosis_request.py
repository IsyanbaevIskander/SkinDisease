from rest_framework.viewsets import ModelViewSet

from core.models import DiagnosisRequest
from core.serializers import DiagnosisRequestSerializer


class DiagnosisRequestView(ModelViewSet):
    queryset = DiagnosisRequest.objects.all()
    serializer_class = DiagnosisRequestSerializer
