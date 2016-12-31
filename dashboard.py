from __future__ import unicode_literals
from bottle import Bottle, template
from collections import OrderedDict
import logging
try:
    import ConfigParser as cfp
except ImportError:
    import configparser as cfp


class Dashboard(Bottle):
    def __init__(self, *args, **kwargs):
        self.main_menu = kwargs.pop("main_menu", menu())
        self.user_profile = kwargs.pop("user", None)
        self.pages = kwargs.pop("tree", tree())
        self.board_config = kwargs.pop("board_config", cfp.ConfigParser())
        if not self.board_config.sections():
            self.board_config.read(kwargs.pop("config_file", "dashboard_settings.ini"))
        super(Dashboard, self).__init__(*args, **kwargs)

    def render_dict(self, **kwargs):
        the_page = kwargs.get("page", None)
        url = kwargs.pop("url", self.get_url)
        return {"url": url,
                "title": self.board_config.get("DEFAULT", "title"),
                "description": self.board_config.get("DEFAULT", "description"),
                "color": self.board_config.get("layout", "color"),
                "layout_options": self.board_config.get("layout", "options"),
                "sidebar_menu": self.main_menu.render(url=url, **kwargs),
                "page": self.pages.get(the_page, page()).render()}

    def register_page(self, **kwargs):
        the_page = self.pages.get(kwargs.get("page_name"))
        the_menu = kwargs.get("menu", self.main_menu)
        logging.info(page)
        the_menu.put(the_page.name, the_page)
        return the_menu


class page(object):
    def __init__(self, **kwargs):
        self.bottle = kwargs.pop("bottle", None)
        self.title = kwargs.pop("title", "Default page")
        self.description = kwargs.pop("description", "A single page")
        self.name = kwargs.pop("name", "default-page")
        self.icon = kwargs.pop("icon", "fa fa-link")
        self.url = kwargs.pop("url", "#")
        self.content = kwargs.pop("content", "The content")

    def render(self):
        return template("page",
                        title=self.title,
                        description=self.description,
                        page_content=self.content)


class tree(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(tree, self).__init__(*args, **kwargs)

    def put(self, key, item, **kwargs):
        self.__setitem__(key, item, **kwargs)


class menu(OrderedDict):
    def __init__(self, *args, **kwargs):
        self.bottle = kwargs.pop("bottle", None)
        self.title = kwargs.pop("title", "Main menu")
        self.name = kwargs.pop("name", "main-menu")
        super(menu, self).__init__(*args, **kwargs)

    def put(self, key, item, **kwargs):
        self.__setitem__(key, item, **kwargs)

    def render(self, **kwargs):
        active = kwargs.pop("page", None)
        url = kwargs.pop("url")
        return template("menu",
                        url=url,
                        active_page=active,
                        title=self.title,
                        entries=self.items())
