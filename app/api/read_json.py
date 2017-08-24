import json
from .config import ERROR
from flask import jsonify


class Read_Json():
    def __init__(self, json_data):
        self.__raw_data = json_data
        self.__data = None
        self.__response = {'errorCode': None, 'errorMessage': None}
        self.test_json_data()

    def test_json_data(self):
        try:
            self.__data = json.loads(self.__raw_data)
        except Exception as e:
            self.set_response(ERROR[1])

    def get_data(self):
        return self.__data

    def get_response(self):
        return self.__response

    def get_response_of_key(self, key):
        if key in self.__response.keys():
            return self.__response[key]
        else:
            return None

    def add_response(self, key, key_string):
        self.__response[key] = key_string

    def add_response_wechat(self, key, key_string):
        if key not in self.__response.keys():
            self.__response={'errorCode': None, 'errorMessage': None,key:[]}
        print(self.__response[key])
        self.__response[key].append(key_string)

    def set_response(self, key):
        self.__response['errorCode'] = key['errorCode']
        self.__response['errorMessage'] = key['errorMessage']

    def get_response_to_views(self):
        return jsonify(self.__response)
