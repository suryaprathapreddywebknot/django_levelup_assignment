from rest_framework import permissions

class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.role == 'admin'
