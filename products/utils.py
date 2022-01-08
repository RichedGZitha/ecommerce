from rest_framework.permissions import BasePermission


# check if user is manager permission.
class IsManager(BasePermission):
    def has_permission(self, request, view):
        print(request.user.groups.filter(name = 'Manager'))
        return request.user.groups.filter(name = 'Manager').exists() or request.user.is_superuser

# check if user is merchant permission.
class IsMerchant(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name = 'Merchant').exists() or request.user.is_superuser