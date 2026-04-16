from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Habit


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
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
