from rest_framework.permissions import BasePermission


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.author
    

class IsAdminOrActivePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_active or request.user.is_staff)