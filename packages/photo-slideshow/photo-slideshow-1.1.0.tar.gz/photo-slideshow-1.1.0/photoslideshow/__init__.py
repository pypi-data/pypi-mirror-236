from configparser import SafeConfigParser
from importlib.resources import files
import os

eml_config = files('config').joinpath('photoslideshow_config.ini').read_text()

config = SafeConfigParser(os.environ)
config.read_string(eml_config)

# if config already exists for the user
if os.path.exists(config.get('path', 'userconfig')):
    config.read(config.get('path', 'userconfig'))
