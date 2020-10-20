"""
ASGI config for essayCompTutors project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'essayCompTutors.settings')

application = get_asgi_application()
