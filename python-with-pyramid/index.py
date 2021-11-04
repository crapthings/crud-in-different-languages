from pyramid.config import Configurator
from pyramid.response import Response, response_adapter
from pyramid.view import view_config
from pyramid.handlers import action
from wsgiref.simple_server import make_server

users = [0] * 10

@view_config(route_name='index', request_method='GET')
def index(request):
  return Response('python with pyramid')

@view_config(route_name='getUsers', request_method='GET', renderer='json')
def getUsers(request):
  return users

@view_config(route_name='createUser', request_method='POST', renderer='json')
def createUser(request):
  return users

class Hello(object):
  __autoexpose__ = None

  def __init__(self, request):
    self.request = request

  @action
  def index(self):
    return Response('Hello world!')

  @action(renderer="mytemplate.mak")
  def bye(self):
    return {}

if __name__ == '__main__':
  with Configurator() as config:
    config.include("pyramid_handlers")
    config.add_handler("hello", "/api/users", handler=Hello)
    config.add_route('index', '/')
    config.add_route('getUsers', '/api/users')
    config.add_route('createUser', '/api/users')
    config.scan()
    app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 3000, app)
  server.serve_forever()
