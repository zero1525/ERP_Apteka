from rest_framework import permissions
from ..models import EmployeesPosition


class IsManagerOfSpace(permissions.BasePermission):
    def has_permission(self, request, view): 
        user = request.user

        if user.is_superuser:
            return True
        
        employee = getattr(user, 'employee_profile', None)
        if not employee:
            return False
        
        return employee.position in [EmployeesPosition.MANAGER,EmployeesPosition.ADMIN]