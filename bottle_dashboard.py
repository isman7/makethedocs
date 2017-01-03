from dashboard import Dashboard
import bottle
import begin
import ConfigParser

cfg = ConfigParser.ConfigParser()
board = Dashboard()


@board.route('/')
@board.route('/home/')
@board.route('/home', name="main_page")
@board.page('main_menu')
def index():
    pass


@board.route('/page/', name="example")
@board.page('example')
def do_stuff():
    pass


@begin.start(auto_convert=True)
@begin.logging
def main(host='localhost', port='10010', config_path="dashboard_settings.ini"):

    cfg.read(config_path)
    board.set_config(cfg)

    board.main_menu.put("example", board.pages.get('example'))
    bottle.run(board, host=host, port=port, debug=True)


