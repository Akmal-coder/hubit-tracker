from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        # Дополнительная валидация на уровне сериализатора
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError('Нельзя одновременно указывать вознаграждение и связанную привычку')

        if data.get('duration', 0) > 120:
            raise serializers.ValidationError('Время выполнения не должно превышать 120 секунд')

        if data.get('related_habit') and not data.get('related_habit').is_pleasant:
            raise serializers.ValidationError('Связанная привычка должна быть приятной')

        if data.get('is_pleasant'):
            if data.get('reward'):
                raise serializers.ValidationError('У приятной привычки не может быть вознаграждения')
            if data.get('related_habit'):
                raise serializers.ValidationError('У приятной привычки не может быть связанной привычки')

        periodicity = data.get('periodicity', 1)
        if periodicity < 1 or periodicity > 7:
            raise serializers.ValidationError('Периодичность должна быть от 1 до 7 дней')

        return data
