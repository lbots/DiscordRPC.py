import inspect
import json
import os
from typing import List

from .baseclient import BaseClient
from .exceptions import *
from .payloads import Payload


class AioClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, isasync=True)
        self._closed = False
        self._events = {}

    async def register_event(self, event: str, func: callable, args: dict = {}):
        if len(inspect.signature(func).parameters) != 1:
            raise ValueError('Unexpected amount of function paameters. Expected 1.')
        await self.subscribe(event, args)
        self._events[event.lower()] = func

    async def unregister_event(self, event: str, args: dict = {}):
        event = event.lower()
        # Don't know what to do, so do nothing. Thanks, Andrew.
        if event not in self._events:
            return
        await self.unsubscribe(event, args)
        del self._events[event]

    async def on_event(self, data):
        if self.sock_reader._eof:
            raise DRPCGenericError('feed_data after feed_eof')
        if not data:
            return
        self.sock_reader._buffer.extend(data)
        self.sock_reader._wakeup_waiter()
        if (self.sock_reader._transport is not None and
                not self.sock_reader._paused and
                len(self.sock_reader._buffer) > 2 * self.sock_reader._limit):
            try:
                self.sock_reader._transport.pause_reading()
            except NotImplementedError:
                self.sock_reader._transport = None
            else:
                self.sock_reader._paused = True

        payload = json.loads(data[8:].decode('utf-8'))

        if payload["evt"] is not None:
            evt = payload["evt"].lower()
            if evt in self._events:
                ev_func = self._events[evt](payload["data"])
                if inspect.iscoroutinefunction(ev_func):
                    await ev_func
            elif evt == 'error':
                raise DiscordError(payload["data"]["code"], payload["data"]["message"])

    async def authorize(self, client_id: str, scopes: List[str]):
        payload = Payload.authorize(client_id, scopes)
        self.send_data(1, payload)
        return await self.read_output()

    async def authenticate(self, token: str):
        payload = Payload.authenticate(token)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_guilds(self):
        payload = Payload.get_guilds()
        self.send_data(1, payload)
        return await self.read_output()

    async def get_guild(self, guild_id: str):
        payload = Payload.get_guild(guild_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_channel(self, channel_id: str):
        payload = Payload.get_channel(channel_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_channels(self, guild_id: str):
        payload = Payload.get_channels(guild_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def set_user_voice_settings(self, user_id: str, pan_left: float = None,
                                      pan_right: float = None, volume: int = None,
                                      mute: bool = None):
        payload = Payload.set_user_voice_settings(user_id, pan_left, pan_right, volume, mute)
        self.send_data(1, payload)
        return await self.read_output()

    async def select_voice_channel(self, channel_id: str):
        payload = Payload.select_voice_channel(channel_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_selected_voice_channel(self):
        payload = Payload.get_selected_voice_channel()
        self.send_data(1, payload)
        return await self.read_output()

    async def select_text_channel(self, channel_id: str, timeout: int):
        payload = Payload.select_text_channel(channel_id, timeout)
        self.send_data(1, payload)
        return await self.read_output()

    async def set_activity(self, pid: int = os.getpid(),
                           state: str = None, details: str = None,
                           start: int = None, end: int = None,
                           large_image: str = None, large_text: str = None,
                           small_image: str = None, small_text: str = None,
                           party_id: str = None, party_size: list = None,
                           join: str = None, spectate: str = None,
                           match: str = None, instance: bool = True):
        payload = Payload.set_activity(pid, state, details, start, end, large_image, large_text,
                                       small_image, small_text, party_id, party_size, join, spectate,
                                       match, instance, activity=True)
        self.send_data(1, payload)
        # TODO: Make this code not so god awful
        return await self.read_output()

    async def clear_activity(self, pid: int = os.getpid()):
        payload = Payload.set_activity(pid, None, None, None, None, None, None, None, None, None, None, None, None,
                                       None, None, None)
        self.send_data(1, payload)
        # TODO: THIS TOOO AAAAAAAAAAAAAĀ
        return await self.read_output()

    async def subscribe(self, event: str, args: dict = {}):
        payload = Payload.subscribe(event, args)
        self.send_data(1, payload)
        return await self.read_output()

    async def unsubscribe(self, event: str, args: dict = {}):
        payload = Payload.unsubscribe(event, args)
        self.send_data(1, payload)
        return await self.read_output()

    async def get_voice_settings(self):
        payload = Payload.get_voice_settings()
        self.send_data(1, payload)
        return await self.read_output()

    async def set_voice_settings(self, _input: dict = None, output: dict = None,
                                 mode: dict = None, automatic_gain_control: bool = None,
                                 echo_cancellation: bool = None, noise_suppression: bool = None,
                                 qos: bool = None, silence_warning: bool = None,
                                 deaf: bool = None, mute: bool = None):
        payload = Payload.set_voice_settings(_input, output, mode, automatic_gain_control, echo_cancellation,
                                             noise_suppression, qos, silence_warning, deaf, mute)
        self.send_data(1, payload)
        return await self.read_output()

    async def capture_shortcut(self, action: str):
        payload = Payload.capture_shortcut(action)
        self.send_data(1, payload)
        return await self.read_output()

    async def send_activity_join_invite(self, user_id: str):
        payload = Payload.send_activity_join_invite(user_id)
        self.send_data(1, payload)
        return await self.read_output()

    async def close_activity_request(self, user_id: str):
        payload = Payload.close_activity_request(user_id)
        self.send_data(1, payload)
        return await self.read_output()

    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self._closed = True
        self.close_event_loop()

    async def start(self):
        await self.handshake()


class Client(AioClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._closed = False
        self._events = {}

    def register_event(self, event: str, func: callable, args: dict = {}):
        if inspect.iscoroutinefunction(func):
            raise NotImplementedError('Event callback cannot be a coroutine')
        elif len(inspect.signature(func).parameters) != 1:
            raise ValueError('Unexpected amount of function paameters. Expected 1.')
        self.subscribe(event, args)
        self._events[event.lower()] = func

    def unregister_event(self, event: str, args: dict = {}):
        event = event.lower()
        # Don't know what to do, so do nothing. Thanks, Andrew.
        if event not in self._events:
            return
        self.unsubscribe(event, args)
        del self._events[event]

    def on_event(self, data):
        if self.sock_reader._eof:
            raise DRPCGenericError('feed_data after feed_eof')
        if not data:
            return
        self.sock_reader._buffer.extend(data)
        self.sock_reader._wakeup_waiter()
        if (self.sock_reader._transport is not None and
                not self.sock_reader._paused and
                len(self.sock_reader._buffer) > 2 * self.sock_reader._limit):
            try:
                self.sock_reader._transport.pause_reading()
            except NotImplementedError:
                self.sock_reader._transport = None
            else:
                self.sock_reader._paused = True

        payload = json.loads(data[8:].decode('utf-8'))

        if payload["evt"] is not None:
            evt = payload["evt"].lower()
            if evt in self._events:
                self._events[evt](payload["data"])
            elif evt == 'error':
                raise DiscordError(payload["data"]["code"], payload["data"]["message"])

    def run_super(self, function_name, *args, **kwargs):
        parent_func = getattr(super(), function_name, lambda x: x)
        return self.loop.run_until_complete(parent_func(*args, **kwargs))

    def authorize(self, client_id: str, scopes: List[str]):
        return self.run_super('authorize', client_id, scopes)

    def authenticate(self, token: str):
        return self.run_super('authenticate', token)

    def get_guilds(self):
        return self.run_super('get_guilds')

    def get_guild(self, guild_id: str):
        return self.run_super('get_guild', guild_id)

    def get_channel(self, channel_id: str):
        return self.run_super('get_channel', channel_id)

    def get_channels(self, guild_id: str):
        return self.run_super('get_channels', guild_id)

    def set_user_voice_settings(self, user_id: str, pan_left: float = None,
                                pan_right: float = None, volume: int = 100,
                                mute: bool = False):
        return self.run_super('set_user_voice_settings', user_id, pan_left, pan_right, volume, mute)

    def select_voice_channel(self, channel_id: str):
        return self.run_super('select_voice_channel', channel_id)

    def get_selected_voice_channel(self):
        return self.run_super('get_selected_voice_channel')

    def select_text_channel(self, channel_id: str, timeout: int):
        return self.run_super('select_text_channel', channel_id, timeout)

    def set_activity(self, pid: int = os.getpid(),
                     state: str = None, details: str = None,
                     start: int = None, end: int = None,
                     large_image: str = None, large_text: str = None,
                     small_image: str = None, small_text: str = None,
                     party_id: str = None, party_size: list = None,
                     join: str = None, spectate: str = None,
                     match: str = None, instance: bool = True):

        return self.run_super('set_activity', pid, state, details, start, end, large_image, large_text,
                              small_image, small_text, party_id, party_size, join, spectate, match, instance)

    def clear_activity(self, pid: int = os.getpid()):
        return self.run_super('set_activity', pid, activity=None)

    def subscribe(self, event: str, args: dict = {}):
        return self.run_super('subscribe', event, args)

    def unsubscribe(self, event: str, args: dict = {}):
        return self.run_super('unsubscribe', event, args)

    def get_voice_settings(self):
        return self.run_super('get_voice_settings')

    def set_voice_settings(self, _input: dict = None, output: dict = None,
                           mode: dict = None, automatic_gain_control: bool = None,
                           echo_cancellation: bool = None, noise_suppression: bool = None,
                           qos: bool = None, silence_warning: bool = None,
                           deaf: bool = None, mute: bool = None):
        payload = Payload.set_voice_settings(_input, output, mode, automatic_gain_control, echo_cancellation,
                                             noise_suppression, qos, silence_warning, deaf, mute)
        self.send_data(1, payload)
        return self.run_super('set_voice_settings', _input, output)

    def capture_shortcut(self, action: str):
        payload = Payload.capture_shortcut(action)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def send_activity_join_invite(self, user_id: str):
        payload = Payload.send_activity_join_invite(user_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def close_activity_request(self, user_id: str):
        payload = Payload.close_activity_request(user_id)
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self._closed = True
        self.close_event_loop()

    def start(self):
        self.loop.run_until_complete(self.handshake())

    def read(self):
        return self.loop.run_until_complete(self.read_output())
