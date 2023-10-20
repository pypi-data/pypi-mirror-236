#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sphinx.errors import ExtensionError


def add_cb_javascript(app, pagename, templatename, context, doctree):
    if not app.config.cookiebanner_enabled:
        metatags_string = context.get('metatags','')
        headercode = """ <!-- Cookie Banner Intentionally Disabled --> """
        context['metatags'] = metatags_string + headercode
        return
    
    # Embed code into the header, using the "metatags" space.
    metatags_string = context.get('metatags','')
    headercode = """
       <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.css" />
    """
    context['metatags'] = metatags_string + headercode
    
    # Embed code into the body, using the "body" space.
    body_string = context.get('body','')
    bodycode = """
       <script src="https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.js" data-cfasync="false"></script>
       <script>
          window.cookieconsent.initialise({
             "palette": {
                "popup": {
                   "background": "#000000",
                   "text": "#ffffff"
                },
                "button": {
                   "background": "#ffffff",
                   "text": "#000000"
                }
             },
             "theme": "classic",
             "position": "top",
             "content": {
                "message": "This website uses cookies to improve user experience. By using our website you consent to all cookies in accordance with the <i>FIRST</i> Privacy Policy.",
                "href": "https://www.firstinspires.org/about/privacy-policy"
             }
          });
       </script>
    """
    context['body'] = body_string + bodycode

    
def setup(app):
    app.add_config_value('cookiebanner_enabled', True, 'html')
    app.connect('html-page-context', add_cb_javascript)

