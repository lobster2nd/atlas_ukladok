from celery import shared_task
from django.core.mail import send_mail

from core import settings


def send_confirmation_code(user_address, confirmation_code):
    """Отправка кода подтверждения"""
    subject = 'Код подтверждения'
    message = f'Для входа на сайт введите код {confirmation_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_address]

    send_mail(subject, message, from_email, recipient_list)

@shared_task(bind=True, max_retries=3)
def send_confirmation_code_task(self, address, code):
    try:
        send_confirmation_code(address, code)
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
