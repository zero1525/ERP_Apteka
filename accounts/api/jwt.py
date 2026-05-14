from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if hasattr(user, 'space'):
            token['space_id'] = user.space.id
    

        return token
    
    def validate(self, attrs):
        data =  super().validate(attrs)

        data['username'] = self.user.username
        if hasattr(self.user, 'space') and self.user.space:
            data['space_name'] = self.user.space.name
        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer