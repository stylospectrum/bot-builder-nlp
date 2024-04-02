import json

from google.protobuf.json_format import MessageToJson


def get_json_list(msg_list: list):
    return [
        json.loads(MessageToJson(expr, preserving_proto_field_name=True))
        for expr in msg_list
    ]
