package main

import (
  "fmt"
  "strconv"
)
import "reflect"
import "github.com/gin-gonic/gin"
import "syreclabs.com/go/faker"

type User struct {
  ID int `json:"_id" uri:"_id"`
  Username string `json:"username"`
  Email string `json:"email"`
  Fullname string `json:"fullname"`
}

func createUser (idx int) (user User) {
  user.ID = idx
  user.Username = faker.Internet().UserName()
  user.Email = faker.Internet().Email()
  user.Fullname = faker.Name().Name()
  return user
}

func main () {
  users := []User{}

  for i := 1; i <= 10; i++ {
    users = append(users, createUser(i))
  }

  router := gin.Default()

  router.GET("/", func (c *gin.Context) {
    c.String(200, "go with gin")
  })

  api := router.Group("/api")
  {
    api.GET("/users", func (c *gin.Context) {
      c.IndentedJSON(200, users)
    })

    api.POST("/users", func (c *gin.Context) {
      lastId := users[len(users) - 1].ID
      users = append(users, createUser(lastId + 1))
      c.IndentedJSON(200, users)
    })

    api.PUT("/users/:_id", func (c *gin.Context) {
      _id, _ := strconv.Atoi(c.Param("_id"))
      for index, item := range users {
        id := reflect.Indirect(reflect.ValueOf(item)).FieldByName("ID")
        if id.Interface().(int) == _id {
          var user User
          _user := &users[index]
          if c.ShouldBind(&user) == nil {
            _user.Username = user.Username
            _user.Email = user.Email
            _user.Fullname = user.Fullname
          }
          c.JSON(200, _user)
          return
        }
      }
      c.JSON(200, nil)
    })

    api.DELETE("/users/:_id", func (c *gin.Context) {
      _id, _ := strconv.Atoi(c.Param("_id"))
      for index, item := range users {
        id := reflect.Indirect(reflect.ValueOf(item)).FieldByName("ID")
        if id.Interface().(int) == _id {
          users = append(users[:index], users[index+1:]...)
          c.JSON(200, _id)
          return
        }
      }
      c.JSON(200, nil)
    })
  }

  fmt.Println("server is running at 3000")
  router.Run(":3000")
}
