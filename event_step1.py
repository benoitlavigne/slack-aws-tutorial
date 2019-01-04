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
        # ignoring those and exiting early, avoiding infinite loops
        if "subtype" in event_payload["event"]:
            return True
        # other cases are messages posted by users, responding
        else:
            channel_id = event_payload["event"]["channel"]
            text = "Hi there! I've received your message :tada:.\n Congratulations, you've finished the first branch of this workshop"
            response = sc.api_call("chat.postMessage",
                                   channel=channel_id, text=text)
            # Slack API will return an "ok":True or "ok":False
            success = response.get("ok")
            return success

    # Non "message" events are not expected, erroring
    else:
        return False
