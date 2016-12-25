from bottle import Bottle, template, static_file
import bottle
import os
import argparse
import begin


# Creating a Bottle app instance.
app = Bottle()

# Using os module to know were the server is running.
abspath = os.path.abspath(".")
print("The absolute path to server program is: {}".format(abspath))

# Bottle Functions start here


@app.route('/static/<path:path>')
def server_static(path):
    """
    Enables support to CSS, JS, images, etc. Links the public URL with the real server files and serve them.
    :param path: a valid local path in server.
    :return: returns the file to bottle app.
    """
    return static_file(path, root='/'.join([abspath, 'static']))


# @app.route('/empty/')
# def index(host="http://{}:{}".format(args.H, args.p)):
#     return template('starter', host=host)
#
#
# @app.route('/home/')
# def index(host="http://{}:{}".format(args.H, args.p)):
#     return template('index', host=host)


@app.route('/pid/')
def pid():
    """
    Auxiliar function that reports the PID of the subprocess running
    the Bottle server in order to kill it if necessary.
    :return: a plain htlm page with the PID
    """
    return str(os.getpid())


@app.error(404)
def error404(error):
    return 'Nothing here, sorry'


@begin.start(auto_convert=True)
def main(host: 'Host' = 'localhost', port: 'Port' = '8080'):
    """ Basic Bottle App with begins module. """
    bottle.run(app, host=host, port=port, debug=True)


