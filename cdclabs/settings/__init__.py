# -*- coding: utf-8 -*-
import os
import sys
import socket
from django.utils.importlib import import_module


CURRENT_HOST = socket.gethostname()
HOST_MAP = {
    'development': 'mark-desktop',
    'production': 'hzcdclabs.org',
}
DISPATCHER = []

def update_settings(setting_type):
    """
    Given a filename, this function will insert all variables and functions
    in ALL_CAPS into the global scope.
    """
    settings = import_module('settings.%s' % setting_type)
    for k, v in settings.__dict__.items():
        if k.upper() == k:
            globals().update({k:v})

for k, v in HOST_MAP.items():
    if CURRENT_HOST == v:
        DISPATCHER.append(k)

for s in DISPATCHER:
    try:
        update_settings(s)
    except ImportError:
        print "Error importing %s" % s
