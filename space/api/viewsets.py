from rest_framework import viewsets
from ..models import Space, Branch, PhoneNumber, SocialMedia
from .serializers import SpaceSerializer, BranchSerializer

class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer

    def get_quesryset(self):
        Space.objects.filter(users=self.request.user) 

    def perform_create(self, serializer):
        serializer.save(users=self.request.user)

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_quesryset(self):
        Branch.objects.filter(users=self.request.user)