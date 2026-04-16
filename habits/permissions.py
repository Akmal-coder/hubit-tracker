from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить чтение любым авторизованным
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Редактировать/удалять может только владелец
        return obj.user == request.user
