from bottle import Bottle, template, static_file, url, route, error
from collections import OrderedDict
import bottle
import os
import begin
# import logging


# AdminLTE constructors
class dashboard(object):
    def __init__(self, **kwargs):
        self.menu = kwargs.pop("menu", dashboard_menu())


class page(object):
    def __init__(self, **kwargs):
        self.title = kwargs.pop("title", "Default page")
        self.name = kwargs.pop("name", "default-page")
        self.icon = kwargs.pop("icon", "fa fa-link")
        self.url = kwargs.pop("url", "#")
        self.subpages = None


class dashboard_menu(OrderedDict):
    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop("title", "Main menu")
        self.name = kwargs.pop("name", "main-menu")
        super(dashboard_menu, self).__init__(*args, **kwargs)

    def put(self, key, item, **kwargs):
        self.__setitem__(key, item, **kwargs)

    def render(self, active=None):
        entry_tpl = """
        <li class="{0}"><a href="{1}"><i class="{2}"></i><span>{3}</span></a></li>
        """
        menu_tpl = """
<ul class="sidebar-menu">
    <li class="header">{0}</li>
    {1}
</ul>
        """
        entries = []
        for label, mpage in self.items():
            li_classes = []
            if active == label:
                li_classes.append("active")
            # if menu_page.subpages:
            #     li_classes.append("treeview")
            entries.append(entry_tpl.format(' '.join(li_classes),
                                            mpage.url,
                                            mpage.icon,
                                            mpage.title)
                           )
        print(entries)
        return menu_tpl.format(self.title, "".join(entries))


menu = dashboard_menu()


# The server routine starts here:
abspath = os.path.abspath(".")
print("The absolute path to server program is: {}".format(abspath))

app = Bottle()

@app.route('/static/<filepath:path>', name="static")
def server_static(filepath):
    """
    Enables support to CSS, JS, images, etc. Links the public URL with the real server files and serve them.
    :param filepath: a valid local path in server.
    :return: returns the file to bottle app.
    """
    return static_file(filepath, root=os.path.join(abspath, 'static'))

@app.route('/empty/')
def index():
    return template('starter', url=app.get_url)


@app.route('/')
def index():
    return template('base_dashboard',
                    url=app.get_url,
                    color="red",
                    layout_options="sidebar-collapse sidebar-mini layout-boxed",
                    sidebar_menu=menu.render())

@app.route('/home/2/')
def index():
    return template('index', url=url)


@app.error(404)
def error404(error):
    return 'Nothing here, sorry'


@begin.start(auto_convert=True)
@begin.logging
def main(host: 'Host' = 'localhost', port: 'Port' = '8080'):

    menu.put("the_page", page())
    menu.put("a_page", page(icon="fa fa-facebook"))

    """ Basic Bottle App with begins module. """
    bottle.run(app, host=host, port=port, debug=True)


