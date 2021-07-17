from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, IsAdminUser
from .models import User

class OwnerPermission(BasePermission):
    message = 'Only owner can post, patch or delete.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user

class CartOwnerPermission(BasePermission):
    message = 'Only owner can use this cart item.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsSupplierPermission(BasePermission):
    message = 'This request only for suppliers.'

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_supplier

class IsClientPermission(BasePermission):
    message = 'Only clients can use this request'

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or not request.user.is_supplier

class ClientPermission(BasePermission):
    message = 'Only clients can use this request'

    def has_permission(self, request, view):
        return  not request.user.is_supplier

class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin