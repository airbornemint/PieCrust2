
CACHE_DIR = '_cache'
ASSETS_DIR = 'assets'
TEMPLATES_DIR = 'templates'
PLUGINS_DIR = 'plugins'
THEME_DIR = 'theme'

CONFIG_PATH = 'config.yml'
THEME_CONFIG_PATH = 'theme_config.yml'

DEFAULT_FORMAT = 'markdown'
DEFAULT_TEMPLATE_ENGINE = 'jinja2'
DEFAULT_POSTS_FS = 'flat'
DEFAULT_DATE_FORMAT = '%b %d, %Y'
DEFAULT_PLUGIN_SOURCE = 'http://bitbucket.org/ludovicchabant/'
DEFAULT_THEME_SOURCE = 'http://bitbucket.org/ludovicchabant/'

PIECRUST_URL = 'http://bolt80.com/piecrust/'

try:
    from piecrust.__version__ import APP_VERSION
except ImportError:
    APP_VERSION = 'unknown'

