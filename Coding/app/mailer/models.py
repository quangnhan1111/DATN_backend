import jwt
import markdown2
from django.db import models
from django.conf import settings
# from django.contrib.sites.models import Site


# class News(models.Model):
#     # list mail
#     mail = models.EmailField(max_length=255, verbose_name="User's Email", unique=True)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.mail


class ScheduleMail(models.Model):
    # storing mail templates to send regularly
    subject = models.CharField(max_length=255, verbose_name="Email's Subject")
    message = models.TextField(max_length=300, verbose_name="Markdown's Content")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def html_content(self):
        markdown = markdown2.Markdown()
        return markdown.convert(self.message)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject


# def encrypt_email(email: str) -> str:
#     encode_jwt = jwt.encode({'email': email}, settings.SECRET_KEY)
#     return encode_jwt
#
#
# def decrypt_email(token: str) -> str:
#     data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
#     return data['email']


# def generate_unsub_url(token: str, https: bool = False) -> str:
#     try:
#         site = Site.objects.get(name='dev')
#     except Site.DoesNotExist:
#         raise Exception('Site does not exists')
#     full_domains = f"http{'s' if https else ''}://{site.domain}"
#     return f"{full_domains}/api/mail/news/unsubscribe/{token}"