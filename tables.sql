CREATE TABLE "User" (
    "id" serial PRIMARY KEY,
    "email" varchar(100) UNIQUE NOT NULL,
    "username" varchar(100) UNIQUE NOT NULL,
    "password" varchar(100) NOT NULL
);

CREATE TABLE "Recipe" (
    "id" serial PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "ingredients" varchar(200) NOT NULL,
    "instructions" text NOT NULL,
    "image" varchar(200) NOT NULL
);

CREATE TABLE "saved_recipes" (
    "user_id" integer REFERENCES "User" ("id"),
    "recipe_id" integer REFERENCES "Recipe" ("id"),
    PRIMARY KEY ("user_id", "recipe_id")
);

