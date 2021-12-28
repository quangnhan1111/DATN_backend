from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from mailer.models import ScheduleMail
from customers.models import Customer as CustomerModel
# from app.celery import app
# from celery.schedules import crontab


# @shared_task
# def send_async_mail(subject: str, emails: list, text_msg: str, html_msg: str):
#     send_mail(subject=subject, from_email=settings.EMAIL_HOST_USER,
#               recipient_list=emails, message=text_msg,
#               fail_silently=True, html_message=html_msg)
#     print("email sent")
#     return True


@shared_task
def send_scheduled_mails():
    mail = ScheduleMail.objects.all().first()
    # print(mail)
    # for _ in CustomerModel.objects.all():
    #     print(_.user.email)
    # list = CustomerModel.objects.filter()
    send_mail(subject=mail.subject, from_email=settings.EMAIL_HOST_USER,
              recipient_list=[_.user.email for _ in CustomerModel.objects.all()],
              message=mail.message,
              fail_silently=True, html_message=mail.html_content)