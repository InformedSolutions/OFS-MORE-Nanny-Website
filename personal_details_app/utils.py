from urllib.parse import urlencode

from django.shortcuts import reverse


def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urlencode(get)
    return url


def app_id_finder(request):
    if request.GET.get('id'):
        app_id = request.GET.get('id')
    if request.POST.get('id'):
        app_id = request.POST.get('id')

    return(app_id)