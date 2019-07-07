import json
import os
from time import time
from typing import List, Union

from .utils import remove_none


def generic_payload(cmd: str, args: dict, event=None):
    payload = {
        "cmd": cmd,
        "args": args,
        "nonce": "{:.20f}".format(time())
    }
    if event:
        payload["evt"] = event
    return payload


class Payload:

    def __init__(self, data, clear_none=True):
        if clear_none:
            data = remove_none(data)
        self.data = data

    def __str__(self):
        return json.dumps(self.data)

    @classmethod
    def set_activity(cls, pid: int = os.getpid(),
                     state: str = None, details: str = None,
                     start: int = None, end: int = None,
                     large_image: str = None, large_text: str = None,
                     small_image: str = None, small_text: str = None,
                     party_id: str = None, party_size: list = None,
                     join: str = None, spectate: str = None,
                     match: str = None, instance: bool = True,
                     activity: Union[bool, None] = True,
                     _rn: bool = True):

        if start:
            start = int(start)
        if end:
            end = int(end)

        if activity is None:
            act_details = None
            clear = True
        else:
            act_details = {
                "state": state,
                "details": details,
                "timestamps": {
                    "start": start,
                    "end": end
                },
                "assets": {
                    "large_image": large_image,
                    "large_text": large_text,
                    "small_image": small_image,
                    "small_text": small_text
                },
                "party": {
                    "id": party_id,
                    "size": party_size
                },
                "secrets": {
                    "join": join,
                    "spectate": spectate,
                    "match": match
                },
                "instance": instance
            }
            clear = False

        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": pid,
                "activity": act_details
            },
            "nonce": '{:.20f}'.format(time())
        }
        if _rn:
            clear = _rn
        return cls(payload, clear)

    @classmethod
    def authorize(cls, client_id: str, scopes: List[str]):
        payload = generic_payload('AUTHORIZE', {"client_id": client_id, "scopes": scopes})
        return cls(payload)

    @classmethod
    def authenticate(cls, token: str):
        payload = generic_payload('AUTHENTICATE', {"access_token": token})
        return cls(payload)

    @classmethod
    def get_guilds(cls):
        payload = generic_payload("GET_GUILDS", {})
        return cls(payload)

    @classmethod
    def get_guild(cls, guild_id: str):
        payload = generic_payload("GET_GUILD", {"guild_id": guild_id})
        return cls(payload)

    @classmethod
    def get_channels(cls, guild_id: str):
        payload = generic_payload("GET_CHANNELS", {"guild_id": guild_id})
        return cls(payload)

    @classmethod
    def get_channel(cls, channel_id: str):
        payload = generic_payload("GET_CHANNEL", {"channel_id": channel_id})
        return cls(payload)

    @classmethod
    def set_user_voice_settings(cls, user_id: str, pan_left: float,
                                pan_right: float, volume: int,
                                mute: bool):
        payload = generic_payload("SET_USER_VOICE_SETTINGS", {
            "user_id": user_id,
            "pan": {
                "left": pan_left,
                "right": pan_right,
            },
            "volume": volume,
            "mute": mute
        })
        return cls(payload, True)

    @classmethod
    def select_voice_channel(cls, channel_id: str):
        payload = generic_payload("SELECT_VOICE_CHANNEL", {"channel_id": channel_id})
        return cls(payload)

    @classmethod
    def get_selected_voice_channel(cls):
        payload = generic_payload("GET_SELECTED_VOICE_CHANNEL", {})
        return cls(payload)

    @classmethod
    def select_text_channel(cls, channel_id: str, timeout: int):
        payload = generic_payload("SELECT_VOICE_CHANNEL", {"channel_id": channel_id, "timeout": timeout})
        return cls(payload)

    @classmethod
    def subscribe(cls, event: str, args: dict):
        payload = {
            "cmd": "SUBSCRIBE",
            "args": args,
            "evt": event.upper(),
            "nonce": '{:.20f}'.format(time())
        }
        return cls(payload)

    @classmethod
    def unsubscribe(cls, event: str, args: dict):
        payload = {
            "cmd": "UNSUBSCRIBE",
            "args": args,
            "evt": event.upper(),
            "nonce": '{:.20f}'.format(time())
        }
        return cls(payload)

    @classmethod
    def get_voice_settings(cls):
        payload = generic_payload("GET_VOICE_SETTINGS", {})
        return cls(payload)

    @classmethod
    def set_voice_settings(cls, _input: dict = None, output: dict = None,
                           mode: dict = None, automatic_gain_control: bool = None,
                           echo_cancellation: bool = None, noise_suppression: bool = None,
                           qos: bool = None, silence_warning: bool = None,
                           deaf: bool = None, mute: bool = None):
        payload = generic_payload("SET_VOICE_SETTINGS",
                                  {
                                      "input": _input,
                                      "output": output,
                                      "mode": mode,
                                      "automatic_gain_control": automatic_gain_control,
                                      "echo_cancellation": echo_cancellation,
                                      "noise_suppression": noise_suppression,
                                      "qos": qos,
                                      "silence_warning": silence_warning,
                                      "deaf": deaf,
                                      "mute": mute
                                  })
        # TODO: Implement default input, output, and mode object structures
        # See Discord docs. Also please fix the function typehints :( Maybe just replace with
        # kwargs? Would look a lot nicer.
        return cls(payload, True)

    @classmethod
    def capture_shortcut(cls, action: str):
        payload = generic_payload("CAPTURE_SHORTCUT", {"action": action.upper()})
        return cls(payload)

    @classmethod
    def set_certified_devices(cls, devices: List[dict]):
        """ Only used by hardware manufacturers to send information
        about device state to Discord. See docs for Object spec if you need this. """
        payload = generic_payload("SET_CERTIFIED_DEVICES", {"devices": devices})
        return cls(payload)

    @classmethod
    def send_activity_join_invite(cls, user_id: str):
        payload = generic_payload("SEND_ACTIVITY_JOIN_INVITE", {"user_id": user_id})
        return cls(payload)

    @classmethod
    def close_activity_request(cls, user_id: str):
        payload = generic_payload("CLOSE_ACTIVITY_REQUEST", {"user_id": user_id})
        return cls(payload)
