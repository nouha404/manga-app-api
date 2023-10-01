from rest_framework import permissions


class NoCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS']
