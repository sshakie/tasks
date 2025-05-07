import re
import sys


def is_correct_mobile_phone_number_ru(s):
    remainder = ''
    # check that number begins with correct characters
    if s.startswith('+7'):
        remainder = s[2:]
    elif s.startswith('8'):
        remainder = s[1:]
    else:
        return False

    # cut off spaces and dashes
    remainder = re.sub(r'[ -]', '', remainder)

    # cut off correct parentheses
    if re.match(r'^\(\d{3}\)', remainder):
        remainder = re.sub(r'\(', '', remainder, 1)
        remainder = re.sub(r'\)', '', remainder, 1)

    # after that exactly 10 digits should left
    return bool(re.match(r'^\d{10}$', remainder))


sys.modules['inspect'] = None