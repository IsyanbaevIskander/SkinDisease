from rest_framework.viewsets import ModelViewSet

from core.models import DiagnosisRequest, DiagnosisResult, SkinCondition
from core.serializers import DiagnosisRequestSerializer
from predictor import predict_skin_disease


class DiagnosisRequestView(ModelViewSet):
    queryset = DiagnosisRequest.objects.all()
    serializer_class = DiagnosisRequestSerializer

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not hasattr(user, 'role'):
            return qs.none()
        if user.role == 'patient':
            return qs.filter(user=user)

        if user.role == 'dermatologist':
            return qs

        return qs.none()

    def perform_create(self, serializer):
        # Создаём запрос
        request_obj = serializer.save(user=self.request.user)

        # Выполняем прогноз модели
        class_id, confidence = predict_skin_disease(request_obj.image.path)

        # Находим заболевание по коду
        condition = SkinCondition.objects.filter(id=class_id).first()

        # Создаем результат диагностики
        DiagnosisResult.objects.create(request=request_obj, condition=condition, confidence=confidence)
