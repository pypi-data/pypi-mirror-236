Install the client library
--------------------------

::

   pip install --upgrade volcengine-avatar-live

Example
-------

.. code-block:: python

   # coding=utf-8

   import logging

   from volcengine_avatar_live.client import LiveClient
   from volcengine_avatar_live.model import INPUT_MODE_TEXT, INPUT_MODE_AUDIO
   from volcengine_avatar_live.util import create_logger

   logger = create_logger("main", logging.INFO)


   # 实际可根据 status、code 等信息自由调整错误处理逻辑
   def check_http_response(status: int, code: int, message: str) -> bool:
      if status != 200:
         logger.error("failed to post: {}".format(status))
         return False
      elif code != 1000:
         logger.error("failed to execute command: [{}]{}".format(code, message))
         return False
      return True


   def get_streaming_audio() -> (bytes, bool):
      # TBD: 添加流式音频获取逻辑
      pass


   if __name__ == "__main__":
      try:
         # 填写剧本内容，支持文本（text 或 ssml）和音频（ssml）两种模式
         contents = [
               (INPUT_MODE_TEXT, "text"),
               (INPUT_MODE_AUDIO, '<speak><audio url="http://host/xxx.mp3" format="mp3"/></speak>'),
         ]

         # 填写直播基本信息，生成客户端
         cli = (
               LiveClient("host")  # TBD: 填写域名
               .build_live("live-id")  # TBD: 填写直播 ID
               .build_auth("appid", "token")  # TBD: 填写鉴权信息
               .build_avatar(
                  "role",  # TBD: 填写形象
                  "",  # TBD: 填写模型，一般无需填写
                  "http://host/xxx.png",  # TBD: 填写背景
                  0,  # TBD: 填写码率
                  {  # TBD: 填写 video 配置
                     "video_width": 1080,
                     "video_height": 1920,
                     # others...
                  },
                  {},  # TBD: 填写 logo 配置
                  {  # TBD: 填写 role_conf 配置
                     "voice_type": "xxxxx",
                     "pose_type": "xxxxx",
                     "clothes_type": "xxxxx",
                     "role_width": 500,
                     "role_left_offset": 300,
                     "role_top_offset": 1000,
                     # others...
                  },
                  {},  # TBD: 填写 actions 配置
               )
               .build_streaming("rtmp://xxxxx")  # TBD: 填写 rtmp 推流地址
               .build_simple_script(contents)
         )

         # 开启直播
         status, code, message = cli.start_live()
         if not check_http_response(status, code, message):
               # TBD: 添加错误处理逻辑
               pass

         # 修改剧本播放模式
         # 顺序播放: 按原本剧本内容顺序依次循环播放
         # 随机播放: 每轮随机调整剧本内容顺序并依次播放
         # random=False: 顺序播放，random=True: 随机播放
         status, code, message = cli.change_play_mode(random=True)
         if not check_http_response(status, code, message):
               # TBD: 添加错误处理逻辑
               pass

         # 点播剧本内容
         # 智能打断当前播放剧本内容后跳转到点播内容，并从点播内容开始依次播放
         # index 为 contents 里的内容序号
         status, code, message = cli.change_play_task(index=0)
         if not check_http_response(status, code, message):
               # TBD: 添加错误处理逻辑
               pass

         # 文本驱动
         # 智能打断当前播放剧本内容后播放文本内容，结束后从断点继续播放剧本内容
         # input 为 text 或 ssml
         input = "text"
         # input = "<speak>ssml</speak>"
         status, code, message = cli.text_drive(input=input)
         if not check_http_response(status, code, message):
               # TBD: 添加错误处理逻辑
               pass

         # 音频驱动
         # 智能打断当前播放剧本内容后播放音频内容，结束后从断点继续播放剧本内容
         # input 为 ssml
         input = '<speak><audio url="http://host/xxx.mp3" format="mp3"/></speak>'
         status, code, message = cli.audio_drive(input=input)
         if not check_http_response(status, code, message):
               # TBD: 添加错误处理逻辑
               pass

         # 流式音频驱动
         # 智能打断当前播放剧本内容后播放流式音频内容，结束后从断点继续播放剧本内容
         # 一般用于真人接管场景，实时采集音频并驱动数字人
         while True:
               audio, end = get_streaming_audio()
               if end:
                  cli.end_stream()
                  break
               cli.stream(audio)

         # 关闭直播
         status, code, message = cli.close_live()
         if not check_http_response(status, code, message):
               # TBD: 添加错误处理逻辑
               pass
      except Exception as e:
         # TBD: 添加异常处理逻辑
         logger.error(e)
