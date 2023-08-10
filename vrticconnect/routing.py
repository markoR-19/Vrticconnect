from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/vrticconnect/(?P<grupa>\w+)/$',consumers.grupaConsumer.as_asgi()),
]