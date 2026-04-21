from app.db import get_db
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def seed():
    db = get_db()

    # ── CLEAR ──
    db.users.drop()
    db.categories.drop()
    db.recipes.drop()
    db.reviews.drop()
    db["savedRecipes"].drop()
    db["mealPlans"].drop()
    # drop stale variants from old naming
    db["saved_recipes"].drop()
    db["SavedRecipes"].drop()
    db["meal_plans"].drop()
    db["MealPlans"].drop()
    db["Meal_plans"].drop()
    db["Categories"].drop()
    db["Recipes"].drop()
    db["Reviews"].drop()
    db["Users"].drop()
    print("Cleared collections.")

    # ── CATEGORIES ──
    # FIX: expanded to 7 categories to match recipe references
    categories = db.categories.insert_many([
        { "name": "Breakfast",  "description": "Morning meals",       "tags": ["quick", "morning"] },
        { "name": "Lunch",      "description": "Midday meals",        "tags": ["light", "midday"] },
        { "name": "Dinner",     "description": "Evening meals",       "tags": ["hearty", "main course"] },
        { "name": "Dessert",    "description": "Sweet treats",        "tags": ["sweet", "baked"] },
        { "name": "Snack",      "description": "Light bites",         "tags": ["quick", "small"] },
        { "name": "Appetizer",  "description": "Starters and bites",  "tags": ["small", "starter"] },
        { "name": "Comfort",    "description": "Comfort food",        "tags": ["hearty", "comfort"] },
    ]).inserted_ids

    # ── USERS ──
    # FIX: removed embedded def seedusers() function — was invalid syntax
    # FIX: renamed dietpreferences → dietary_preferences, favcategories → favorite_categories
    # FIX: renamed creationdate → created_at to match schema
    users = db.users.insert_many([
        { "name": "Maria Santos",        "email": "maria@example.com",                    "dietaryPreferences": ["vegetarian", "gluten-free"], "favoriteCategories": [categories[0]], "createdAt": datetime.utcnow() },
        { "name": "Alice Johnson",        "email": "alice@gmail.com",                      "dietaryPreferences": ["vegetarian"],                 "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Bob Smith",            "email": "bob@bobby.com",                        "dietaryPreferences": ["high-protein"],               "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Laura Palmer",         "email": "laurapalmer@twinpeaks.com",            "dietaryPreferences": ["gluten-free"],                "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Dale Cooper",          "email": "dalecooper@fbi.gov",                   "dietaryPreferences": ["low-carb"],                   "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Roger Huntington",     "email": "borntobleed@gmail.com",                "dietaryPreferences": ["high-protein"],               "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "John Doe",             "email": "john.doe@missing.com",                 "dietaryPreferences": ["vegan"],                      "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "John Wick",            "email": "john.wick@continental.com",            "dietaryPreferences": ["high-protein"],               "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Stu Macher",           "email": "stu.macher@scarymovies.com",           "dietaryPreferences": ["low-carb"],                   "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Billy Loomis",         "email": "billy.loomis@scarymovies.com",         "dietaryPreferences": ["low-carb"],                   "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Silent Bob",           "email": "silentbob@viewaskew.com",              "dietaryPreferences": ["vegan"],                      "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Fox Mulder",           "email": "fox.mulder@fbi.gov",                   "dietaryPreferences": ["mediterranean"],              "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Ash Williams",         "email": "ash.williams@necronomicon.com",        "dietaryPreferences": ["paleo"],                      "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Vincent Vega",         "email": "vincent.vega@pulpfiction.com",         "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Jules Winnfield",      "email": "jules.winnfield@pulpfiction.com",      "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Charlie Dompler",      "email": "charlie.dompler@SmilingFriends.net",   "dietaryPreferences": ["vegan"],                      "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Pim Pimling",          "email": "pim.pimling@smilingfriends.net",       "dietaryPreferences": ["vegetarian"],                 "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Allan Red",            "email": "allan.red@smilingfriends.net",         "dietaryPreferences": ["high-protein"],               "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Walter White",         "email": "walter.white@breakingbad.com",         "dietaryPreferences": ["high-protein"],               "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Jesse Pinkman",        "email": "jesse.pinkman@breakingbad.com",        "dietaryPreferences": ["low-carb"],                   "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Dexter Morgan",        "email": "dexter.morgan@darkmatter.com",         "dietaryPreferences": ["paleo"],                      "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Sneakers O'Toole",     "email": "sneakers.otoole@gmail.com",            "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Dio Brando",           "email": "dio.brando@gmail.com",                 "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Dan Smith",            "email": "dan.smith@gmail.com",                  "dietaryPreferences": ["vegan"],                      "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Terry Crews",          "email": "terry.crews@gmail.com",                "dietaryPreferences": ["high-protein"],               "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Sarah Connor",         "email": "sarah.connor@terminator.com",          "dietaryPreferences": ["paleo"],                      "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "James Bond",           "email": "james.bond@mi6.uk",                    "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Jane Kilcher",         "email": "jane.kilcher@gmail.com",               "dietaryPreferences": ["paleo"],                      "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Kurt Hummel",          "email": "kurt.hummel@gmail.com",                "dietaryPreferences": ["vegetarian"],                 "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Rachel Green",         "email": "rachel.green@friends.com",             "dietaryPreferences": ["vegetarian"],                 "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Jay Mewes",            "email": "jay.mewes@viewaskew.com",              "dietaryPreferences": ["vegan"],                      "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Shaggy Rogers",        "email": "shaggy.rogers@monsterhunters.com",     "dietaryPreferences": ["vegetarian"],                 "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Fred Jones",           "email": "fred.jones@monsterhunters.com",        "dietaryPreferences": ["high-protein"],               "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Velma Dinkley",        "email": "velma.dinkley@twinpeaks.com",          "dietaryPreferences": ["gluten-free"],                "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Daphnie Blake",        "email": "daphnie.blake@monsterhunters.com",     "dietaryPreferences": ["vegetarian"],                 "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Chev Chelios",         "email": "unstoppable@crank.com",                "dietaryPreferences": ["high-protein"],               "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "John McClane",         "email": "john.mcclane@diehard.com",             "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Black Dynamite",       "email": "black.dynamite@fbi.gov",               "dietaryPreferences": ["high-protein"],               "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Duke Nukem",           "email": "duke.nukem@3drealms.com",              "dietaryPreferences": ["low-carb"],                   "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Richard B. Riddick",   "email": "richard.riddick@pitchblack.com",       "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Henry Dorsett Case",   "email": "henry.dorsett.case@Neuromancer.com",   "dietaryPreferences": ["futuristic"],                 "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Neo Anderson",         "email": "neo.anderson@matrix.com",              "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Morpheus",             "email": "morpheus@matrix.com",                  "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Masao Kakihara",       "email": "kakihara@yakuza.com",                  "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Ronnie James Dio",     "email": "holydiver@thelastinline.com",           "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Bob Clarkson",         "email": "bob.clarkson@gmail.com",               "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Terry Gilliam",        "email": "tgilliam@montypython.com",             "dietaryPreferences": ["vegan"],                      "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "The Black Knight",     "email": "BlackKnight@montypython.com",          "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Hiro Protagonist",     "email": "hiro.protagonist@snowcrash.com",       "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Kirby Reed",           "email": "kirby.reed@fbi.gov",                   "dietaryPreferences": ["none"],                       "favoriteCategories": [],              "createdAt": datetime.utcnow() },
        { "name": "Daria Morgendorffer",  "email": "daria.morgendorffer@sadsickworld.com", "dietaryPreferences": ["vegetarian"],                 "favoriteCategories": [],              "createdAt": datetime.utcnow() },
    ]).inserted_ids
    print(f"Seeded {len(users)} users.")

    # ── RECIPES ──
    # FIX: replaced all categoryids → categories, userids → users
    # FIX: added missing commas between recipe dicts
    # FIX: standardized field names (preptime → prep_time, cooktime → cook_time)
    recipes = db.recipes.insert_many([
        {
            "title": "Chicken Tikka Masala",
            "description": "A rich, creamy tomato-based curry.",
            "categoryId": categories[2],
            "authorUserId": users[0],
            "ingredients": [
                { "name": "chicken breast", "amount": 500, "unit": "g" },
                { "name": "heavy cream",    "amount": 200, "unit": "ml" },
                { "name": "garam masala",   "amount": 2,   "unit": "tsp" },
            ],
            "tags": ["curry", "Indian", "comfort food"],
            "dietaryFlags": ["gluten-free", "high-protein"],
            "prepTime": 20, "cookTime": 35, "servings": 4,
        },
        {
            "title": "Veggie Omelette",
            "description": "Healthy vegetarian omelette.",
            "categoryId": categories[0],
            "authorUserId": users[1],
            "ingredients": [
                { "name": "eggs",    "amount": 2,   "unit": "whole" },
                { "name": "spinach", "amount": 1,   "unit": "cup" },
            ],
            "tags": ["vegetarian", "breakfast"],
            "dietaryFlags": ["vegetarian"],
            "prepTime": 5, "cookTime": 10, "servings": 1,
        },
        {
            "title": "Grilled Chicken",
            "description": "High protein dinner.",
            "categoryId": categories[2],
            "authorUserId": users[2],
            "ingredients": [
                { "name": "chicken breast", "amount": 200, "unit": "g" },
            ],
            "tags": ["protein", "simple"],
            "dietaryFlags": ["high-protein"],
            "prepTime": 10, "cookTime": 20, "servings": 2,
        },
        {
            "title": "Gluten-Free Pasta",
            "description": "Pasta for gluten-sensitive diets.",
            "categoryId": categories[1],
            "authorUserId": users[3],
            "ingredients": [
                { "name": "gluten-free pasta", "amount": 100, "unit": "g" },
                { "name": "tomato sauce",       "amount": 1,   "unit": "cup" },
            ],
            "tags": ["gluten-free", "pasta"],
            "dietaryFlags": ["gluten-free"],
            "prepTime": 15, "cookTime": 15, "servings": 2,
        },
        {
            "title": "Keto Salad",
            "description": "Low-carb salad for keto diet.",
            "categoryId": categories[1],
            "authorUserId": users[4],
            "ingredients": [
                { "name": "lettuce",  "amount": 2,  "unit": "cups" },
                { "name": "avocado",  "amount": 1,  "unit": "whole" },
                { "name": "bacon",    "amount": 50, "unit": "g" },
            ],
            "tags": ["keto", "salad", "low-carb"],
            "dietaryFlags": ["low-carb"],
            "prepTime": 10, "cookTime": 0, "servings": 1,
        },
        {
            "title": "Vegan Stir-Fry",
            "description": "Quick and easy vegan stir-fry.",
            "categoryId": categories[2],
            "authorUserId": users[5],
            "ingredients": [
                { "name": "tofu",              "amount": 200, "unit": "g" },
                { "name": "mixed vegetables",  "amount": 2,   "unit": "cups" },
                { "name": "soy sauce",         "amount": 2,   "unit": "tbsp" },
            ],
            "tags": ["vegan", "stir-fry"],
            "dietaryFlags": ["vegan"],
            "prepTime": 15, "cookTime": 10, "servings": 2,
        },
        {
            "title": "Paleo Beef Stew",
            "description": "Hearty beef stew for paleo diet.",
            "categoryId": categories[2],
            "authorUserId": users[6],
            "ingredients": [
                { "name": "beef chunks", "amount": 300, "unit": "g" },
                { "name": "carrots",     "amount": 2,   "unit": "whole" },
                { "name": "potatoes",    "amount": 2,   "unit": "whole" },
                { "name": "beef broth",  "amount": 2,   "unit": "cups" },
            ],
            "tags": ["paleo", "stew"],
            "dietaryFlags": ["paleo"],
            "prepTime": 20, "cookTime": 120, "servings": 4,
        },
        {
            "title": "Mediterranean Quinoa Salad",
            "description": "Light and healthy quinoa salad.",
            "categoryId": categories[1],
            "authorUserId": users[7],
            "ingredients": [
                { "name": "quinoa",      "amount": 1,  "unit": "cup" },
                { "name": "cucumber",    "amount": 1,  "unit": "whole" },
                { "name": "tomatoes",    "amount": 2,  "unit": "whole" },
                { "name": "feta cheese", "amount": 50, "unit": "g" },
                { "name": "olive oil",   "amount": 2,  "unit": "tbsp" },
            ],
            "tags": ["mediterranean", "salad"],
            "dietaryFlags": ["mediterranean"],
            "prepTime": 15, "cookTime": 15, "servings": 2,
        },
        {
            "title": "Red Smoothie",
            "description": "A simple red berry smoothie.",
            "categoryId": categories[0],
            "authorUserId": users[8],
            "ingredients": [
                { "name": "red berries",  "amount": 1, "unit": "cup" },
                { "name": "almond milk",  "amount": 1, "unit": "cup" },
                { "name": "chia seeds",   "amount": 2, "unit": "tbsp" },
            ],
            "tags": ["smoothie", "breakfast"],
            "dietaryFlags": ["vegan"],
            "prepTime": 5, "cookTime": 0, "servings": 1,
        },
        {
            "title": "Rabbit Stew",
            "description": "Stew made with rabbit meat.",
            "categoryId": categories[2],
            "authorUserId": users[9],
            "ingredients": [
                { "name": "rabbit meat",  "amount": 300, "unit": "g" },
                { "name": "carrots",      "amount": 2,   "unit": "whole" },
                { "name": "potatoes",     "amount": 2,   "unit": "whole" },
                { "name": "onions",       "amount": 1,   "unit": "whole" },
                { "name": "garlic",       "amount": 2,   "unit": "cloves" },
                { "name": "rabbit broth", "amount": 2,   "unit": "cups" },
            ],
            "tags": ["stew", "rabbit"],
            "dietaryFlags": ["paleo"],
            "prepTime": 20, "cookTime": 120, "servings": 4,
        },
        {
            "title": "Asian Salad",
            "description": "A fresh salad inspired by Asian flavors.",
            "categoryId": categories[1],
            "authorUserId": users[10],
            "ingredients": [
                { "name": "lettuce",   "amount": 2, "unit": "cups" },
                { "name": "avocado",   "amount": 1, "unit": "whole" },
                { "name": "quinoa",    "amount": 1, "unit": "cup" },
                { "name": "edamame",   "amount": 1, "unit": "cup" },
                { "name": "soy sauce", "amount": 2, "unit": "tbsp" },
            ],
            "tags": ["asian", "salad"],
            "dietaryFlags": ["vegan"],
            "prepTime": 15, "cookTime": 10, "servings": 2,
        },
        {
            "title": "Kale Smoothie",
            "description": "A simple kale smoothie.",
            "categoryId": categories[0],
            "authorUserId": users[11],
            "ingredients": [
                { "name": "kale",        "amount": 2, "unit": "cups" },
                { "name": "banana",      "amount": 1, "unit": "whole" },
                { "name": "almond milk", "amount": 1, "unit": "cup" },
            ],
            "tags": ["smoothie", "healthy"],
            "dietaryFlags": ["vegan"],
            "prepTime": 5, "cookTime": 0, "servings": 1,
        },
        {
            "title": "Fish and Chips",
            "description": "Classic British dish.",
            "categoryId": categories[2],
            "authorUserId": users[12],
            "ingredients": [
                { "name": "fish fillets", "amount": 200, "unit": "g" },
                { "name": "potatoes",     "amount": 2,   "unit": "whole" },
                { "name": "flour",        "amount": 1,   "unit": "cup" },
                { "name": "beer",         "amount": 1,   "unit": "cup" },
            ],
            "tags": ["fish", "british"],
            "dietaryFlags": ["none"],
            "prepTime": 15, "cookTime": 20, "servings": 2,
        },
        {
            "title": "Vegan Chocolate Cake",
            "description": "A delicious vegan chocolate cake.",
            "categoryId": categories[3],
            "authorUserId": users[13],
            "ingredients": [
                { "name": "flour",            "amount": 1.5, "unit": "cups" },
                { "name": "cocoa powder",     "amount": 0.5, "unit": "cup" },
                { "name": "sugar",            "amount": 1,   "unit": "cup" },
                { "name": "baking soda",      "amount": 1,   "unit": "tsp" },
                { "name": "water",            "amount": 1,   "unit": "cup" },
                { "name": "vegetable oil",    "amount": 0.5, "unit": "cup" },
                { "name": "vanilla extract",  "amount": 1,   "unit": "tsp" },
            ],
            "tags": ["vegan", "dessert", "chocolate"],
            "dietaryFlags": ["vegan"],
            "prepTime": 20, "cookTime": 30, "servings": 8,
        },
        {
            "title": "Pasta Primavera",
            "description": "A light pasta dish with fresh vegetables.",
            "categoryId": categories[2],
            "authorUserId": users[14],
            "ingredients": [
                { "name": "pasta",           "amount": 200, "unit": "g" },
                { "name": "zucchini",        "amount": 1,   "unit": "whole" },
                { "name": "bell pepper",     "amount": 1,   "unit": "whole" },
                { "name": "cherry tomatoes", "amount": 1,   "unit": "cup" },
                { "name": "olive oil",       "amount": 2,   "unit": "tbsp" },
                { "name": "garlic",          "amount": 2,   "unit": "cloves" },
                { "name": "parmesan cheese", "amount": 50,  "unit": "g" },
            ],
            "tags": ["pasta", "vegetarian"],
            "dietaryFlags": ["vegetarian"],
            "prepTime": 15, "cookTime": 20, "servings": 2,
        },
        {
            "title": "Steak and Eggs",
            "description": "A hearty high-protein meal.",
            "categoryId": categories[0],
            "authorUserId": users[15],
            "ingredients": [
                { "name": "steak", "amount": 300, "unit": "g" },
                { "name": "eggs",  "amount": 2,   "unit": "whole" },
            ],
            "tags": ["steak", "eggs", "high-protein"],
            "dietaryFlags": ["high-protein"],
            "prepTime": 10, "cookTime": 15, "servings": 1,
        },
        {
            "title": "Birria Tacos",
            "description": "Delicious slow-cooked birria tacos.",
            "categoryId": categories[2],
            "authorUserId": users[16],
            "ingredients": [
                { "name": "beef",         "amount": 300, "unit": "g" },
                { "name": "taco shells",  "amount": 4,   "unit": "whole" },
                { "name": "onions",       "amount": 1,   "unit": "whole" },
                { "name": "garlic",       "amount": 2,   "unit": "cloves" },
                { "name": "chili powder", "amount": 1,   "unit": "tbsp" },
                { "name": "beef broth",   "amount": 2,   "unit": "cups" },
            ],
            "tags": ["birria", "tacos", "mexican"],
            "dietaryFlags": ["none"],
            "prepTime": 20, "cookTime": 120, "servings": 4,
        },
        {
            "title": "Chicken Teriyaki",
            "description": "A savory Japanese-inspired chicken dish.",
            "categoryId": categories[2],
            "authorUserId": users[17],
            "ingredients": [
                { "name": "chicken",        "amount": 300, "unit": "g" },
                { "name": "teriyaki sauce", "amount": 2,   "unit": "tbsp" },
                { "name": "ginger",         "amount": 1,   "unit": "tsp" },
                { "name": "garlic",         "amount": 2,   "unit": "cloves" },
                { "name": "soy sauce",      "amount": 1,   "unit": "tbsp" },
            ],
            "tags": ["chicken", "teriyaki", "japanese"],
            "dietaryFlags": ["none"],
            "prepTime": 15, "cookTime": 20, "servings": 2,
        },
        {
            "title": "Caesar Salad",
            "description": "A refreshing classic Caesar salad.",
            "categoryId": categories[0],
            "authorUserId": users[18],
            "ingredients": [
                { "name": "romaine lettuce",  "amount": 1,  "unit": "head" },
                { "name": "croutons",         "amount": 1,  "unit": "cup" },
                { "name": "parmesan cheese",  "amount": 50, "unit": "g" },
                { "name": "Caesar dressing",  "amount": 2,  "unit": "tbsp" },
            ],
            "tags": ["salad", "caesar", "vegetarian"],
            "dietaryFlags": ["vegetarian"],
            "prepTime": 10, "cookTime": 0, "servings": 2,
        },
        {
            "title": "Miso Soup",
            "description": "A comforting Japanese miso soup.",
            "categoryId": categories[0],
            "authorUserId": users[19],
            "ingredients": [
                { "name": "miso paste",   "amount": 2, "unit": "tbsp" },
                { "name": "tofu",         "amount": 100, "unit": "g" },
                { "name": "green onions", "amount": 2, "unit": "whole" },
                { "name": "dashi broth",  "amount": 4, "unit": "cups" },
            ],
            "tags": ["soup", "miso", "japanese"],
            "dietaryFlags": ["vegetarian"],
            "prepTime": 10, "cookTime": 15, "servings": 4,
        },
        {
            "title": "Spaghetti Carbonara",
            "description": "A classic Italian pasta dish.",
            "categoryId": categories[2],
            "authorUserId": users[20],
            "ingredients": [
                { "name": "spaghetti",       "amount": 200, "unit": "g" },
                { "name": "pancetta",        "amount": 100, "unit": "g" },
                { "name": "eggs",            "amount": 2,   "unit": "whole" },
                { "name": "parmesan cheese", "amount": 50,  "unit": "g" },
            ],
            "tags": ["pasta", "carbonara", "italian"],
            "dietaryFlags": ["none"],
            "prepTime": 15, "cookTime": 20, "servings": 2,
        },
        {
            "title": "Gabagool Sandwich",
            "description": "A delicious Italian-inspired sandwich.",
            "categoryId": categories[1],
            "authorUserId": users[21],
            "ingredients": [
                { "name": "gabagool",         "amount": 100, "unit": "g" },
                { "name": "italian bread",    "amount": 1,   "unit": "loaf" },
                { "name": "provolone cheese", "amount": 50,  "unit": "g" },
                { "name": "lettuce",          "amount": 1,   "unit": "cup" },
                { "name": "tomato",           "amount": 1,   "unit": "whole" },
                { "name": "italian dressing", "amount": 2,   "unit": "tbsp" },
            ],
            "tags": ["sandwich", "italian"],
            "dietaryFlags": ["none"],
            "prepTime": 10, "cookTime": 0, "servings": 2,
        },
        {
            "title": "Cordon Bleu",
            "description": "A classic French stuffed chicken dish.",
            "categoryId": categories[2],
            "authorUserId": users[22],
            "ingredients": [
                { "name": "chicken breast", "amount": 2,  "unit": "pieces" },
                { "name": "bacon",          "amount": 4,  "unit": "slices" },
                { "name": "swiss cheese",   "amount": 4,  "unit": "slices" },
                { "name": "breadcrumbs",    "amount": 1,  "unit": "cup" },
            ],
            "tags": ["chicken", "french"],
            "dietaryFlags": ["none"],
            "prepTime": 15, "cookTime": 25, "servings": 2,
        },
        {
            "title": "Four Cheese Mac and Cheese",
            "description": "A cheesy comfort food classic.",
            "categoryId": categories[6],
            "authorUserId": users[23],
            "ingredients": [
                { "name": "macaroni",          "amount": 200, "unit": "g" },
                { "name": "cheddar cheese",    "amount": 100, "unit": "g" },
                { "name": "mozzarella cheese", "amount": 100, "unit": "g" },
                { "name": "parmesan cheese",   "amount": 50,  "unit": "g" },
                { "name": "milk",              "amount": 1,   "unit": "cup" },
            ],
            "tags": ["pasta", "cheese", "comfort"],
            "dietaryFlags": ["vegetarian"],
            "prepTime": 10, "cookTime": 20, "servings": 4,
        },
        {
            "title": "Buffalo Wings",
            "description": "Spicy chicken wings for game day.",
            "categoryId": categories[4],
            "authorUserId": users[24],
            "ingredients": [
                { "name": "chicken wings",  "amount": 500, "unit": "g" },
                { "name": "buffalo sauce",  "amount": 1,   "unit": "cup" },
                { "name": "butter",         "amount": 2,   "unit": "tbsp" },
                { "name": "garlic powder",  "amount": 1,   "unit": "tsp" },
            ],
            "tags": ["chicken", "spicy", "snack"],
            "dietaryFlags": ["none"],
            "prepTime": 15, "cookTime": 25, "servings": 4,
        },
        {
            "title": "Jalapeno Poppers",
            "description": "Spicy stuffed peppers.",
            "categoryId": categories[5],
            "authorUserId": users[25],
            "ingredients": [
                { "name": "jalapeno peppers",   "amount": 10,  "unit": "whole" },
                { "name": "cream cheese",        "amount": 100, "unit": "g" },
                { "name": "garlic",              "amount": 2,   "unit": "cloves" },
                { "name": "panko breadcrumbs",   "amount": 1,   "unit": "cup" },
                { "name": "parmesan cheese",     "amount": 50,  "unit": "g" },
            ],
            "tags": ["appetizer", "spicy"],
            "dietaryFlags": ["vegetarian"],
            "prepTime": 20, "cookTime": 15, "servings": 4,
        },
        {
            "title": "Chocolate Chip Cookies",
            "description": "Classic cookies for dessert.",
            "categoryId": categories[3],
            "authorUserId": users[26],
            "ingredients": [
                { "name": "flour",           "amount": 2,   "unit": "cups" },
                { "name": "sugar",           "amount": 1,   "unit": "cup" },
                { "name": "butter",          "amount": 1,   "unit": "cup" },
                { "name": "eggs",            "amount": 2,   "unit": "whole" },
                { "name": "chocolate chips", "amount": 1,   "unit": "cup" },
                { "name": "vanilla extract", "amount": 1,   "unit": "tsp" },
                { "name": "baking soda",     "amount": 1,   "unit": "tsp" },
            ],
            "tags": ["dessert", "cookies", "baked"],
            "dietaryFlags": ["vegetarian"],
            "prepTime": 15, "cookTime": 10, "servings": 24,
        },
    ]).inserted_ids
    print(f"Seeded {len(recipes)} recipes.")

    # ── REVIEWS ──
    reviews = db.reviews.insert_many([
        { "userId": users[0],  "recipeId": recipes[0],  "rating": 5, "comment": "Perfect level of spice.",             "reviewDateTime": datetime.utcnow() },
        { "userId": users[1],  "recipeId": recipes[1],  "rating": 4, "comment": "Quick and healthy breakfast.",        "reviewDateTime": datetime.utcnow() },
        { "userId": users[2],  "recipeId": recipes[2],  "rating": 4, "comment": "Simple and filling.",                 "reviewDateTime": datetime.utcnow() },
        { "userId": users[3],  "recipeId": recipes[3],  "rating": 5, "comment": "Great for my dietary needs.",         "reviewDateTime": datetime.utcnow() },
        { "userId": users[4],  "recipeId": recipes[4],  "rating": 3, "comment": "Solid keto option.",                  "reviewDateTime": datetime.utcnow() },
        { "userId": users[5],  "recipeId": recipes[5],  "rating": 5, "comment": "Love a good stir-fry.",               "reviewDateTime": datetime.utcnow() },
        { "userId": users[6],  "recipeId": recipes[6],  "rating": 4, "comment": "Hearty and delicious.",               "reviewDateTime": datetime.utcnow() },
        { "userId": users[7],  "recipeId": recipes[7],  "rating": 5, "comment": "My go-to lunch.",                     "reviewDateTime": datetime.utcnow() },
        { "userId": users[8],  "recipeId": recipes[8],  "rating": 4, "comment": "Refreshing smoothie.",                "reviewDateTime": datetime.utcnow() },
        { "userId": users[9],  "recipeId": recipes[9],  "rating": 5, "comment": "Surprisingly good stew.",             "reviewDateTime": datetime.utcnow() },
        { "userId": users[10], "recipeId": recipes[10], "rating": 4, "comment": "Fresh and filling.",                  "reviewDateTime": datetime.utcnow() },
        { "userId": users[11], "recipeId": recipes[11], "rating": 3, "comment": "Decent smoothie.",                    "reviewDateTime": datetime.utcnow() },
        { "userId": users[12], "recipeId": recipes[12], "rating": 5, "comment": "Classic done right.",                 "reviewDateTime": datetime.utcnow() },
        { "userId": users[13], "recipeId": recipes[13], "rating": 5, "comment": "Best vegan cake ever.",               "reviewDateTime": datetime.utcnow() },
        { "userId": users[14], "recipeId": recipes[14], "rating": 4, "comment": "Light and tasty.",                    "reviewDateTime": datetime.utcnow() },
        { "userId": users[15], "recipeId": recipes[15], "rating": 5, "comment": "Breakfast of champions.",             "reviewDateTime": datetime.utcnow() },
        { "userId": users[16], "recipeId": recipes[16], "rating": 5, "comment": "Worth every minute of cook time.",   "reviewDateTime": datetime.utcnow() },
        { "userId": users[17], "recipeId": recipes[17], "rating": 4, "comment": "Great weeknight dinner.",             "reviewDateTime": datetime.utcnow() },
        { "userId": users[18], "recipeId": recipes[18], "rating": 3, "comment": "Solid classic.",                      "reviewDateTime": datetime.utcnow() },
        { "userId": users[19], "recipeId": recipes[19], "rating": 5, "comment": "Warms the soul.",                     "reviewDateTime": datetime.utcnow() },
        { "userId": users[20], "recipeId": recipes[20], "rating": 4, "comment": "Rich and satisfying.",                "reviewDateTime": datetime.utcnow() },
        { "userId": users[21], "recipeId": recipes[21], "rating": 5, "comment": "Best sandwich I have ever had.",      "reviewDateTime": datetime.utcnow() },
        { "userId": users[22], "recipeId": recipes[22], "rating": 4, "comment": "Fancy but worth it.",                 "reviewDateTime": datetime.utcnow() },
        { "userId": users[23], "recipeId": recipes[23], "rating": 5, "comment": "Ultimate comfort food.",              "reviewDateTime": datetime.utcnow() },
        { "userId": users[24], "recipeId": recipes[24], "rating": 4, "comment": "Game day essential.",                 "reviewDateTime": datetime.utcnow() },
        { "userId": users[25], "recipeId": recipes[25], "rating": 4, "comment": "Great appetizer.",                    "reviewDateTime": datetime.utcnow() },
        { "userId": users[26], "recipeId": recipes[26], "rating": 5, "comment": "Perfect every time.",                 "reviewDateTime": datetime.utcnow() },
        { "userId": users[0],  "recipeId": recipes[5],  "rating": 4, "comment": "Great vegan option.",                 "reviewDateTime": datetime.utcnow() },
        { "userId": users[1],  "recipeId": recipes[14], "rating": 5, "comment": "My favorite pasta dish.",             "reviewDateTime": datetime.utcnow() },
        { "userId": users[2],  "recipeId": recipes[17], "rating": 4, "comment": "Easy weeknight meal.",                "reviewDateTime": datetime.utcnow() },
    ]).inserted_ids
    print(f"Seeded {len(reviews)} reviews.")

    # ── SAVED RECIPES ──
    saved = db["savedRecipes"].insert_many([
        { "userId": users[0],  "recipeId": recipes[0],  "submissionDateTime": datetime.utcnow() },
        { "userId": users[1],  "recipeId": recipes[1],  "submissionDateTime": datetime.utcnow() },
        { "userId": users[2],  "recipeId": recipes[2],  "submissionDateTime": datetime.utcnow() },
        { "userId": users[3],  "recipeId": recipes[3],  "submissionDateTime": datetime.utcnow() },
        { "userId": users[4],  "recipeId": recipes[4],  "submissionDateTime": datetime.utcnow() },
        { "userId": users[5],  "recipeId": recipes[5],  "submissionDateTime": datetime.utcnow() },
        { "userId": users[6],  "recipeId": recipes[6],  "submissionDateTime": datetime.utcnow() },
        { "userId": users[7],  "recipeId": recipes[7],  "submissionDateTime": datetime.utcnow() },
        { "userId": users[8],  "recipeId": recipes[8],  "submissionDateTime": datetime.utcnow() },
        { "userId": users[9],  "recipeId": recipes[9],  "submissionDateTime": datetime.utcnow() },
        { "userId": users[10], "recipeId": recipes[10], "submissionDateTime": datetime.utcnow() },
        { "userId": users[11], "recipeId": recipes[11], "submissionDateTime": datetime.utcnow() },
        { "userId": users[12], "recipeId": recipes[12], "submissionDateTime": datetime.utcnow() },
        { "userId": users[13], "recipeId": recipes[13], "submissionDateTime": datetime.utcnow() },
        { "userId": users[14], "recipeId": recipes[14], "submissionDateTime": datetime.utcnow() },
        { "userId": users[15], "recipeId": recipes[15], "submissionDateTime": datetime.utcnow() },
        { "userId": users[16], "recipeId": recipes[16], "submissionDateTime": datetime.utcnow() },
        { "userId": users[17], "recipeId": recipes[17], "submissionDateTime": datetime.utcnow() },
        { "userId": users[18], "recipeId": recipes[18], "submissionDateTime": datetime.utcnow() },
        { "userId": users[19], "recipeId": recipes[19], "submissionDateTime": datetime.utcnow() },
        { "userId": users[20], "recipeId": recipes[20], "submissionDateTime": datetime.utcnow() },
        { "userId": users[21], "recipeId": recipes[21], "submissionDateTime": datetime.utcnow() },
        { "userId": users[22], "recipeId": recipes[22], "submissionDateTime": datetime.utcnow() },
        { "userId": users[23], "recipeId": recipes[23], "submissionDateTime": datetime.utcnow() },
        { "userId": users[24], "recipeId": recipes[24], "submissionDateTime": datetime.utcnow() },
        { "userId": users[25], "recipeId": recipes[25], "submissionDateTime": datetime.utcnow() },
        { "userId": users[26], "recipeId": recipes[26], "submissionDateTime": datetime.utcnow() },
        { "userId": users[0],  "recipeId": recipes[14], "submissionDateTime": datetime.utcnow() },
        { "userId": users[1],  "recipeId": recipes[6],  "submissionDateTime": datetime.utcnow() },
        { "userId": users[2],  "recipeId": recipes[23], "submissionDateTime": datetime.utcnow() },
    ]).inserted_ids
    print(f"Seeded {len(saved)} saved recipes.")

    # ── MEAL PLANS ──
    meal_plans = db["mealPlans"].insert_many([
        { "userId": users[0],  "weekStart": datetime(2026, 4, 13), "days": [ { "day": "Monday", "recipeId": recipes[0], "notes": "" }, { "day": "Wednesday", "recipeId": recipes[1], "notes": "" }, { "day": "Friday", "recipeId": recipes[14], "notes": "" } ], "notes": "Vegetarian week." },
        { "userId": users[1],  "weekStart": datetime(2026, 4, 13), "days": [ { "day": "Monday", "recipeId": recipes[2], "notes": "" }, { "day": "Thursday", "recipeId": recipes[15], "notes": "" } ], "notes": "High protein week." },
        { "userId": users[2],  "weekStart": datetime(2026, 4, 13), "days": [ { "day": "Tuesday", "recipeId": recipes[5], "notes": "" }, { "day": "Friday", "recipeId": recipes[13], "notes": "" } ], "notes": "Vegan week." },
        { "userId": users[3],  "weekStart": datetime(2026, 4, 13), "days": [ { "day": "Monday", "recipeId": recipes[3], "notes": "" }, { "day": "Wednesday", "recipeId": recipes[19], "notes": "" } ], "notes": "Gluten-free week." },
        { "userId": users[4],  "weekStart": datetime(2026, 4, 20), "days": [ { "day": "Monday", "recipeId": recipes[4], "notes": "" }, { "day": "Friday", "recipeId": recipes[20], "notes": "" } ], "notes": "Low carb week." },
        { "userId": users[5],  "weekStart": datetime(2026, 4, 20), "days": [ { "day": "Monday", "recipeId": recipes[5], "notes": "" }, { "day": "Wednesday", "recipeId": recipes[6], "notes": "" } ], "notes": "Vegan and paleo mix." },
        { "userId": users[6],  "weekStart": datetime(2026, 4, 20), "days": [ { "day": "Tuesday", "recipeId": recipes[6], "notes": "" }, { "day": "Saturday", "recipeId": recipes[9], "notes": "" } ], "notes": "Paleo week." },
        { "userId": users[7],  "weekStart": datetime(2026, 4, 27), "days": [ { "day": "Monday", "recipeId": recipes[7], "notes": "" }, { "day": "Friday", "recipeId": recipes[10], "notes": "" } ], "notes": "Mediterranean week." },
        { "userId": users[8],  "weekStart": datetime(2026, 4, 27), "days": [ { "day": "Monday", "recipeId": recipes[8], "notes": "" }, { "day": "Thursday", "recipeId": recipes[11], "notes": "" } ], "notes": "Smoothie week." },
        { "userId": users[9],  "weekStart": datetime(2026, 4, 27), "days": [ { "day": "Sunday", "recipeId": recipes[9], "notes": "Big batch" }, { "day": "Wednesday", "recipeId": recipes[6], "notes": "" } ], "notes": "Stew week." },
        { "userId": users[10], "weekStart": datetime(2026, 5, 4),  "days": [ { "day": "Monday", "recipeId": recipes[10], "notes": "" }, { "day": "Wednesday", "recipeId": recipes[7], "notes": "" } ], "notes": "Salad week." },
        { "userId": users[11], "weekStart": datetime(2026, 5, 4),  "days": [ { "day": "Monday", "recipeId": recipes[11], "notes": "" }, { "day": "Friday", "recipeId": recipes[8], "notes": "" } ], "notes": "Smoothie week." },
        { "userId": users[12], "weekStart": datetime(2026, 5, 4),  "days": [ { "day": "Tuesday", "recipeId": recipes[12], "notes": "" }, { "day": "Friday", "recipeId": recipes[21], "notes": "" } ], "notes": "Classic meals week." },
        { "userId": users[13], "weekStart": datetime(2026, 5, 11), "days": [ { "day": "Monday", "recipeId": recipes[13], "notes": "" }, { "day": "Thursday", "recipeId": recipes[26], "notes": "Treat" } ], "notes": "Vegan dessert week." },
        { "userId": users[14], "weekStart": datetime(2026, 5, 11), "days": [ { "day": "Monday", "recipeId": recipes[14], "notes": "" }, { "day": "Friday", "recipeId": recipes[18], "notes": "" } ], "notes": "Vegetarian week." },
        { "userId": users[15], "weekStart": datetime(2026, 5, 11), "days": [ { "day": "Monday", "recipeId": recipes[15], "notes": "" }, { "day": "Wednesday", "recipeId": recipes[2], "notes": "" } ], "notes": "Protein week." },
        { "userId": users[16], "weekStart": datetime(2026, 5, 18), "days": [ { "day": "Sunday", "recipeId": recipes[16], "notes": "Big batch" }, { "day": "Monday", "recipeId": recipes[16], "notes": "Leftovers" } ], "notes": "Taco week." },
        { "userId": users[17], "weekStart": datetime(2026, 5, 18), "days": [ { "day": "Tuesday", "recipeId": recipes[17], "notes": "" }, { "day": "Thursday", "recipeId": recipes[0], "notes": "" } ], "notes": "Asian-inspired week." },
        { "userId": users[18], "weekStart": datetime(2026, 5, 18), "days": [ { "day": "Monday", "recipeId": recipes[18], "notes": "" }, { "day": "Thursday", "recipeId": recipes[7], "notes": "" } ], "notes": "Salad week." },
        { "userId": users[19], "weekStart": datetime(2026, 5, 25), "days": [ { "day": "Monday", "recipeId": recipes[19], "notes": "" }, { "day": "Wednesday", "recipeId": recipes[1], "notes": "" } ], "notes": "Soup week." },
        { "userId": users[20], "weekStart": datetime(2026, 5, 25), "days": [ { "day": "Monday", "recipeId": recipes[20], "notes": "" }, { "day": "Friday", "recipeId": recipes[22], "notes": "" } ], "notes": "Italian week." },
        { "userId": users[21], "weekStart": datetime(2026, 5, 25), "days": [ { "day": "Tuesday", "recipeId": recipes[21], "notes": "" }, { "day": "Friday", "recipeId": recipes[12], "notes": "" } ], "notes": "Sandwich week." },
        { "userId": users[22], "weekStart": datetime(2026, 6, 1),  "days": [ { "day": "Wednesday", "recipeId": recipes[22], "notes": "" }, { "day": "Friday", "recipeId": recipes[17], "notes": "" } ], "notes": "Fancy week." },
        { "userId": users[23], "weekStart": datetime(2026, 6, 1),  "days": [ { "day": "Monday", "recipeId": recipes[23], "notes": "" }, { "day": "Friday", "recipeId": recipes[26], "notes": "Treat" } ], "notes": "Comfort food week." },
        { "userId": users[24], "weekStart": datetime(2026, 6, 1),  "days": [ { "day": "Saturday", "recipeId": recipes[24], "notes": "Game day!" }, { "day": "Sunday", "recipeId": recipes[25], "notes": "" } ], "notes": "Game day week." },
        { "userId": users[25], "weekStart": datetime(2026, 6, 8),  "days": [ { "day": "Monday", "recipeId": recipes[25], "notes": "" }, { "day": "Thursday", "recipeId": recipes[5], "notes": "" } ], "notes": "Light week." },
        { "userId": users[26], "weekStart": datetime(2026, 6, 8),  "days": [ { "day": "Monday", "recipeId": recipes[26], "notes": "Baking day" }, { "day": "Friday", "recipeId": recipes[13], "notes": "" } ], "notes": "Baking week." },
    ]).inserted_ids
    print(f"Seeded {len(meal_plans)} meal plans.")

    print("\nSeed complete!")
    print(f"  Users:        {len(users)}")
    print(f"  Categories:   {len(categories)}")
    print(f"  Recipes:      {len(recipes)}")
    print(f"  Reviews:      {len(reviews)}")
    print(f"  Saved:        {len(saved)}")
    print(f"  Meal plans:   {len(meal_plans)}")

if __name__ == "__main__":
    seed()
