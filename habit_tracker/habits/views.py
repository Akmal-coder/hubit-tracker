from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Habit
from .permissions import IsOwnerOrReadOnly
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
