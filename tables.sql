﻿CREATE TABLE "User" (
    "id" serial PRIMARY KEY,
    "email" varchar(100) UNIQUE NOT NULL,
    "username" varchar(100) UNIQUE NOT NULL,
    "password" varchar(100) NOT NULL,
    "saved_recipes_count" integer 
);

CREATE TABLE "Recipe" (
    "id" serial PRIMARY KEY,
    "title" varchar(100) NOT NULL,
    "usedIngredients" varchar(200) NOT NULL,
    "instructions" text NOT NULL,
    "image" varchar(200) NOT NULL
);

CREATE TABLE "Saved_Recipes" (
    "id" serial PRIMARY KEY,
    "user_id" integer REFERENCES "User" ("id"),
    "recipe_id" integer REFERENCES "Recipe" ("id")
);

