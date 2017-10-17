# -*- coding: utf-8 -*-

import json
import urlparse
import requests
from PIL import Image
from StringIO import StringIO

def lambda_handler(event, context):
    print("-----------------------")
    print(event)
    print("-----------------------")

    parameters = parse_token(event["body"])
    payload = command(parameters)

    return { "statusCode": 200, "body": json.dumps(payload) }

def parse_token(token):
    parsed = urlparse.parse_qs(token)
    return {
        "user_id": parsed["user_id"][0],
        "channel_id": parsed["channel_id"][0],
        "text": parsed["text"][0],
        "response_url": parsed["response_url"][0],
        "team_id": parsed["team_id"][0],
        "channel_name": parsed["channel_name"][0],
        "token": parsed["token"][0],
        "command": parsed["command"][0],
        "team_domain": parsed["team_domain"][0],
        "user_name": parsed["user_name"][0],
    }

def command(parameters):
    print(parameters)
    if parameters["command"] == "/emojisan":
        return command_emojisan(parameters)
    else:
        return {
            "text": "Not supported command: %s" % parameters["command"]
        }

def command_emojisan(parameters):
    print(parameters)
    image = download_image(parameters["text"])
    image = resize_image(image)
    return {
        "text": "Emoji Sanです %s" % parameters["text"]
    }

def download_image(url):
    print(url)
    response = requests.get(url)
    print(response.status_code)
    return Image.open(StringIO(response.content))

def resize_image(image):
    image.thumbnail((128, 128), Image.ANTIALIAS)
    return image
