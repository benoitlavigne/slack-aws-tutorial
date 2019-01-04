import json
import os

from lib.make_response import make_response
from slackclient import SlackClient

APP_TOKEN = os.environ.get("APP_TOKEN")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

sc = SlackClient(BOT_TOKEN)


def event_handler(event, context):

    event_payload = json.loads(event.get("body"))
    print(event_payload)

    # Verifying that the token matches the expected value
    if event_payload.get("token") == APP_TOKEN:

        # confirming url when events endpoint is added in Slack
        if "challenge" in event_payload:
            return make_response(event_payload["challenge"], 200)

        # all other cases besides confirming url
        else:
            success = event_processor(event_payload)
            if success:
                print ("event successfully handled")
                return make_response("ok", 200)
            else:
                print ("something went wrong when processing the event")
                return make_response("", 500)
    else:
        print("token did not match")
        return make_response("could not authenticate, token did not match", 403)


def event_processor(event_payload):
    """
    Function processing the actual event data
    Returning a success parameter to the event handler
    """
    event_type = event_payload["event"]["type"]

    if event_type == "message":

        # the event will have a subtype if it's an automated or bot message
        # ignoring those and exiting early to avoid infinite loops
        if "subtype" in event_payload["event"]:
            return True
        # other cases are messages posted by users, responding
        else:
            channel_id = event_payload["event"]["channel"]
            text = "Hi there! I'm a bot who can help users understand what channels are about.\nI won't be of much use here, but if you invite me to a channel I'll welcome users when they join it!"
            response = sc.api_call("chat.postMessage",
                                   channel=channel_id, text=text)
            # Slack API will return an "ok":True or "ok":False
            success = response.get("ok")
            return success

    elif event_type == "member_joined_channel":

        channel_id = event_payload["event"]["channel"]
        user_id = event_payload["event"]["user"]

        # Using the web API to get more info about the channel
        convo_info = sc.api_call("conversations.info", channel=channel_id)

        # checking that the call was sucessful and storring the data we're interested in
        if convo_info.get("ok") == True:
            topic = convo_info["channel"]["topic"]["value"]
            purpose = convo_info["channel"]["purpose"]["value"]
        else:
            topic, purpose = "error", "error"

        # building the message we want to send the user
        text = f"welcome to <#{channel_id}>! Here's the channel's topic: \n {topic} \n and the purpose: \n {purpose}"
        # sending an ephemeral message to the user who just joined the channel.
        attachments = [
            {
                "fallback": "open Slack to acknowledge",
                "callback_id": "ack",
                "actions": [
                    {
                        "name": "confirm",
                        "text": "confirm",
                        "type": "button",
                        "value": "confirm"
                    }
                ]
            }
        ]
        response = sc.api_call("chat.postEphemeral",
                               channel=channel_id, text=text, attachments=attachments, user=user_id)
        # Slack API will return an "ok":True or "ok":False
        success = response.get("ok")
        return success

    # event of an unexpected type, erroring
    else:
        return False
