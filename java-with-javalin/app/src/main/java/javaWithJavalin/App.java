package javaWithJavalin;

import java.util.ArrayList;
import io.javalin.Javalin;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class App {
  public static void main(String[] args) {
    GsonBuilder builder = new GsonBuilder();
    builder.setPrettyPrinting();
    Gson gson = builder.create();

    ArrayList<User> users = new ArrayList<User>();

    for (int i = 1; i <= 10; i++) {
      users.add(new User(i));
    }

    Javalin app = Javalin.create().start(3000);

    app.get("/", ctx -> ctx.result("java with javalin"));

    app.get("/api/users", ctx -> {
      ctx.json(gson.toJson(users));
    });

    app.post("/api/users", ctx -> {
      int lastId = users.get(users.size() - 1)._id;
      User user = new User(lastId + 1);
      users.add(user);
      ctx.json(gson.toJson(user));
    });

    app.put("/api/users/{_id}", ctx -> {
      int id = Integer.parseInt(ctx.pathParam("_id"));
      System.out.println(ctx.body());
      for (User user : users) {
        if (user._id == id) {
          User a = gson.fromJson(ctx.body(), User.class);
          a._id = id;
          users.set(users.indexOf(user), a);
          ctx.json(gson.toJson(a));
          return;
        }
      }
      ctx.json(gson.toJson(null));
    });

    app.delete("/api/users/{_id}", ctx -> {
      int id = Integer.parseInt(ctx.pathParam("_id"));
      for (User user : users) {
        if (user._id == id) {
          users.remove(user);
          ctx.json(gson.toJson(id));
          return;
        }
      }
      ctx.json(gson.toJson(null));
    });
  }
}
