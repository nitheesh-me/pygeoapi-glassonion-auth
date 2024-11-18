import logging
import importlib
from typing import Any

from pygeoapi.plugin import load_plugin as load_plugin_from_base, InvalidPluginError

LOGGER = logging.getLogger(__name__)


PLUGINS = {
    'auth': {
        'Basic': 'pygeoapi_secure.auth.basic_auth.BasicAuth',
        'Session': 'pygeoapi_secure.auth.session_auth.SessionAuth',
        # 'Github': 'pygeoapi_secure.auth.github_auth.GithubAuth',
        # 'Google': 'pygeoapi_secure.auth.google_auth.GoogleAuth',
        # 'Azure': 'pygeoapi_secure.auth.azure_auth.AzureAuth',
        # 'LDAP': 'pygeoapi_secure.auth.ldap_auth.LDAPAuth',
    }
}


def load_plugin(plugin_type: str, plugin_def: dict) -> Any:
    """Choose plugin from list of available plugin or in the base list of plugins"""
    try:
        name = plugin_def['name']
        if plugin_type not in PLUGINS.keys():
            raise InvalidPluginError(f'Plugin type {plugin_type} not found')
        plugin_list = PLUGINS[plugin_type]
        if '.' not in name and name not in plugin_list.keys():
            raise InvalidPluginError(f'Plugin {name} not found')
        if '.' in name:  # dotted path
            packagename, classname = name.rsplit('.', 1)
        else:  # core formatter
            packagename, classname = plugin_list[name].rsplit('.', 1)

        LOGGER.debug(f'package name: {packagename}')
        LOGGER.debug(f'class name: {classname}')

        module = importlib.import_module(packagename)
        class_ = getattr(module, classname)
        plugin = class_(plugin_def)

        return plugin
    except (InvalidPluginError, KeyError) as e:
        LOGGER.exception(e)
        return load_plugin_from_base(plugin_type, plugin_def)
