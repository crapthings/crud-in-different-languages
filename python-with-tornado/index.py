import tornado.web
import tornado.ioloop
from tornado.httpserver import HTTPServer
from tornado.routing import RuleRouter, Rule, PathMatches
import ujson
from faker import Faker

fake = Faker()

def createUser(idx):
  return {
    '_id': idx,
    'fullname': fake.name(),
    'email': fake.email(),
  }

users = [createUser(0)] * 10

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    self.write('python with tornado')

class UsersHandler(tornado.web.RequestHandler):
  def get(self):
    self.write(dict(results=users))

  def post(self):
    user = createUser(users[len(users) - 1]['_id'] + 1)
    users.append(user)
    self.write(user)

  def put(self):
    user = createUser(users[len(users) - 1]['_id'] + 1)
    users.append(user)
    self.write(user)

  def delete(self):
    user = createUser(users[len(users) - 1]['_id'] + 1)
    users.append(user)
    self.write(user)

def createServer():
  return tornado.web.Application([
    (r'/', IndexHandler),
    (r'/api/users', UsersHandler),
  ])

if __name__ == '__main__':
  server = createServer()
  server.listen(3000)
  print('server is running at 3000')
  tornado.ioloop.IOLoop.current().start()
