"""
DiscordRPC.py
-----------------------------
A complete Discord RPC interface written in Python
Original code by qwertyquerty and LewdNeko
Rewritten by LBots.org
"""

from .baseclient import BaseClient
from .client import Client, AioClient
from .exceptions import *
from .payloads import Payload
from .response import Response


__title__ = 'discordrpc'
__author__ = 'LBots'
__copyright__ = 'Copyright 2019 LBots'
__license__ = 'MIT'
__version__ = '1.0.0'
