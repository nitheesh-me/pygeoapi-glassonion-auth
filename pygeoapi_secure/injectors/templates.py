from pathlib import Path


def add_template_location(config: dict, template_folder: Path|str):
    """
    Adds a new template folder to pygeoapi's configuration.

    :param app: The Flask application instance.
    :param template_folder: The path to the new template folder.
    """
    if not isinstance(template_folder, Path):
        template_folder = Path(template_folder)
    if not template_folder.exists():
        raise FileNotFoundError(f'The template folder {template_folder} does not exist.')
    if not template_folder.is_dir():
        raise NotADirectoryError(f'The template folder {template_folder} is not a directory.')
    if 'server' not in config or 'templates' not in config['server']:
        config['server'] = {'templates': {}}
    config['server']['templates']['path'] = str(template_folder)
    return config
