__all__ = ["ProviderNotRegistered"]

from pygeoapi.provider.base import ProviderGenericError


class ProviderNotRegistered(ProviderGenericError):
    default_msg = 'Provider not registered'


class IdentityNotValid(Exception):
    pass