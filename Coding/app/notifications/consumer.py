import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'notification'
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )
        self.accept()
        # self.send(text_data=json.dumps(
        #     {
        #         'status': "connected"
        #     }
        # ))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data):
        self.send(text_data=json.dumps({
            'status': "We got you"
        }))

    def send_notification(self, event):
        data = json.loads(event['value'])
        print(data)
        self.send(text_data=json.dumps(data))


class MessageNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'message_notification'
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )
        self.accept()
        # self.send(text_data=json.dumps(
        #     {
        #         'status': "connected"
        #     }
        # ))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data):
        self.send(text_data=json.dumps({
            'status': "We got you"
        }))

    def send_message_notification(self, event):
        data = json.loads(event['value'])
        print(data)
        self.send(text_data=json.dumps(data))



class InvoiceNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'invoice_notification'
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data):
        self.send(text_data=json.dumps({
            'status': "We got you"
        }))

    def send_invoice_notification(self, event):
        data = event['value']
        print(data)
        self.send(text_data=data)





