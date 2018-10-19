import random
import re
import string
import time

from urllib.parse import urlencode

from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urlencode(get)
    return url


def get_form_class(self):
    """
    Returns the form class to use in this view
    """
    return self.form_class


def get_form(self, form_class=None):
    """
    Returns an instance of the form to be used in this view.
    """
    if form_class is None:

        form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())


def form_valid(self, form):
    """
    If the form is valid, redirect to the supplied URL.
    """
    return HttpResponseRedirect(self.get_success_url())