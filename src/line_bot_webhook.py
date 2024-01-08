from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
# from assistant import run, assistant_id, thread
from langchain_assistant import ChatAI

app = Flask(__name__)

configuration = Configuration(access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text = True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid Line signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message = TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        user_input = event.message.text
        event.source.userId
        result = run(user_input)
        print("result=", result)
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=result)]
            )
        )
@app.route("/test", methods=["GET"])
def backdoor():
    user_input = request.args.get("q")
    # result = run(assistant_id, thread, user_input)
    ai = ChatAI()
    result = ai.run(user_input)
    return result

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 5001)

