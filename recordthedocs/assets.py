# -*- coding: utf-8 -*-
from flask.ext.assets import Bundle, Environment

css = Bundle(
    "libs/bootstrap/dist/css/bootstrap.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.js",
    "js/plugins.js",
    "libs/jqueryui/ui/jquery-ui.js",
    "libs/rangy/rangy-core.js",
    "libs/hallo/dist/hallo.js",
    "js/rst2html.js",
    "js/html2rst.js",
    "libs/markdown-browser-0.6.0-beta1/markdown.js",
    filters='jsmin',
    output="public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)