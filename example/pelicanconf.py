AUTHOR = 'Node Nomad'
SITENAME = 'Micron Blog'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'UTC'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Micron related settings
PLUGIN_PATHS = ["../plugin"]
PLUGINS = ['micron']
THEME = '../theme'
MICRON_PATH = 'output/micron'
