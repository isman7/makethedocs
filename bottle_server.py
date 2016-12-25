from bottle import Bottle, template, static_file, url, route, error
import bottle
import os
import logging
import begin


# Using os module to know were the server is running.
abspath = os.path.abspath(".")
print("The absolute path to server program is: {}".format(abspath))

# Bottle Functions start here

#
# def get_template_uri

@route('/static/<filepath:path>', name="static")
def server_static(filepath):
    """
    Enables support to CSS, JS, images, etc. Links the public URL with the real server files and serve them.
    :param filepath: a valid local path in server.
    :return: returns the file to bottle app.
    """
    return static_file(filepath, root=os.path.join(abspath, 'static'))

@route('/empty/')
def index():
    return template('starter', url=url)


@route('/home/')
def index():
    return template('index', url=url)

@route('/home/2/')
def index():
    return template('index', url=url)


@error(404)
def error404(error):
    return 'Nothing here, sorry'


@begin.start(auto_convert=True)
@begin.logging
def main(host: 'Host' = 'localhost', port: 'Port' = '8080'):
    """ Basic Bottle App with begins module. """
    bottle.run(host=host, port=port, debug=True)


