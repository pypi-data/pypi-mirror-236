# coding=utf-8

import json
import requests
import logging

from typing import List
from volcengine_avatar_live.model import (
    Live,
    Auth,
    Avatar,
    Streaming,
    Content,
    Scene,
    Product,
    Script,
    INPUT_MODE_TEXT,
    INPUT_MODE_AUDIO,
)
from volcengine_avatar_live.util import create_logger, generate_log_id
from websockets.sync.client import connect


class LiveClient:
    def __init__(self, host: str):
        if len(host) == 0:
            raise ValueError("host shouldn't be empty")
        self.logger = create_logger("live_client", logging.INFO)
        self.host = host
        self.ws = None
        self.live = None
        self.auth = None
        self.avatar = None
        self.streaming = None
        self.script = None

    def build_live(self, live_id: str):
        self.live = Live(live_id)
        return self

    def build_auth(self, appid: str, token: str):
        self.auth = Auth(appid, token)
        return self

    def build_avatar(
        self,
        role: str,
        dh_type: str,
        background: str,
        bitrate: str,
        video: map,
        logo: map,
        role_conf: map,
        actions: map,
    ):
        self.avatar = Avatar(role, dh_type, background, bitrate, video, logo, role_conf, actions)
        return self

    def build_streaming(self, rtmp_addr: str):
        self.streaming = Streaming(rtmp_addr)
        return self

    def build_simple_script(self, contents: List[tuple]):
        """Build script in a simple way that each content belongs to a single scene and a single product.

        :param contents: Each item should be a tuple with length 2 (mode, input). For example,
            [("text", "hello"),("audio", "<speak><audio url="http://foo/bar.pcm" format="pcm"/></speak>")]
        """
        product_list = []
        for c in contents:
            content = Content(c[0], c[1])
            content_list = [content]
            scene = Scene(content_list)
            scene_list = [scene]
            product = Product(scene_list)
            product_list.append(product)
        if len(product_list) > 0:
            self.script = Script(product_list)
        return self

    def start_live(self) -> (int, int, str):
        req = {
            "live": self.live.to_map(),
            "auth": self.auth.to_map(),
            "avatar": self.avatar.to_map(),
            "streaming": self.streaming.to_map(),
            "script": self.script.to_map(),
        }
        return self.__http_post__("start_live", req)

    def close_live(self) -> (int, int, str):
        req = {
            "live": self.live.to_map(),
            "auth": self.auth.to_map(),
        }
        return self.__http_post__("close_live", req)

    def change_play_mode(self, random: bool) -> (int, int, str):
        req = {
            "live": self.live.to_map(),
            "auth": self.auth.to_map(),
            "data": {"play_mode": 1 if random else 0},
        }
        return self.__http_post__("change_play_mode", req)

    def change_play_task(self, index: int) -> (int, int, str):
        product_id = ""
        scene_id = ""
        n = 0
        for p in self.script.product_list:
            for s in p.scene_list:
                n += 1
                if n - 1 == index:
                    product_id = p.product_id
                    scene_id = s.scene_id
                    break
            if n > index:
                break
        if n <= index:
            raise IndexError("index is out of script range")
        req = {
            "live": self.live.to_map(),
            "auth": self.auth.to_map(),
            "data": {
                "product_id": product_id,
                "scene_id": scene_id,
            },
        }
        return self.__http_post__("change_play_task", req)

    def text_drive(self, input: str) -> (int, int, str):
        req = {
            "live": self.live.to_map(),
            "auth": self.auth.to_map(),
            "data": {
                "mode": INPUT_MODE_TEXT,
                "input": input,
            },
        }
        return self.__http_post__("drive", req)

    def audio_drive(self, input: str) -> (int, int, str):
        req = {
            "live": self.live.to_map(),
            "auth": self.auth.to_map(),
            "data": {
                "mode": INPUT_MODE_AUDIO,
                "input": input,
            },
        }
        return self.__http_post__("drive", req)

    def stream(self, audio: bytes):
        live_id = self.live.live_id
        if self.ws is None:
            prefix = "wss://"
            if self.host.startswith("localhost"):
                prefix = "ws://"
            url = prefix + self.host + "/virtual_human/avatar_live/live"
            self.log_id = generate_log_id()
            self.logger.info("[log_id: {}][live_id: {}]connect websocket".format(self.log_id, live_id))
            headers = {"X-Tt-Logid": self.log_id}
            self.ws = connect(url, logger=self.logger, additional_headers=headers)
            req = {
                "live": self.live.to_map(),
                "auth": self.auth.to_map(),
                "avatar": self.avatar.to_map(),
                "streaming": self.streaming.to_map(),
                "script": self.script.to_map(),
            }
            self.ws.send("|CTL|00|" + json.dumps(req))
            resp = self.ws.recv()
            self.logger.info("[log_id: {}][live_id: {}]websocket response: {}".format(self.log_id, live_id, resp))
            if len(resp) < 8:
                raise ConnectionError("invalid websocket response: {}".format(resp))
            msg = json.loads(resp[8:])
            if msg["code"] != 1000:
                self.logger.error("[log_id: {}][live_id: {}]websocket response: {}".format(self.log_id, live_id, resp))
                self.ws.close(1000)
                self.ws = None
                self.log_id = None
                raise ConnectionError("[{}]{}".format(msg["code"], msg["message"]))
        self.logger.info(
            "[log_id: {}][live_id: {}]send streaming audio, length: {}".format(self.log_id, live_id, len(audio))
        )
        if len(audio) > 0:
            req = b"|DAT|02|" + audio
            self.ws.send(req)

    def end_stream(self):
        if self.ws is not None:
            self.logger.info(
                "[log_id: {}][live_id: {}]end streaming audio and close websocket".format(
                    self.log_id, self.live.live_id
                )
            )
            self.ws.send("|CTL|12|")
            self.ws.close(1000)
            self.ws = None
            self.log_id = None

    def __http_post__(self, url_suffix: str, req: map) -> (int, int, str):
        log_id = generate_log_id()
        live_id = self.live.live_id
        self.logger.info("[log_id: {}][live_id: {}]========== {} ==========".format(log_id, live_id, url_suffix))
        self.logger.info("[log_id: {}][live_id: {}]http request: {}".format(log_id, live_id, req))
        prefix = "https://"
        if self.host.startswith("localhost"):
            prefix = "http://"
        url = prefix + self.host + "/virtual_human/avatar_live/" + url_suffix
        headers = {"Content-Type": "application/json", "X-Tt-Logid": log_id}
        resp = requests.post(url, data=json.dumps(req), headers=headers)
        if resp.status_code != 200:
            self.logger.error(
                "[log_id: {}][live_id: {}]http response status: {}".format(log_id, live_id, resp.status_code)
            )
            return resp.status_code, 0, ""
        self.logger.info("[log_id: {}][live_id: {}]http response: {}".format(log_id, live_id, resp.text))
        msg = json.loads(resp.content)
        return resp.status_code, msg["code"], msg["message"]
