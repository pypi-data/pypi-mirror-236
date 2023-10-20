.. -*- restructuredtext -*-

===========================================
Cookie Banner extension for Sphinx
===========================================

:author: Danny Diaz <ddiaz@firstinspires.org>

About
=====

This extensions allows you to add a cookie banner to 
your website. This uses the Cookie Consent code found
here:  
https://www.osano.com/cookieconsent/documentation/about-cookie-consent/

Enabling the extension in Sphinx_
---------------------------------

Just add ``sphinxcontrib.cookiebanner` to the list of extensions in the ``conf.py``
file. For example::

    extensions = ['sphinxcontrib.cookiebanner']


Configuration
-------------

For now one optional configuration is added to Sphinx_. It can be set in
``conf.py`` file:

``cookiebanner_enabled`` <bool>:
	True by default, use it to turn off the cookiebanner.

