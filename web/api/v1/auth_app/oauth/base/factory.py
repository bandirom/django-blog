from collections import OrderedDict
from typing import Type

from .provider import OAuth2Provider


class ProviderRegistry(object):
    def __init__(self):
        self.provider_map = OrderedDict()
        self.loaded = False

    def get_classes(self):
        return [{'name': name} for name, cls in self.provider_map.items() if cls().enabled]

    def register(self, cls):
        self.provider_map[cls.name] = cls

    def get_class(self, provider_name: str) -> Type[OAuth2Provider]:
        return self.provider_map.get(provider_name)

    def as_choices(self):
        return [(provider_cls.name, provider_cls.name.capitalize()) for provider_cls in self.provider_map.values()]


provider_registry = ProviderRegistry()
