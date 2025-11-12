from rest_framework.viewsets import ModelViewSet

from core.models import DiagnosisResult
from core.serializers import DiagnosisResultSerializer


class DiagnosisResultView(ModelViewSet):
    queryset = DiagnosisResult.objects.all()
    serializer_class = DiagnosisResultSerializer
