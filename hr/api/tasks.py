from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(email, full_name, password, space_name):
    subject = f'Добро пожаловать в нашу компанию {space_name}!'
    message = f'Здравствуйте, {full_name}! Спасибо за присоединение к нашей команде. Мы рады работать с вами. Это ваш пароль для входа в систему: {password}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    from_email = settings.DEFAULT_FROM_EMAIL

    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)