from flask import Blueprint, render_template, jsonify, request
from app.db import get_db

# Blueprint for recipes
recipes_bp = Blueprint("recipes", __name__)

#-------------------------------------
# READ/FIND ONE recipe by ID
#-------------------------------------
def read_one_recipe(recipe_id: int):
    # Get the database connection
    db = get_db()
    # Find and return the recipe document by _id
    return db.recipes.find_one({"_id": recipe_id})

#-------------------------------------
# Route for reading one recipe by ID
#-------------------------------------
@recipes_bp.route("/recipes/<int:recipe_id>", methods=["GET"])
def read_one_recipe_route(recipe_id):
    # Get the recipe document by ID
    recipe = recipes_bp.read_one_recipe(recipe_id)
    # If recipe not found, return 404 error
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    # Convert ObjectId to string for JSON serialization
    recipe["_id"] = str(recipe["_id"])
    # Return the recipe document as JSON
    return jsonify(recipe), 200

#--------------------------------
# READ/FIND ALL recipes
#--------------------------------
def read_all_recipes():
    # Get the database connection
    db = get_db()
    # Find and return ALL recipe documents as a list
    return list(db.recipes.find())

#--------------------------------
# Route for reading all recipes
#--------------------------------
@recipes_bp.route("/recipes", methods=["GET"])
def read_all_recipes_route():
    # Get all recipe documents
    recipes = recipes_bp.read_all_recipes()
    # Convert ObjectId to string for JSON serialization
    for recipe in recipes:
        recipe["_id"] = str(recipe["_id"])
    # Return the list of recipes as JSON
    return jsonify(recipes), 200

#--------------------------------
# CREATE/INSERT recipe
#--------------------------------
def create_recipe(title, description, categoryid, authoruserid, ingredients, tags, dietaryflags, preptime, cooktime, servings):
    # Get the database connection
    db = get_db()
    # Create a new recipe document and insert it into the database
    recipe = {
        "title": title,
        "description": description,
        "categoryid": categoryid,
        "authorUserId": authoruserid,
        "ingredients": ingredients,
        "tags": tags,
        "dietaryFlags": dietaryflags,
        "preptime": preptime,
        "cooktime": cooktime,
        "servings": servings
    }
    # Insert and return the inserted ID
    return db.recipes.insert_one(recipe).inserted_id

#--------------------------------
# Route for creating a new recipe
#--------------------------------
@recipes_bp.route("/recipes", methods=["POST"])
def create_recipe_route():
    # Get the JSON data from the request
    data = request.get_json()
    # Retrieve recipe fields from the JSON data
    title = data.get("title")
    description = data.get("description")
    categoryid = data.get("categoryid")
    authoruserid = data.get("authorUserId")
    ingredients = data.get("ingredients")
    tags = data.get("tags")
    dietaryflags = data.get("dietaryFlags")
    preptime = data.get("preptime")
    cooktime = data.get("cooktime")
    servings = data.get("servings")
    # Validate required fields
    if not title or not description or not categoryid or not authoruserid:
        return jsonify({"error": "Missing required fields"}), 400
    # Create the recipe and get the new recipe ID
    recipe_id = recipes_bp.create_recipe(title, description, categoryid, authoruserid, ingredients, tags, dietaryflags, preptime, cooktime, servings)
    # Return a success message with the new recipe ID
    return jsonify({"message": "Recipe created", "recipe_id": str(recipe_id)}), 201


#--------------------------------
# UPDATE ONE recipe
#--------------------------------
def update_recipe(recipe_id, title, description, categoryid, authoruserid, ingredients, tags, dietaryflags, preptime, cooktime, servings):
    # Build the recipe update
    update_fields = {}
    # ensures that only fields with values are updated
    if title:
        update_fields["title"] = title
    if description:
        update_fields["description"] = description
    if categoryid:
        update_fields["categoryid"] = categoryid
    if authoruserid:
        update_fields["authorUserId"] = authoruserid
    if ingredients:
        update_fields["ingredients"] = ingredients
    if tags:
        update_fields["tags"] = tags
    if dietaryflags:
        update_fields["dietaryFlags"] = dietaryflags
    if preptime:
        update_fields["preptime"] = preptime
    if cooktime:
        update_fields["cooktime"] = cooktime
    if servings:
        update_fields["servings"] = servings
    # If no fields to update, return False
    if not update_fields:
        return None
    # Get the database connection
    db = get_db()
    # Update the recipe document by ID and return whether it was modified
    return db.recipes.update_one(
        {"_id": recipe_id}, 
        {"$set": update_fields}).modified_count > 0

#--------------------------------
# Route for updating a recipe by ID
#--------------------------------
@recipes_bp.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe_route(recipe_id):
    # Get the JSON data from the request
    data = request.get_json()
    # Retrieve recipe fields from the JSON data
    title = data.get("title")
    description = data.get("description")
    categoryid = data.get("categoryid")
    authoruserid = data.get("authorUserId")
    ingredients = data.get("ingredients")
    tags = data.get("tags")
    dietaryflags = data.get("dietaryFlags")
    preptime = data.get("preptime")
    cooktime = data.get("cooktime")
    servings = data.get("servings")
    # Update the recipe and get the result
    result = recipes_bp.update_recipe(recipe_id, title, description, categoryid, authoruserid, ingredients, tags, dietaryflags, preptime, cooktime, servings)
    # If no fields to update, return 400 error
    if result is None:
        return jsonify({"error": "No fields to update"}), 400
    # If no documents were modified, return 404 error
    if not result:
        return jsonify({"error": "Recipe not found"}), 404
    # Return success message as JSON
    return jsonify({"message": "Recipe updated successfully"}), 200

#-------------------------------
# UPDATE many recipes
#-------------------------------
def update_many_recipes(recipe_ids, title, description, categoryid, authoruserid, ingredients, tags, dietaryflags, preptime, cooktime, servings):
    # Build the recipe update
    update_fields = {}
    # ensures that only fields with values are updated
    if title:
        update_fields["title"] = title
    if description:
        update_fields["description"] = description
    if categoryid:
        update_fields["categoryid"] = categoryid
    if authoruserid:
        update_fields["authorUserId"] = authoruserid
    if ingredients:
        update_fields["ingredients"] = ingredients
    if tags:
        update_fields["tags"] = tags
    if dietaryflags:
        update_fields["dietaryFlags"] = dietaryflags
    if preptime:
        update_fields["preptime"] = preptime
    if cooktime:
        update_fields["cooktime"] = cooktime
    if servings:
        update_fields["servings"] = servings
    # If no fields to update, return None
    if not update_fields:
        return None
    # Get the database connection
    db = get_db()
    # Update the recipe documents by IDs and return the result
    return db.recipes.update_many(
        {"_id": {"$in": recipe_ids}}, 
        {"$set": update_fields})

#-------------------------------
# Route for updating many recipes by IDs
#-------------------------------
@recipes_bp.route("/recipes/batch", methods=["PUT"])
def update_many_recipes_route():
    # Get the JSON data from the request
    data = request.get_json()
    recipe_ids = data.get("recipe_ids")
    title = data.get("title")
    description = data.get("description")
    categoryid = data.get("categoryid")
    authoruserid = data.get("authorUserId")
    ingredients = data.get("ingredients")
    tags = data.get("tags")
    dietaryflags = data.get("dietaryFlags")
    preptime = data.get("preptime")
    cooktime = data.get("cooktime")
    servings = data.get("servings")
    # Validate that recipe_ids is provided and is a list
    result = recipes_bp.update_many_recipes(recipe_ids, title, description, categoryid, authoruserid, ingredients, tags, dietaryflags, preptime, cooktime, servings)
    # If no fields to update, return 400 error
    if result is None:
        return jsonify({"error": "No fields to update"}), 400
    # If no documents were modified, return 404 error
    if result.matched_count == 0:
        return jsonify({"error": "No recipes found for the provided IDs"}), 404
    # Return success message with count of modified recipes as JSON
    return jsonify({"message": f"{result.modified_count} recipes updated successfully"}), 200

#--------------------------------
# DELETE ONE recipe
#--------------------------------
def delete_one_recipe(recipe_id: int):
    # Get the database connection
    db = get_db()
    # Delete the recipe document by ID and return whether it was deleted
    result = db.recipes.delete_one({"_id": recipe_id})
    # Return the count of deleted documents
    return result.deleted_count > 0

#--------------------------------
# Route for deleting one recipe by ID
#--------------------------------
@recipes_bp.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_one_recipe_route(recipe_id):
    # Delete the recipe and get the result
    result = recipes_bp.delete_one_recipe(recipe_id)
    # If no documents were deleted, return 404 error
    if not result:
        return jsonify({"error": "Recipe not found"}), 404
    # Return success message as JSON
    return jsonify({"message": "Recipe deleted successfully"}), 200

#--------------------------------
# DELETE many recipes
#--------------------------------
def delete_many_recipes(recipe_ids):
    # Get the database connection
    db = get_db()
    # Delete the recipe documents by IDs and return the count of deleted documents
    result = db.recipes.delete_many({"_id": {"$in": recipe_ids}})
    # Return the count of deleted documents
    return result.deleted_count

#--------------------------------
# Route for deleting many recipes by IDs
#--------------------------------
@recipes_bp.route("/recipes/batch", methods=["DELETE"])
def delete_many_recipes_route():
    # Get the JSON data from the request
    data = request.get_json()
    # Validate that recipe_ids is provided and is a list
    recipe_ids = data.get("recipe_ids")
    # If recipe_ids is not provided or is not a list, return 400 error
    if not recipe_ids or not isinstance(recipe_ids, list):
        return jsonify({"error": "recipe_ids must be a list of IDs"}), 400
    # Delete the recipes and get the count of deleted documents
    deleted_count = recipes_bp.delete_many_recipes(recipe_ids)
    # If no documents were deleted, return 404 error
    if deleted_count == 0:
        return jsonify({"error": "No recipes found for the provided IDs"}), 404
    # Return success message with count of deleted recipes as JSON
    return jsonify({"message": f"{deleted_count} recipes deleted successfully"}), 200
