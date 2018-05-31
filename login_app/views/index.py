from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


def index(request):
    logger.info('Example log usage')
    return render(request, 'index.html')
