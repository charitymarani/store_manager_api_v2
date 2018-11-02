import re
from flask import jsonify
def list_iterator(list_):
    for listitem in list_:
        if listitem is None or not listitem:
            return False


def check_is_int(list_):
    for listitem in list_:
        if isinstance(listitem,int):
            return True
        return jsonify({"message":"{} must be an of integer format".format(listitem)}),400

def validate_password(password, confirm_password):
        '''method checking pasword requirements'''
        special_character_regex=r'[0-9~!@#$%^&*()_-`{};:\'"\|/?.>,<]'
        error = {}
        if confirm_password != password:
            error["message"] = "The passwords you entered don't match"
        if bool(re.search(r'[A-Z][a-z]|[a-z][A-Z]', password)) is False:
            error["message"] = "password must contain a mix of upper and lowercase letters"
        if bool(re.search(special_character_regex, password)) is False:
            error["message"] = "password must contain atleast one numeric or special character"
        if len(password) < 6:
            error["message"] = "The password is too short,minimum length is 6"
        if "message" in error:
            return error
        return password