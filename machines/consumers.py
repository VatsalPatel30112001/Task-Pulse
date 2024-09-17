import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from axis.models import *

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class MachineValuesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "data_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "data_updates",
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def send_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            'data': data
        }))


def broadcast_data(json):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "data_updates", {
            "type": "send_data",
            "data": json
        }
    )
