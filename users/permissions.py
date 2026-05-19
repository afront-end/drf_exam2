from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'seller'

class IsStorekeeper(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'storekeeper'

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'

class IsApprovedCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role == 'customer' and 
                request.user.is_approved)
    
class IsAdminOrSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                (request.user.role == 'admin' or request.user.role == 'seller'))
    
class IsAdminOrStorekeeper(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                (request.user.role == 'admin' or request.user.role == 'storekeeper'))
    
class IsNotStorekeeper(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role != 'storekeeper'