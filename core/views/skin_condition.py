from rest_framework.viewsets import ModelViewSet

from core.models import SkinCondition
from core.serializers import SkinConditionSerializer


class SkinConditionView(ModelViewSet):
    queryset = SkinCondition.objects.all()
    serializer_class = SkinConditionSerializer
