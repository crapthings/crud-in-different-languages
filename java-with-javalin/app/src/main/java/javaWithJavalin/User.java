package javaWithJavalin;

import com.github.javafaker.Faker;

public class User {
  int _id;
  String username;
  String email;
  String fullname;

  public User(int id) {
    Faker faker = new Faker();
    _id = id;
    username = faker.name().username();
    email = faker.internet().emailAddress();
    fullname = faker.name().fullName();
  }
}
