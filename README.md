# micron-blog

Pelican Plug-In and Theme for publishing a site in Micron markup format for Nomad Network Nodes

## Installation

Install dependencies

```
$ pip3 install -r requirements.txt
```

## Create a Static Site from Scratch

Use the `example` folder as a starting point...

+ Write your content in markdown formatted files and place them in the `content` folder
+ Edit the micron formatted Jinja2 templates in `theme/templates` to your liking
+ Generate the blog by running the following command in the `example` folder:

```
$ pelican content
```

## Use alongside an existing Pelican installation

+ Copy the theme and plugin to your Pelican site's folder
+ Duplicate your `pelicanconf.py` file to something like `micronconf.py`
+ Edit the new file and make sure Pelican can find the new folders by adding them to the `PLUGIN_PATHS` and editing the `THEME` and `PLUGINS` variables respectively
+ If you want to place the micron .mu files in a different output folder than your generated HTML files, specify a path in a variable called `MICRON_PATH`
+ Make sure `RELATIVE_URLS` is set to `True`
+ Make sure all Links in your Markdown articles and pages are relative and local, since you will not be able to access http links inside Nomad Network

Example Settings, vary depending on your setup:

```Python
PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ['micron']
THEME = 'micron-theme'
MICRON_PATH = 'micron_out'
RELATIVE_URLS = True
```

Generate the Micron pages by pointing Pelican to the Micron config file:

```
$ pelican content -s micronconf.py
```

## Deployment

If you have not run Nomad Network yet, initialize the needed folder by running `nomadnet` once

```
$ nomadnet
```

Copy the generated .mu files from the output folder to the NN node's `pages` folder:
```
$ cp -R output/* ~/.nomadnetwork/storage/pages
```

Run your node and serve the pages....