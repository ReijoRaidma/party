from django.contrib.auth.models import User
from rest_framework import permissions


class ObjectOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
