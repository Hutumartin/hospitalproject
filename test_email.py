import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospitalproject.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print('Email user:', settings.EMAIL_HOST_USER)
print('Email password set:', bool(settings.EMAIL_HOST_PASSWORD))
print('Sending test email...')

try:
    send_mail(
        'Test Email from HMS',
        'This is a test email from your Hospital Management System.',
        settings.DEFAULT_FROM_EMAIL,
        ['hutumartin748@gmail.com'],
        fail_silently=False,
    )
    print('SUCCESS! Email sent!')
except Exception as e:
    print('FAILED! Error:', str(e))