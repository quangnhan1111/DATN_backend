# Create your views here.
from rest_framework import status
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.utils import response
from invoices.models import Invoice
from .models import Notifications, MessageNotifications


@api_view(['GET'])
def notifications(request):
    data = Notifications.objects.filter(is_seen=False).values()
    content = response(data, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def mark(request, pk):
    notification = Notifications.objects.filter(id=pk).update(is_seen=True)
    content = response(notification, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)

@api_view(['GET'])
def clear_all_notification(request):
    data = Notifications.objects.all().update(is_seen=True)
    content = response('Clear successfully', 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def message_notifications(request):
    messages = MessageNotifications.objects.filter(is_seen=False).values()
    content = response(messages, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def mark_message(request, pk):
    message = MessageNotifications.objects.filter(id=pk).update(is_seen=True)
    content = response(message, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)

@api_view(['GET'])
def clear_all_message(request):
    message = MessageNotifications.objects.all().update(is_seen=True)
    content = response('Clear successfully', 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def invoice_notifications(request):
    count = Invoice.objects.filter(is_paid=False).count()
    content = response(count, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)

