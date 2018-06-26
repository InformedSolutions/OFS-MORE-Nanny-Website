import random
import re
import string
import time

from urllib.parse import urlencode

from django import forms
from django.conf import settings
from django.shortcuts import reverse


def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urlencode(get)
    return url
