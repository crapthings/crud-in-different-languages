import { faker } from '@faker-js/faker'
import Fastify from 'fastify'

const fastify = Fastify()

type User = {
  _id: number
  username: string
  email?: string
  fullname?: string
  avatarUrl?: string
}

type RouteParams = {
  _id: string
}

const createUser = (_id: number): User => ({
  _id: _id,
  username: faker.internet.userName(),
  email: faker.internet.email(),
  fullname: faker.person.fullName(),
  avatarUrl: faker.image.avatar (),
})

const users = Array.from({ length: 10 }, (_, idx) => idx + 1).map(createUser)

fastify.register(function (fastify, opts, done) {
  fastify.get('/users', function (req, res) {
    res.send(users)
  })

  fastify.post('/users', function (req, res) {
    const user = createUser(users[users.length - 1]._id + 1)
    users.push(user)
    res.send(user)
  })

  fastify.put<{
    Params: RouteParams
    Body: User
  }>('/users/:_id', function (req, res) {
    const userId = parseInt(req.params._id)
    const userIndex = users.findIndex(({ _id }) => _id === userId)
    const user = users[userIndex] = { ...req.body, _id: userId }
    res.send(user)
  })

  fastify.delete<{
    Params: RouteParams
  }>('/users/:_id', function (req, res) {
    const userId = parseInt(req.params._id)
    const userIndex = users.findIndex(({ _id }) => _id === userId)
    if (userIndex) {
      users.splice(userIndex, 1)
    }
    res.send(userIndex)
  })

  done()
}, { prefix: '/api' })


fastify.get('/', (req, res) => {
  res.send('typescript with fastify')
})

fastify.listen({ port: 3000 }, () => {
  console.log('server is running at 3000')
})
