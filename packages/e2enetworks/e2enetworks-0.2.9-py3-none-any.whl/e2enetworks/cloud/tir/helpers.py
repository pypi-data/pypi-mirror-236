import string
import random


def get_random_string(N):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
