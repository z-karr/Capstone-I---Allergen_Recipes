CREATE TABLE "User" (
    "id" serial PRIMARY KEY,
    "email" varchar(100) UNIQUE NOT NULL,
    "username" varchar(100) UNIQUE NOT NULL,
    "password" varchar(100) NOT NULL,
    "saved_recipes" integer NOT NULL
);

CREATE TABLE "Recipe" (
    "id" serial PRIMARY KEY,
    "spoonacular_id" integer UNIQUE
);

CREATE TABLE "Saved_Recipes" (
    "id" serial PRIMARY KEY,
    "user_id" integer REFERENCES "User" ("id"),
    "recipe_id" integer REFERENCES "Recipe" ("id")
);

