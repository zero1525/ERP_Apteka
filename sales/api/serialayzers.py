from rest_framework.serializers import  ModelSerializer
from ..models import CheckItem, HeaderCheck
from ..service import create_check

class CheckItemSerializer(ModelSerializer):
    class Meta:
        model = CheckItem
        fields = 'recept', 'quantity'

class HeaderCheckSerializer(ModelSerializer):
    items = CheckItemSerializer(many=True)
    class Meta:
        model = HeaderCheck
        fields = 'branch', 'number_kassa', 'items'
        
    def create(self, validated_data):
        user = self.context['request'].user
        
        space = user.employee_profile.space 
        branch = validated_data['branch']
        number_kassa = validated_data['number_kassa']
        items = validated_data['items']
        
        return create_check(
            space=space,
            branch=branch,
            number_kassa=number_kassa,
            items=items
        )