Title: Hello World
Date: 2023-05-22
save_as: 
url: helloworld.mu

<!-- 

The empty 'save_as' tag tells Pelican to not save this file
but use the given 'url' in all links that point to this
dummy article. We only use this to create links throughout
the generated page.

The following settings in 'pelicanconf.py' will then copy the
'helloworld.mu' script from the 'scripts' folder to where this
'url' points.

STATIC_PATHS = ['../scripts/helloworld.mu']
EXTRA_PATH_METADATA = {'../scripts/helloworld.mu': {'path': '/micron/helloworld.mu'},}

-->