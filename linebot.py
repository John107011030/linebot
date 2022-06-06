from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('mK+R1//sAQFF0f7vYCjeIxMRzvpw2QX8MeQ/nPxBwQiOoMpT1+065LNsO5NwmvwuNbkdZU8l3cS8MrUo8laVo5ZQGYte1n/zgqp/qeDfnx3eUZdXbf4HRpkFI39Jsz8Q3oFQMTWRC2jphVRY/cNy2gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c788bee006f5e3fd138ffdf07b11dcd3')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()