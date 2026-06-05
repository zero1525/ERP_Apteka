from rest_framework import serializers
from ..models import Space, Branch, PhoneNumber, SocialMedia

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['operator', 'number']

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['platform', 'url']

class SpaceSerializer(serializers.ModelSerializer):
    PhoneNumberSerializer = serializers.StringRelatedField(many=True, read_only=True)
    SocialMediaSerializer = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Space
        fields = [ 'name', 'description', 'PhoneNumberSerializer', 'SocialMediaSerializer']

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [ 'space', 'name', 'address']