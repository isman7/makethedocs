from __future__ import unicode_literals
from bottle import Bottle, static_file, view, request
from dashboard import Dashboard, page
import bottle
import os
import begin


# The server routine starts here:
abspath = os.path.abspath(".")
print("The absolute path to server program is: {}".format(abspath))

# menu = dashboard_menu(bottle=app)
board = Dashboard()


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
@view('dashboard')
def index():
    return board.render_dict(page="home")


@board.route('/facebook/', name="facebook")
@view('dashboard')
def facebook():
    return board.render_dict(page="social")


@board.route('/search', name='search')
@view('dashboard')
def search():
    return board.render_dict(page="search_page")

@board.route('/chart', name='chart')
@view('dashboard_test_chartjs')
def chart():
    return board.render_dict(page="chart")


@board.route('/search', name='search', method='POST')
@view('dashboard')
def search():
    """
    Do search stuff. In this example the query is rendered as plain text inside the page.
    """
    search_string = request.forms.get("s")
    search_page = board.pages.get("search_page", page(url="search"))
    search_page.content = search_string
    board.pages.put("search_page", search_page)
    return board.render_dict(page="search_page")


@board.error(404)
def error404(error):
    return 'Nothing here, sorry'


@begin.start(auto_convert=True)
@begin.logging
def main(host='localhost', port='10010'):

    board.pages.put("home", page(url="home",
                                 icon="fa fa-home",
                                 name="home",
                                 title="Home page",
                                 content="This is my main page."))
    board.pages.put("social", page(url="facebook",
                                   icon="fa fa-facebook",
                                   name="social",
                                   title="Facebook account",
                                   content="Link to Facebook maybe?"))
    board.pages.put("search_page", page(url="search",
                                        name="search",
                                        title="Search"))

    board.pages.put("chart", page(url="chart",
                                    icon="fa fa-pie-chart",
                                    name="chart",
                                    title="ChartJS"))

    board.register_page(page_name="home")
    board.register_page(page_name="social")
    board.register_page(page_name="chart")

    board.pages.get("chart").content = """
<div class="box box-danger">
    <div class="box-header with-border">
      <h3 class="box-title">Donut Chart</h3>

      <div class="box-tools pull-right">
        <button type="button" class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-minus"></i>
        </button>
        <button type="button" class="btn btn-box-tool" data-widget="remove"><i class="fa fa-times"></i></button>
      </div>
    </div>
    <div class="box-body">
      <canvas id="pieChart" style="height:250px"></canvas>
    </div>
    <!-- /.box-body -->
</div>
    """

    bottle.run(board, host=host, port=port, debug=True)


