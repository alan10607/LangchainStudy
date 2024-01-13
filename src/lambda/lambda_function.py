import json
import os
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
from lib.langchain_assistant import ChatAI


configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
ai = ChatAI()

def lambda_handler(event, context):
    @handler.add(MessageEvent, message=TextMessageContent)
    def handle_message(event):
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            text = "error"
            # if event.message.type == "text":
            #     user_input = event.message.text
            #     result = ai.run(user_input)
            #     text = "user_input:" + user_input + ",result:" + result
            # else:
            #     text = "Not a text message. Can't reply to you"
                
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=text), TextMessage(text=text)]
                )
            )

        


    # get X-Line-Signature header value
    signature = event["headers"]["x-line-signature"] # must in lower-case or it will 502

    # get request body as text
    body = event["body"]

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        return {
            "statusCode": 502,
            "body": json.dumps("Invalid Line signature. Please check your channel access token/channel secret. Error: " + str(e))
        }
    return {
        "statusCode": 200,
        "body": json.dumps("ok")
    }
