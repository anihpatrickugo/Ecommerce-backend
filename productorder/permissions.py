from rest_framework.permissions import BasePermission

class IsOrderOwner(BasePermission):
    """
    check if the request user is the owner of the object.
    """
    pass

    def has_object_permission(self, request, view, obj) -> bool:
        if obj.user == request.user:
            return True
        return False
