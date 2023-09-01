-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "User" (
    "UserID" int   NOT NULL,
    "Email" string   NOT NULL,
    "Username" string NOT NULL,
    "Password" string   NOT NULL,
    "saved_recipes_count" AS (SELECT COUNT(*) FROM Saved_Recipes WHERE Saved_Recipes.UserID = User.UserID)
        ); int   NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "UserID"
);

CREATE TABLE "Recipe" (
    "RecipeID" int   NOT NULL,
    "NameofRecipe" string   NOT NULL,
    "Ingredients" string   NOT NULL,
    "Instructions" text   NOT NULL,
    "Image" URL   NOT NULL,
    CONSTRAINT "pk_Recipe" PRIMARY KEY (
        "RecipeID"
     )
);

CREATE TABLE "Saved_Recipes" (
    "UserID" int   NOT NULL,
    "RecipeID" int   NOT NULL
);

ALTER TABLE "Recipe" ADD CONSTRAINT "fk_Recipe_RecipeID" FOREIGN KEY("RecipeID")
REFERENCES "Saved_Recipes" ("RecipeID");

ALTER TABLE "Saved_Recipes" ADD CONSTRAINT "fk_Saved_Recipes_UserID" FOREIGN KEY("UserID")
REFERENCES "User" ("UserID");


