"""
WebSocket consumers for real-time features
"""

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class VideoCallConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for video calls"""
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'video_call_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'offer' or message_type == 'answer' or message_type == 'ice-candidate':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'video_signal',
                    'data': data
                }
            )
    
    async def video_signal(self, event):
        await self.send(text_data=json.dumps(event['data']))
