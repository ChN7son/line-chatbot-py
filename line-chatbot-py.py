# coding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

#line token
channel_access_token = 'QzpiJ0TLKDPkHLYJTGgXm+qaH3VOpBgQzQRreQ9TSoDFILCdzb5gqGDqNRxUEPb3cEJV2iGHP5GWcIqws/J2sZ8yL3vMwT5zInWqimHhPXy0P8O7AAknMJqDeK8YHnyPqeQQQIv9pva4U3NnE5PViwdB04t89/1O/w1cDnyilFU='
channel_secret = '6d4580ea02fab6b4bb9bbb7dd006e39c'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #echo
    msg= event.message.text
    message = TextSendMessage(text=msg)
    line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)