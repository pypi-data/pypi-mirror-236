# coding=utf-8

import uuid

from typing import List

INPUT_MODE_TEXT = "text"
INPUT_MODE_AUDIO = "audio"


class Live:
    def __init__(self, live_id: str):
        if len(live_id) == 0:
            raise ValueError("live_id shouldn't be empty")
        elif len(live_id) > 128:
            raise ValueError("live_id shouldn't be longer than 128")
        self.live_id = live_id

    def to_map(self) -> map:
        return {"live_id": self.live_id}


class Auth:
    def __init__(self, appid: str, token: str):
        if len(appid) == 0:
            raise ValueError("appid shouldn't be empty")
        if len(token) == 0:
            raise ValueError("token shouldn't be empty")
        self.appid = appid
        self.token = token

    def to_map(self) -> map:
        return {"appid": self.appid, "token": self.token}


class Avatar:
    def __init__(
        self,
        role: str,
        dh_type: str,
        background: str,
        bitrate: int,
        video: map,
        logo: map,
        role_conf: map,
        actions: map,
    ):
        if len(role) == 0:
            raise ValueError("role shouldn't be empty")
        if bitrate != 0 and (bitrate < 100 or bitrate > 8000):
            raise ValueError("bitrate is invalid")
        if "voice_type" not in role_conf:
            raise ValueError("voice_type shouldn't be empty")
        else:
            voice_type = role_conf["voice_type"]
            if isinstance(voice_type, str):
                if len(voice_type) == 0:
                    raise ValueError("voice_type shouldn't be empty")
            else:
                raise ValueError("voice_type is invalid")
        self.role = role
        self.dh_type = dh_type
        self.background = background
        self.bitrate = bitrate
        self.video = video
        self.logo = logo
        self.role_conf = role_conf
        self.actions = actions

    def to_map(self) -> map:
        m = {
            "avatar_type": "2d",
            "input_mode": INPUT_MODE_AUDIO,
            "role": self.role,
        }
        if len(self.dh_type) > 0:
            m["dh_type"] = self.dh_type
        if len(self.background) > 0:
            m["background"] = self.background
        if self.bitrate > 0:
            m["bitrate"] = self.bitrate
        if self.video is not None and len(self.video) > 0:
            m["video"] = self.video
        if self.logo is not None and len(self.logo) > 0:
            m["logo"] = self.logo
        if self.role_conf is not None and len(self.role_conf) > 0:
            m["role_conf"] = self.role_conf
        if self.actions is not None and len(self.actions) > 0:
            m["actions"] = self.actions
        return m


class Streaming:
    def __init__(self, rtmp_addr: str):
        if len(rtmp_addr) == 0:
            raise ValueError("rtmp_addr shouldn't be empty")
        self.rtmp_addr = rtmp_addr

    def to_map(self) -> map:
        return {"type": "rtmp", "rtmp_addr": self.rtmp_addr}


class Content:
    def __init__(self, mode: str, input: str):
        if mode == INPUT_MODE_TEXT:
            if len(input) == 0:
                raise ValueError("input is invalid")
            elif len(input) > 1000:
                raise ValueError("input shouldn't be longer than 1000")
        elif mode == INPUT_MODE_AUDIO:
            if len(input) == 0:
                raise ValueError("input is invalid")
        else:
            raise ValueError("mode is invalid")
        self.mode = mode
        self.input = input

    def to_map(self) -> map:
        return {"mode": self.mode, "input": self.input}


class Scene:
    def __init__(self, content_list: List[Content]):
        if len(content_list) == 0:
            raise ValueError("content_list shouldn't be empty")
        self.scene_id = str(uuid.uuid4())
        self.content_list = content_list

    def to_map(self) -> map:
        return {"scene_id": self.scene_id, "content_list": [c.to_map() for c in self.content_list]}


class Product:
    def __init__(self, scene_list: List[Scene]):
        if len(scene_list) == 0:
            raise ValueError("scene_list shouldn't be empty")
        self.product_id = str(uuid.uuid4())
        self.scene_list = scene_list

    def to_map(self) -> map:
        return {"product_id": self.product_id, "scene_list": [s.to_map() for s in self.scene_list]}


class Script:
    def __init__(self, product_list: List[Product]):
        if len(product_list) == 0:
            raise ValueError("product_list shouldn't be empty")
        self.script_id = str(uuid.uuid4())
        self.product_list = product_list

    def to_map(self) -> map:
        return {"script_id": self.script_id, "product_list": [p.to_map() for p in self.product_list]}
