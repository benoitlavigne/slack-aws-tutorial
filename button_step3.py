import json
from urllib.parse import parse_qs
import botocore.vendored.requests as requests

from lib.make_response import make_response


def button_handler(event, context):

    # When a user clicks a button, Slack sends a payload body parameter,
    # itself containing an application/x-www-form-urlencoded JSON string.
    # extracting this info and storing in a variable
    button_payload = json.loads(parse_qs(event.get("body"))["payload"][0])

    return button_processor(button_payload)


def button_processor(button_payload):

    user_id = button_payload["user"]["id"]
    response_url = button_payload["response_url"]

    response_payload = {
        "text": f"<@{user_id}> Confirmed that they have read this channel's topic and purpose",
        "replace_original": False,
        "response_type": "in_channel"
    }

    r = requests.post(response_url, json=response_payload)

    if r.json().get("ok") == True:
        return make_response("ok", 200)
    else:
        return make_response("error posting to Slack", 500)
