from bottle import Bottle, template, static_file, url, route, error, view
from collections import OrderedDict
import bottle
import os
import begin
import configparser
import logging


# AdminLTE constructors
class dashboard(object):
    def __init__(self, **kwargs):
        self.bottle = kwargs.pop("bottle", Bottle())
        self.main_menu = kwargs.pop("menu", dashboard_menu())
        self.user_profile = kwargs.pop("user", None)
        self.tree = kwargs.pop("tree", dashboard_tree())
        self.config = kwargs.pop("config", configparser.ConfigParser())
        if not self.config.sections():
            self.config.read(kwargs.pop("config_file", "dashboard_settings.ini"))

    def get_render_dict(self, **kwargs):
        page = kwargs.get("page", None)
        return {"url": kwargs.get("url", self.bottle.get_url),
                "color": self.config.get("layout", "color"),
                "layout_options": self.config.get("layout", "options"),
                "sidebar_menu": self.main_menu.render(**kwargs),
                "page_content": self.tree.get(page, dashboard_page()).render()}



class dashboard_page(object):
    def __init__(self, **kwargs):
        self.title = kwargs.pop("title", "Default page")
        self.name = kwargs.pop("name", "default-page")
        self.icon = kwargs.pop("icon", "fa fa-link")
        self.url = kwargs.pop("url", "#")
        self.content = kwargs.pop("content", "The content")

    def render(self):
        return self.content


class dashboard_tree(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(dashboard_tree, self).__init__(*args, **kwargs)

    def put(self, key, item, **kwargs):
        self.__setitem__(key, item, **kwargs)


class dashboard_menu(OrderedDict):
    def __init__(self, *args, **kwargs):
        self.bottle = kwargs.pop("bottle", Bottle())
        self.title = kwargs.pop("title", "Main menu")
        self.name = kwargs.pop("name", "main-menu")
        super(dashboard_menu, self).__init__(*args, **kwargs)

    def put(self, key, item, **kwargs):
        self.__setitem__(key, item, **kwargs)

    def render(self, **kwargs):
        active = kwargs.pop("page", None)
        url = kwargs.pop("url", self.bottle.get_url)
        # entry_tpl = """
        # <li class="{0}"><a href="{1}"><i class="{2}"></i><span>{3}</span></a></li>
        # """
        # entries = []
        # for label, mpage in self.items():
        #     li_classes = []
        #     if active == label:
        #         li_classes.append("active")
        #     # if menu_page.subpages:
        #     #     li_classes.append("treeview")
        #     entries.append(entry_tpl.format(' '.join(li_classes),
        #                                     mpage.url,
        #                                     mpage.icon,
        #                                     mpage.title)
        #                    )

        # return menu_tpl.format(self.title, "".join(entries))
        print(self.bottle.router.builder)
        return template("menu",
                        url=url,
                        active_page=active,
                        title=self.title,
                        entries=self.items())



# The server routine starts here:
abspath = os.path.abspath(".")
print("The absolute path to server program is: {}".format(abspath))

app = Bottle()

menu = dashboard_menu(bottle=app)
board = dashboard(bottle=app, main_menu=menu)


@app.route('/static/<filepath:path>', name="static")
def server_static(filepath):
    """
    Enables support to CSS, JS, images, etc. Links the public URL with the real server files and serve them.
    :param filepath: a valid local path in server.
    :return: returns the file to bottle app.
    """
    return static_file(filepath, root=os.path.join(abspath, 'static'))


@app.route('/')
@app.route('/home/', name="home")
def index():
    print(board.bottle.router.builder)
    return template('base_dashboard', board.get_render_dict(page="the_page", url=app.get_url))


@app.route('/facebook/', name="facebook")
@view("base_dashboard")
def index():
    return board.get_render_dict(page="a_page", url=app.get_url)

@app.route('/home/2/')
def index():
    return template('index', url=url)


@app.error(404)
def error404(error):
    return 'Nothing here, sorry'


@begin.start(auto_convert=True)
@begin.logging
def main(host: 'Host' = 'localhost', port: 'Port' = '8080'):

    board.main_menu.put("the_page", dashboard_page(url="home"))
    board.main_menu.put("a_page", dashboard_page(icon="fa fa-facebook", url="facebook"))

    """ Basic Bottle App with begins module. """
    bottle.run(board.bottle, host=host, port=port, debug=True)


