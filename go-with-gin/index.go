package main

import (
  "fmt"
  "net/http"
  "strconv"

  "github.com/gin-gonic/gin"
  "syreclabs.com/go/faker"
)

type User struct {
  ID       int    `json:"_id" uri:"_id"`
  Username string `json:"username"`
  Email    string `json:"email"`
  Fullname string `json:"fullname"`
}

func createUser (idx int) User {
  return User{
    ID:       idx,
    Username: faker.Internet().UserName(),
    Email:    faker.Internet().Email(),
    Fullname: faker.Name().Name(),
  }
}

func main () {
  users := make(map[int]User)

  for i := 1; i <= 10; i++ {
    users[i] = createUser(i)
  }

  router := gin.Default()

  router.GET("/", func(c *gin.Context) {
    c.String(http.StatusOK, "go with gin")
  })

  api := router.Group("/api")
  {
    api.GET("/users", func (c *gin.Context) {
      userList := make([]User, 0, len(users))

      for _, user := range users {
        userList = append(userList, user)
      }

      c.JSON(http.StatusOK, userList)
    })

    api.POST("/users", func (c *gin.Context) {
      newID := len(users) + 1
      newUser := createUser(newID)
      users[newID] = newUser
      c.JSON(http.StatusCreated, newUser)
    })

    api.PUT("/users/:_id", func (c *gin.Context) {
      id, err := strconv.Atoi(c.Param("_id"))

      if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
        return
      }

      user, exists := users[id]

      if !exists {
        c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
        return
      }

      if err := c.BindJSON(&user); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
      }

      users[id] = user

      c.JSON(http.StatusOK, user)
    })

    api.DELETE("/users/:_id", func (c *gin.Context) {
      id, err := strconv.Atoi(c.Param("_id"))

      if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
        return
      }

      if _, exists := users[id]; !exists {
        c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
        return
      }

      delete(users, id)

      c.JSON(http.StatusOK, gin.H{"message": "User deleted"})
    })
  }

  fmt.Println("server is running at 3000")
  router.Run(":3000")
}
