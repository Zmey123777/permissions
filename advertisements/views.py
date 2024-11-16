from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.filters import AdvertisementFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.exceptions import PermissionDenied

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def perform_update(self, serializer):
        """Переопределение метода обновления."""
        advertisement = self.get_object()
        if advertisement.creator != self.request.user:
            raise PermissionDenied("Вы не можете обновить это объявление.")
        serializer.save()

    def perform_destroy(self, instance):
        """Переопределение метода удаления."""
        if instance.creator != self.request.user:
            raise PermissionDenied("Вы не можете удалить это объявление.")
        instance.delete()
