from rest_framework import permissions

class IsManagerOfSpace(permissions.BasePermission):
    """
    Доступ только для MANAGER или OTHER (админа), привязанных к конкретному Space.
    """

    def has_permission(self, request, view):
        
        if not request.user or not request.user.is_authenticated:
            return False

       
        if request.user.is_superuser:
            return True

       
        if not hasattr(request.user, 'employee_profile'):
            return False

        
        space_id_url = view.kwargs.get('space_pk') or view.kwargs.get('space_id')
        if not space_id_url:
            return False

        employee = request.user.employee_profile
        
    
        is_correct_space = str(employee.space_id) == str(space_id_url)
        is_manager = employee.position in ['MANAGER', 'OTHER'] 

        return is_correct_space and is_manager