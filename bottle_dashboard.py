from bottle import Bottle, template, static_file, url, route, error, view, request
from collections import OrderedDict
import bottle
import os
import begin
import configparser
import logging


# AdminLTE constructors
class dashboard(Bottle):
    def __init__(self, *args, **kwargs):
        self.main_menu = kwargs.pop("main_menu", dashboard_menu())
        self.user_profile = kwargs.pop("user", None)
        self.pages = kwargs.pop("tree", dashboard_tree())
        self.board_config = kwargs.pop("board_config", configparser.ConfigParser())
        if not self.board_config.sections():
            self.board_config.read(kwargs.pop("config_file", "dashboard_settings.ini"))
        super(dashboard, self).__init__(*args, **kwargs)

    def render_dict(self, **kwargs):
        page = kwargs.get("page", None)
        url = kwargs.pop("url", self.get_url)
        return {"url": url,
                "color": self.board_config.get("layout", "color"),
                "layout_options": self.board_config.get("layout", "options"),
                "sidebar_menu": self.main_menu.render(url=url, **kwargs),
                "page": self.pages.get(page, dashboard_page()).render()}

    def page_to_menu(self, **kwargs):
        page = self.pages.get(kwargs.get("page_name"))
        logging.info(page)
        self.main_menu.put(page.name, page)
        return self.main_menu




class dashboard_page(object):
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


class dashboard_tree(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(dashboard_tree, self).__init__(*args, **kwargs)

    def put(self, key, item, **kwargs):
        self.__setitem__(key, item, **kwargs)


class dashboard_menu(OrderedDict):
    def __init__(self, *args, **kwargs):
        self.bottle = kwargs.pop("bottle", None)
        self.title = kwargs.pop("title", "Main menu")
        self.name = kwargs.pop("name", "main-menu")
        super(dashboard_menu, self).__init__(*args, **kwargs)

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



# The server routine starts here:
abspath = os.path.abspath(".")
print("The absolute path to server program is: {}".format(abspath))

app = Bottle()

# menu = dashboard_menu(bottle=app)
board = dashboard()


@board.route('/static/<filepath:path>', name="static")
def server_static(filepath):
    """
    Enables support to CSS, JS, images, etc. Links the public URL with the real server files and serve them.
    :param filepath: a valid local path in server.
    :return: returns the file to bottle app.
    """
    return static_file(filepath, root=os.path.join(abspath, 'static'))


@board.route('/')
@board.route('/home/', name="home")
@view('base_dashboard')
def index():
    return board.render_dict(page="home")


@board.route('/facebook/', name="facebook")
@view('base_dashboard')
def facebook():
    return board.render_dict(page="social")

@board.route('/search', name='search')
@view('base_dashboard')
def search():
    return board.render_dict(page="search_page")

@board.route('/search', name='search', method='POST')
@view('base_dashboard')
def search():
    # do search stuff
    search_string = request.forms.get("s")
    search_page = board.pages.get("search_page", dashboard_page(url="search"))
    search_page.content = search_string
    board.pages.put("search_page", search_page)
    return board.render_dict(page="search_page")


@board.error(404)
def error404(error):
    return 'Nothing here, sorry'


@begin.start(auto_convert=True)
@begin.logging
def main(host: 'Host' = 'localhost', port: 'Port' = '10010'):

    board.pages.put("home", dashboard_page(url="home",
                                           icon="fa fa-home",
                                           name="home",
                                           title="Home page",
                                           content="This is my main page."))
    board.pages.put("social", dashboard_page(url="facebook",
                                             icon="fa fa-facebook",
                                             name="social",
                                             title="Facebook account",
                                             content="Link to Facebook maybe?"))
    board.pages.put("search_page", dashboard_page(url="search",
                                                  name="search",
                                                  title="Search"))

    board.page_to_menu(page_name="home")
    board.page_to_menu(page_name="social")

    """ Basic Bottle App with begins module. """
    bottle.run(board, host=host, port=port, debug=True)


