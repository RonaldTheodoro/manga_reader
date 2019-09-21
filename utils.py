#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib.parse

import lxml.html
import requests


def create_directory(directory):
    """Checks if a directory exists and if not create it.

    Args:
        directory (str): Directory path.
    """
    if not os.path.exists(directory):
        os.mkdir(directory)


def create_html_element_instance(response, base_url):
    """Create a HtmlElement instance with the site response.

    Args:
        response (requests.models.Response): Page response.

    Returns:
        lxml.html.HtmlElement: HTML Element.
    """
    root = lxml.html.fromstring(response.text, base_url=base_url)
    root.make_links_absolute()
    return root


def is_url(url):
    """Checks if it is a valid URL

    Args:
        url (str): URL string.

    Returns:
        bool: Returns true if it is a valid URL.
    """
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
