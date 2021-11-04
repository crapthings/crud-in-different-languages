from sanic import Sanic
from sanic.response import text
from sanic.response import json
from faker import Faker

fake = Faker()

def createUser(idx):
  return {
    '_id': idx + 1,
    'fullname': fake.name(),
    'email': fake.email()
  }

users = list((createUser(idx) for idx in range(10)))

app = Sanic('server')

@app.get('/api/users')
async def getUsers(req):
  return json(users)

@app.post('/api/users')
async def createUsers(req):
  return json(users)

@app.put('/api/users/<_id>')
async def createUsers(req, _id):
  id = int(_id)
  userIndex = next((userIdx for userIdx, user in enumerate(users) if user['_id'] is id), None)
  if userIndex is not None:
    user = { '_id': id, **req.json }
    users[userIndex] = user
    return json(user)
  else:
    return json(None)

@app.delete('/api/users/<_id>')
async def createUsers(req, _id):
  id = int(_id)

  for userIdx, user in enumerate(users):
    if user['_id'] is id:
      del users[userIdx]
      break

  return json(_id)

@app.get('/')
async def hello_world(req):
  return text('python with sanic')

app.run(host='0.0.0.0', port=3000, access_log=False)
