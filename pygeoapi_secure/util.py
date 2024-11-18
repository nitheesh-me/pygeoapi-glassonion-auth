"""Currently incompatable functions with pygeoapi"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from flask import session
from babel.support import Translations
from pygeoapi import __version__
from pygeoapi import l10n
from pygeoapi.util import (
    LOGGER, TEMPLATES,
    to_json, format_datetime, format_duration, human_size, get_path_basename, get_breadcrumbs, filter_dict_by_key_value
)

THISDIR = Path(__file__).parent.resolve()
NEW_TEMPLATES = THISDIR / 'templates'

def render_j2_template(config: dict, template: Path,
                       data: dict, locale_: str|None = None) -> str:
    """
    Change from previous version at
    https://github.com/geopython/pygeoapi/blob/2e4ff714f6ca090d6cc294d5d03e7ad550d38608/pygeoapi/util.py#L429C1-L479C75
    """

    template_paths = [NEW_TEMPLATES, TEMPLATES, '.']            # Need a hook here for library to add custom templates

    locale_dir = config['server'].get('locale_dir', 'locale')
    LOGGER.debug(f'Locale directory: {locale_dir}')

    try:
        templates = config['server']['templates']['path']
        template_paths.insert(0, templates)
        LOGGER.debug(f'using custom templates: {templates}')
    except (KeyError, TypeError):
        LOGGER.debug(f'using default templates: {TEMPLATES}')

    env = Environment(loader=FileSystemLoader(template_paths),
                      extensions=['jinja2.ext.i18n'],
                      autoescape=select_autoescape())

    env.filters['to_json'] = to_json
    env.filters['format_datetime'] = format_datetime
    env.filters['format_duration'] = format_duration
    env.filters['human_size'] = human_size
    env.globals.update(to_json=to_json)

    env.filters['get_path_basename'] = get_path_basename
    env.globals.update(get_path_basename=get_path_basename)

    env.filters['get_breadcrumbs'] = get_breadcrumbs
    env.globals.update(get_breadcrumbs=get_breadcrumbs)

    env.filters['filter_dict_by_key_value'] = filter_dict_by_key_value
    env.globals.update(filter_dict_by_key_value=filter_dict_by_key_value)

    translations = Translations.load(locale_dir, [locale_])
    env.install_gettext_translations(translations)

    template = env.get_template(template)

    assert 'session' not in data
    data['session'] = session

    return template.render(config=l10n.translate_struct(config, locale_, True),
                           data=data, locale=locale_, version=__version__)

# update pygeoapi.util.render_j2_template with new function (internal modification)
def enable_mock():
    from unittest.mock import patch
    patch('pygeoapi.util.render_j2_template', render_j2_template).start()

    import atexit
    atexit.register(patch.stopall)