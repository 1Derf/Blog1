import importlib

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        signals = importlib.import_module('users.signals')
