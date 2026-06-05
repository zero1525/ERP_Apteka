from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def create_object_for_user_space(model_class: type[models.Model], user: User, validated_data: dict) -> models.Model:
    user_space = user.employee_profile.space

    final_data = {
        **validated_data,
        'space': user_space
    }
    return model_class.objects.create(**final_data)