import json
from flask import jsonify


class Json_Data():
    def __init__(self, json_data):
        self.__data = json.loads(json_data)
        self.__response = {'success': False}

    def get_data(self):
        return self.__data

    def get_response(self):
        return self.__response

    def get_response_for_key(self, key):
        if key in self.__response.keys():
            return self.__response[key]
        else:
            return None

    def set_response(self, key, key_String):
        self.__response[key] = key_String

    def get_response_to_views(self):
        return jsonify(self.__response)
