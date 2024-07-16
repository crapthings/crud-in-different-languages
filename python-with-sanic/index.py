from sanic import Sanic
from sanic.response import text
from sanic.response import json
from faker import Faker

fake = Faker()

def createUser (idx):
  return {
    '_id': idx + 1,
    'email': fake.email(),
    'fullname': fake.name(),
  }

users = list((createUser(idx) for idx in range(10)))

app = Sanic('server')

@app.get('/api/users')
async def getUsers (req):
  return json(users)

@app.post('/api/users')
async def postUser (req):
  lastId = users[len(users) - 1]['_id']
  user = createUser(lastId)
  users.append(user)
  return json(user)

@app.put('/api/users/<_id>')
async def putUser (req, _id):
  id = int(_id)
  userIndex = next((userIdx for userIdx, user in enumerate(users) if user['_id'] is id), None)
  if userIndex is not None:
    user = { '_id': id, **req.json }
    users[userIndex] = user
    return json(user)
  else:
    return json(None)

@app.delete('/api/users/<_id>')
async def deleteUser (req, _id):
  id = int(_id)
  userIndex = next((userIdx for userIdx, user in enumerate(users) if user['_id'] is id), None)
  if userIndex is not None:
    del users[userIndex]
    return json(_id)
  else:
    return json(None)

@app.get('/')
async def index(req):
  return text('python with sanic')

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 3000, access_log = False)
