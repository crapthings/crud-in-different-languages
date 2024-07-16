const express = require('express')
const bodyParser = require('body-parser')
const { faker } = require('@faker-js/faker')

const server = new express()
const router = express.Router()

const createUser = (_id) => ({
  _id,
  username: faker.internet.userName(),
  email: faker.internet.email(),
  fullname: faker.person.fullName(),
  avatarUrl: faker.image.avatar(),
})

const users = Array.from({ length: 10 }, (_, idx) => idx + 1).map(createUser)

router.get('/users', function (req, res) {
  res.json(users)
})

router.post('/users', function (req, res) {
  const user = createUser(users[users.length - 1]._id + 1)
  users.push(user)
  res.json(user)
})

router.put('/users/:_id', function (req, res) {
  const userId = parseInt(req.params._id)
  const userIndex = users.findIndex(({ _id }) => _id === userId)
  const user = users[userIndex] = { _id: userId, ...req.body }
  res.json(user)
})

router.delete('/users/:_id', function (req, res) {
  const userId = parseInt(req.params._id)
  const userIndex = users.findIndex(({ _id }) => _id === userId)
  if (userIndex) {
    users.splice(userIndex, 1)
  }
  res.json(userIndex)
})

server.get('/', function (req, res) {
  res.end('javascript with express')
})

server.use(bodyParser.json())
server.use('/api', router)

server.listen(3000, function () {
  console.log('server is running at 3000')
})
