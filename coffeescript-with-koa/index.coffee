faker = require 'faker'
Koa = require 'koa'
bodyParser = require 'koa-bodyparser'
json = require 'koa-json'
Router = require 'koa-better-router'

createUser = (idx) ->
  _id: idx
  username: do faker.internet.userName
  email: do faker.internet.email
  fullname: do faker.name.findName
  avatarUrl: do faker.internet.avatar

users = Array.from({ length: 10 }, (_, idx) -> idx + 1).map createUser

server = new Koa

api = Router
  prefix: '/api'

api.loadMethods()

api.get '/users', (ctx) ->
  ctx.body = users

api.post '/users', (ctx) ->
  lastIdx = users[users.length - 1]._id + 1
  user = createUser(lastIdx)
  users.push user
  ctx.body = user

api.put '/users/:_id', (ctx) ->
  userId = parseInt ctx.params._id
  userIndex = users.findIndex (user) -> user._id == userId

  users[userIndex] = {
    _id: userId
    ctx.request.body...
  }

  ctx.body = users[userIndex]

api.del '/users/:_id', (ctx) ->
  userId = parseInt ctx.params._id
  userIndex = users.findIndex (user) -> user._id == userId
  users.splice(userIndex, 1) unless userIndex is -1
  ctx.body = userIndex

router = Router().loadMethods()

router.get '/', (ctx) ->
  ctx.body = 'coffeescript with koa'

server.use bodyParser()
server.use json()
server.use api.middleware()
server.use router.middleware()

server.listen 3000, () ->
  console.log 'server is running at 3000'
