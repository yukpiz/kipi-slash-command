# -*- coding: utf-8 -*-

import urlparse
import boto3
import json

def lambda_handler(event, context):
    parameters = parse_token(event["body"])
    payload = command(parameters)
    return { "statusCode": 200, "body": json.dumps(payload) }

def parse_token(token):
    parsed = urlparse.parse_qs(token)
    args = parsed["text"][0].split(" ")
    return {
        "user_id": parsed["user_id"][0],
        "channel_id": parsed["channel_id"][0],
        "image_url": args[0],
        "emoji_name": args[1],
        "response_url": parsed["response_url"][0],
        "team_id": parsed["team_id"][0],
        "channel_name": parsed["channel_name"][0],
        "token": parsed["token"][0],
        "command": parsed["command"][0],
        "team_domain": parsed["team_domain"][0],
        "user_name": parsed["user_name"][0],
    }

def command(parameters):
    if parameters["command"] == "/emojisan":
        payload = json.dumps(parameters)
        response = boto3.client("lambda").invoke(
            FunctionName="kipi-emoji-san",
            InvocationType="Event",
            Payload=payload
        )
        return {
            "text": "Thanks %s! Now uploading your emoji." % parameters["user_name"]
        }
    else:
        return {
            "text": "Not supported command: %s" % parameters["command"]
        }