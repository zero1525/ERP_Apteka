from rest_framework import viewsets
from .serialayzers import EmployeeSerializer
from ..models import Employees
from .permision import IsManagerOfSpace

class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employees.objects.select_related('user', 'space', 'branch').all()
    permission_classes = [IsManagerOfSpace]

    
    def perform_create(self, serializer):
        serializer.save()