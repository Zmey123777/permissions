from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import Advertisement

class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)

class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user = self.context["request"].user
        
        # Проверка на количество открытых объявлений
        if data.get('status') == 'OPEN' and Advertisement.objects.filter(creator=user, status='OPEN').count() >= 10:
            raise serializers.ValidationError("У вас не может быть больше 10 открытых объявлений.")
        
        return data