from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from ..models import Employees
from .tasks import send_welcome_email

User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    full_name = serializers.CharField(source='user.full_name')
    phone_number = serializers.CharField(source='user.phone_number', required=False, allow_blank=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Employees
        fields = [
            'id', 'email', 'full_name', 'phone_number', 'password1', 'password2',
            'avatar', 'position', 'experience', 'contact_info', 'skills', 
            'iin', 'year_of_birth',  'salary', 'branch'
        ]

    def validate(self, data):
        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError({"password2": "Пароли не совпадают."})
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password1')
        validated_data.pop('password2') 

        with transaction.atomic():
            user = User.objects.create_user(
                email=user_data['email'],
                full_name=user_data['full_name'],
                phone_number=user_data.get('phone_number'),
                password=password
            )

           
            request = self.context.get('request')
            manager_space = request.user.employee_profile.space

            employee = Employees.objects.create(
                user=user, 
                space=manager_space, 
                **validated_data
            )
            send_welcome_email.delay(
                user.email, 
                user.full_name, 
                password, 
                manager_space.name
            )
        return employee