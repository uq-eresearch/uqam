from django.utils.crypto import get_random_string


def gen_secret_key(len):
    """
    Generate a secret key of given length

    Exact same code as in django's startproject
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(len, chars)
