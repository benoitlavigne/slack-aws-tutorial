import json
from urllib.parse import parse_qs

from lib.make_response import make_response


def button_handler(event, context):

    # When a user clicks a button, Slack sends a payload body parameter,
    # itself containing an application/x-www-form-urlencoded JSON string.
    # extracting this info and storing in a variable
    button_payload = json.loads(parse_qs(event.get("body"))["payload"][0])

    return button_processor(button_payload)


def button_processor(button_payload):

    user_id = button_payload["user"]["id"]

    response_body = {
        "text": f"<@{user_id}> Confirmed that they have read this channel's topic and purpose",
        "replace_original": False,
        "response_type": "in_channel"
    }

    return make_response(response_body, 200)
