import re

_password_re = re.compile(r'\A(?=.*[a-zA-Z0-9]).{6,}\Z')

def is_password_valid(password):
    return _password_re.match(password)