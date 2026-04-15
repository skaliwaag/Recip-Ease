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
    db.saved_recipes.drop()
    db.meal_plans.drop()
    print("Cleared collections.")

    # ── CATEGORIES ──
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
    users = db.users.insert_many([
        { "name": "Maria Santos",        "email": "maria@example.com",                    "dietary_preferences": ["vegetarian", "gluten-free"], "favorite_categories": [categories[0]], "created_at": datetime.utcnow() },
        { "name": "Alice Johnson",        "email": "alice@gmail.com",                      "dietary_preferences": ["vegetarian"],                 "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Bob Smith",            "email": "bob@bobby.com",                        "dietary_preferences": ["high-protein"],               "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Laura Palmer",         "email": "laurapalmer@twinpeaks.com",            "dietary_preferences": ["gluten-free"],                "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Dale Cooper",          "email": "dalecooper@fbi.gov",                   "dietary_preferences": ["low-carb"],                   "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Roger Huntington",     "email": "borntobleed@gmail.com",                "dietary_preferences": ["high-protein"],               "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "John Doe",             "email": "john.doe@missing.com",                 "dietary_preferences": ["vegan"],                      "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "John Wick",            "email": "john.wick@continental.com",            "dietary_preferences": ["high-protein"],               "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Stu Macher",           "email": "stu.macher@scarymovies.com",           "dietary_preferences": ["low-carb"],                   "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Billy Loomis",         "email": "billy.loomis@scarymovies.com",         "dietary_preferences": ["low-carb"],                   "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Silent Bob",           "email": "silentbob@viewaskew.com",              "dietary_preferences": ["vegan"],                      "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Fox Mulder",           "email": "fox.mulder@fbi.gov",                   "dietary_preferences": ["mediterranean"],              "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Ash Williams",         "email": "ash.williams@necronomicon.com",        "dietary_preferences": ["paleo"],                      "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Vincent Vega",         "email": "vincent.vega@pulpfiction.com",         "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Jules Winnfield",      "email": "jules.winnfield@pulpfiction.com",      "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Charlie Dompler",      "email": "charlie.dompler@SmilingFriends.net",   "dietary_preferences": ["vegan"],                      "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Pim Pimling",          "email": "pim.pimling@smilingfriends.net",       "dietary_preferences": ["vegetarian"],                 "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Allan Red",            "email": "allan.red@smilingfriends.net",         "dietary_preferences": ["high-protein"],               "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Walter White",         "email": "walter.white@breakingbad.com",         "dietary_preferences": ["high-protein"],               "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Jesse Pinkman",        "email": "jesse.pinkman@breakingbad.com",        "dietary_preferences": ["low-carb"],                   "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Dexter Morgan",        "email": "dexter.morgan@darkmatter.com",         "dietary_preferences": ["paleo"],                      "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Sneakers O'Toole",     "email": "sneakers.otoole@gmail.com",            "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Dio Brando",           "email": "dio.brando@gmail.com",                 "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Dan Smith",            "email": "dan.smith@gmail.com",                  "dietary_preferences": ["vegan"],                      "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Terry Crews",          "email": "terry.crews@gmail.com",                "dietary_preferences": ["high-protein"],               "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Sarah Connor",         "email": "sarah.connor@terminator.com",          "dietary_preferences": ["paleo"],                      "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "James Bond",           "email": "james.bond@mi6.uk",                    "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Jane Kilcher",         "email": "jane.kilcher@gmail.com",               "dietary_preferences": ["paleo"],                      "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Kurt Hummel",          "email": "kurt.hummel@gmail.com",                "dietary_preferences": ["vegetarian"],                 "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Rachel Green",         "email": "rachel.green@friends.com",             "dietary_preferences": ["vegetarian"],                 "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Jay Mewes",            "email": "jay.mewes@viewaskew.com",              "dietary_preferences": ["vegan"],                      "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Shaggy Rogers",        "email": "shaggy.rogers@monsterhunters.com",     "dietary_preferences": ["vegetarian"],                 "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Fred Jones",           "email": "fred.jones@monsterhunters.com",        "dietary_preferences": ["high-protein"],               "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Velma Dinkley",        "email": "velma.dinkley@twinpeaks.com",          "dietary_preferences": ["gluten-free"],                "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Daphnie Blake",        "email": "daphnie.blake@monsterhunters.com",     "dietary_preferences": ["vegetarian"],                 "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Chev Chelios",         "email": "unstoppable@crank.com",                "dietary_preferences": ["high-protein"],               "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "John McClane",         "email": "john.mcclane@diehard.com",             "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Black Dynamite",       "email": "black.dynamite@fbi.gov",               "dietary_preferences": ["high-protein"],               "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Duke Nukem",           "email": "duke.nukem@3drealms.com",              "dietary_preferences": ["low-carb"],                   "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Richard B. Riddick",   "email": "richard.riddick@pitchblack.com",       "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Henry Dorsett Case",   "email": "henry.dorsett.case@Neuromancer.com",   "dietary_preferences": ["futuristic"],                 "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Neo Anderson",         "email": "neo.anderson@matrix.com",              "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Morpheus",             "email": "morpheus@matrix.com",                  "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Masao Kakihara",       "email": "kakihara@yakuza.com",                  "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Ronnie James Dio",     "email": "holydiver@thelastinline.com",           "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Bob Clarkson",         "email": "bob.clarkson@gmail.com",               "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Terry Gilliam",        "email": "tgilliam@montypython.com",             "dietary_preferences": ["vegan"],                      "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "The Black Knight",     "email": "BlackKnight@montypython.com",          "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Hiro Protagonist",     "email": "hiro.protagonist@snowcrash.com",       "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Kirby Reed",           "email": "kirby.reed@fbi.gov",                   "dietary_preferences": ["none"],                       "favorite_categories": [],              "created_at": datetime.utcnow() },
        { "name": "Daria Morgendorffer",  "email": "daria.morgendorffer@sadsickworld.com", "dietary_preferences": ["vegetarian"],                 "favorite_categories": [],              "created_at": datetime.utcnow() },
    ]).inserted_ids
    print(f"Seeded {len(users)} users.")

    # ── RECIPES ──
    recipes = db.recipes.insert_many([
        {
            "title": "Chicken Tikka Masala",
            "description": "A rich, creamy tomato-based curry.",
            "category_id": categories[2],
            "author_user_id": users[0],
            "ingredients": [
                { "name": "chicken breast", "amount": 500, "unit": "g" },
                { "name": "heavy cream",    "amount": 200, "unit": "ml" },
                { "name": "garam masala",   "amount": 2,   "unit": "tsp" },
            ],
            "tags": ["curry", "Indian", "comfort food"],
            "dietary_flags": ["gluten-free", "high-protein"],
            "prep_time": 20, "cook_time": 35, "servings": 4,
        },
        {
            "title": "Veggie Omelette",
            "description": "Healthy vegetarian omelette.",
            "category_id": categories[0],
            "author_user_id": users[1],
            "ingredients": [
                { "name": "eggs",    "amount": 2,   "unit": "whole" },
                { "name": "spinach", "amount": 1,   "unit": "cup" },
            ],
            "tags": ["vegetarian", "breakfast"],
            "dietary_flags": ["vegetarian"],
            "prep_time": 5, "cook_time": 10, "servings": 1,
        },
        {
            "title": "Grilled Chicken",
            "description": "High protein dinner.",
            "category_id": categories[2],
            "author_user_id": users[2],
            "ingredients": [
                { "name": "chicken breast", "amount": 200, "unit": "g" },
            ],
            "tags": ["protein", "simple"],
            "dietary_flags": ["high-protein"],
            "prep_time": 10, "cook_time": 20, "servings": 2,
        },
        {
            "title": "Gluten-Free Pasta",
            "description": "Pasta for gluten-sensitive diets.",
            "category_id": categories[1],
            "author_user_id": users[3],
            "ingredients": [
                { "name": "gluten-free pasta", "amount": 100, "unit": "g" },
                { "name": "tomato sauce",       "amount": 1,   "unit": "cup" },
            ],
            "tags": ["gluten-free", "pasta"],
            "dietary_flags": ["gluten-free"],
            "prep_time": 15, "cook_time": 15, "servings": 2,
        },
        {
            "title": "Keto Salad",
            "description": "Low-carb salad for keto diet.",
            "category_id": categories[1],
            "author_user_id": users[4],
            "ingredients": [
                { "name": "lettuce",  "amount": 2,  "unit": "cups" },
                { "name": "avocado",  "amount": 1,  "unit": "whole" },
                { "name": "bacon",    "amount": 50, "unit": "g" },
            ],
            "tags": ["keto", "salad", "low-carb"],
            "dietary_flags": ["low-carb"],
            "prep_time": 10, "cook_time": 0, "servings": 1,
        },
        {
            "title": "Vegan Stir-Fry",
            "description": "Quick and easy vegan stir-fry.",
            "category_id": categories[2],
            "author_user_id": users[5],
            "ingredients": [
                { "name": "tofu",              "amount": 200, "unit": "g" },
                { "name": "mixed vegetables",  "amount": 2,   "unit": "cups" },
                { "name": "soy sauce",         "amount": 2,   "unit": "tbsp" },
            ],
            "tags": ["vegan", "stir-fry"],
            "dietary_flags": ["vegan"],
            "prep_time": 15, "cook_time": 10, "servings": 2,
        },
        {
            "title": "Paleo Beef Stew",
            "description": "Hearty beef stew for paleo diet.",
            "category_id": categories[2],
            "author_user_id": users[6],
            "ingredients": [
                { "name": "beef chunks", "amount": 300, "unit": "g" },
                { "name": "carrots",     "amount": 2,   "unit": "whole" },
                { "name": "potatoes",    "amount": 2,   "unit": "whole" },
                { "name": "beef broth",  "amount": 2,   "unit": "cups" },
            ],
            "tags": ["paleo", "stew"],
            "dietary_flags": ["paleo"],
            "prep_time": 20, "cook_time": 120, "servings": 4,
        },
        {
            "title": "Mediterranean Quinoa Salad",
            "description": "Light and healthy quinoa salad.",
            "category_id": categories[1],
            "author_user_id": users[7],
            "ingredients": [
                { "name": "quinoa",      "amount": 1,  "unit": "cup" },
                { "name": "cucumber",    "amount": 1,  "unit": "whole" },
                { "name": "tomatoes",    "amount": 2,  "unit": "whole" },
                { "name": "feta cheese", "amount": 50, "unit": "g" },
                { "name": "olive oil",   "amount": 2,  "unit": "tbsp" },
            ],
            "tags": ["mediterranean", "salad"],
            "dietary_flags": ["mediterranean"],
            "prep_time": 15, "cook_time": 15, "servings": 2,
        },
        {
            "title": "Red Smoothie",
            "description": "A simple red berry smoothie.",
            "category_id": categories[0],
            "author_user_id": users[8],
            "ingredients": [
                { "name": "red berries",  "amount": 1, "unit": "cup" },
                { "name": "almond milk",  "amount": 1, "unit": "cup" },
                { "name": "chia seeds",   "amount": 2, "unit": "tbsp" },
            ],
            "tags": ["smoothie", "breakfast"],
            "dietary_flags": ["vegan"],
            "prep_time": 5, "cook_time": 0, "servings": 1,
        },
        {
            "title": "Rabbit Stew",
            "description": "Stew made with rabbit meat.",
            "category_id": categories[2],
            "author_user_id": users[9],
            "ingredients": [
                { "name": "rabbit meat",  "amount": 300, "unit": "g" },
                { "name": "carrots",      "amount": 2,   "unit": "whole" },
                { "name": "potatoes",     "amount": 2,   "unit": "whole" },
                { "name": "onions",       "amount": 1,   "unit": "whole" },
                { "name": "garlic",       "amount": 2,   "unit": "cloves" },
                { "name": "rabbit broth", "amount": 2,   "unit": "cups" },
            ],
            "tags": ["stew", "rabbit"],
            "dietary_flags": ["paleo"],
            "prep_time": 20, "cook_time": 120, "servings": 4,
        },
        {
            "title": "Asian Salad",
            "description": "A fresh salad inspired by Asian flavors.",
            "category_id": categories[1],
            "author_user_id": users[10],
            "ingredients": [
                { "name": "lettuce",   "amount": 2, "unit": "cups" },
                { "name": "avocado",   "amount": 1, "unit": "whole" },
                { "name": "quinoa",    "amount": 1, "unit": "cup" },
                { "name": "edamame",   "amount": 1, "unit": "cup" },
                { "name": "soy sauce", "amount": 2, "unit": "tbsp" },
            ],
            "tags": ["asian", "salad"],
            "dietary_flags": ["vegan"],
            "prep_time": 15, "cook_time": 10, "servings": 2,
        },
        {
            "title": "Kale Smoothie",
            "description": "A simple kale smoothie.",
            "category_id": categories[0],
            "author_user_id": users[11],
            "ingredients": [
                { "name": "kale",        "amount": 2, "unit": "cups" },
                { "name": "banana",      "amount": 1, "unit": "whole" },
                { "name": "almond milk", "amount": 1, "unit": "cup" },
            ],
            "tags": ["smoothie", "healthy"],
            "dietary_flags": ["vegan"],
            "prep_time": 5, "cook_time": 0, "servings": 1,
        },
        {
            "title": "Fish and Chips",
            "description": "Classic British dish.",
            "category_id": categories[2],
            "author_user_id": users[12],
            "ingredients": [
                { "name": "fish fillets", "amount": 200, "unit": "g" },
                { "name": "potatoes",     "amount": 2,   "unit": "whole" },
                { "name": "flour",        "amount": 1,   "unit": "cup" },
                { "name": "beer",         "amount": 1,   "unit": "cup" },
            ],
            "tags": ["fish", "british"],
            "dietary_flags": ["none"],
            "prep_time": 15, "cook_time": 20, "servings": 2,
        },
        {
            "title": "Vegan Chocolate Cake",
            "description": "A delicious vegan chocolate cake.",
            "category_id": categories[3],
            "author_user_id": users[13],
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
            "dietary_flags": ["vegan"],
            "prep_time": 20, "cook_time": 30, "servings": 8,
        },
        {
            "title": "Pasta Primavera",
            "description": "A light pasta dish with fresh vegetables.",
            "category_id": categories[2],
            "author_user_id": users[14],
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
            "dietary_flags": ["vegetarian"],
            "prep_time": 15, "cook_time": 20, "servings": 2,
        },
        {
            "title": "Steak and Eggs",
            "description": "A hearty high-protein meal.",
            "category_id": categories[0],
            "author_user_id": users[15],
            "ingredients": [
                { "name": "steak", "amount": 300, "unit": "g" },
                { "name": "eggs",  "amount": 2,   "unit": "whole" },
            ],
            "tags": ["steak", "eggs", "high-protein"],
            "dietary_flags": ["high-protein"],
            "prep_time": 10, "cook_time": 15, "servings": 1,
        },
        {
            "title": "Birria Tacos",
            "description": "Delicious slow-cooked birria tacos.",
            "category_id": categories[2],
            "author_user_id": users[16],
            "ingredients": [
                { "name": "beef",         "amount": 300, "unit": "g" },
                { "name": "taco shells",  "amount": 4,   "unit": "whole" },
                { "name": "onions",       "amount": 1,   "unit": "whole" },
                { "name": "garlic",       "amount": 2,   "unit": "cloves" },
                { "name": "chili powder", "amount": 1,   "unit": "tbsp" },
                { "name": "beef broth",   "amount": 2,   "unit": "cups" },
            ],
            "tags": ["birria", "tacos", "mexican"],
            "dietary_flags": ["none"],
            "prep_time": 20, "cook_time": 120, "servings": 4,
        },
        {
            "title": "Chicken Teriyaki",
            "description": "A savory Japanese-inspired chicken dish.",
            "category_id": categories[2],
            "author_user_id": users[17],
            "ingredients": [
                { "name": "chicken",        "amount": 300, "unit": "g" },
                { "name": "teriyaki sauce", "amount": 2,   "unit": "tbsp" },
                { "name": "ginger",         "amount": 1,   "unit": "tsp" },
                { "name": "garlic",         "amount": 2,   "unit": "cloves" },
                { "name": "soy sauce",      "amount": 1,   "unit": "tbsp" },
            ],
            "tags": ["chicken", "teriyaki", "japanese"],
            "dietary_flags": ["none"],
            "prep_time": 15, "cook_time": 20, "servings": 2,
        },
        {
            "title": "Caesar Salad",
            "description": "A refreshing classic Caesar salad.",
            "category_id": categories[0],
            "author_user_id": users[18],
            "ingredients": [
                { "name": "romaine lettuce",  "amount": 1,  "unit": "head" },
                { "name": "croutons",         "amount": 1,  "unit": "cup" },
                { "name": "parmesan cheese",  "amount": 50, "unit": "g" },
                { "name": "Caesar dressing",  "amount": 2,  "unit": "tbsp" },
            ],
            "tags": ["salad", "caesar", "vegetarian"],
            "dietary_flags": ["vegetarian"],
            "prep_time": 10, "cook_time": 0, "servings": 2,
        },
        {
            "title": "Miso Soup",
            "description": "A comforting Japanese miso soup.",
            "category_id": categories[0],
            "author_user_id": users[19],
            "ingredients": [
                { "name": "miso paste",   "amount": 2, "unit": "tbsp" },
                { "name": "tofu",         "amount": 100, "unit": "g" },
                { "name": "green onions", "amount": 2, "unit": "whole" },
                { "name": "dashi broth",  "amount": 4, "unit": "cups" },
            ],
            "tags": ["soup", "miso", "japanese"],
            "dietary_flags": ["vegetarian"],
            "prep_time": 10, "cook_time": 15, "servings": 4,
        },
        {
            "title": "Spaghetti Carbonara",
            "description": "A classic Italian pasta dish.",
            "category_id": categories[2],
            "author_user_id": users[20],
            "ingredients": [
                { "name": "spaghetti",       "amount": 200, "unit": "g" },
                { "name": "pancetta",        "amount": 100, "unit": "g" },
                { "name": "eggs",            "amount": 2,   "unit": "whole" },
                { "name": "parmesan cheese", "amount": 50,  "unit": "g" },
            ],
            "tags": ["pasta", "carbonara", "italian"],
            "dietary_flags": ["none"],
            "prep_time": 15, "cook_time": 20, "servings": 2,
        },
        {
            "title": "Gabagool Sandwich",
            "description": "A delicious Italian-inspired sandwich.",
            "category_id": categories[1],
            "author_user_id": users[21],
            "ingredients": [
                { "name": "gabagool",         "amount": 100, "unit": "g" },
                { "name": "italian bread",    "amount": 1,   "unit": "loaf" },
                { "name": "provolone cheese", "amount": 50,  "unit": "g" },
                { "name": "lettuce",          "amount": 1,   "unit": "cup" },
                { "name": "tomato",           "amount": 1,   "unit": "whole" },
                { "name": "italian dressing", "amount": 2,   "unit": "tbsp" },
            ],
            "tags": ["sandwich", "italian"],
            "dietary_flags": ["none"],
            "prep_time": 10, "cook_time": 0, "servings": 2,
        },
        {
            "title": "Cordon Bleu",
            "description": "A classic French stuffed chicken dish.",
            "category_id": categories[2],
            "author_user_id": users[22],
            "ingredients": [
                { "name": "chicken breast", "amount": 2,  "unit": "pieces" },
                { "name": "bacon",          "amount": 4,  "unit": "slices" },
                { "name": "swiss cheese",   "amount": 4,  "unit": "slices" },
                { "name": "breadcrumbs",    "amount": 1,  "unit": "cup" },
            ],
            "tags": ["chicken", "french"],
            "dietary_flags": ["none"],
            "prep_time": 15, "cook_time": 25, "servings": 2,
        },
        {
            "title": "Four Cheese Mac and Cheese",
            "description": "A cheesy comfort food classic.",
            "category_id": categories[6],
            "author_user_id": users[23],
            "ingredients": [
                { "name": "macaroni",          "amount": 200, "unit": "g" },
                { "name": "cheddar cheese",    "amount": 100, "unit": "g" },
                { "name": "mozzarella cheese", "amount": 100, "unit": "g" },
                { "name": "parmesan cheese",   "amount": 50,  "unit": "g" },
                { "name": "milk",              "amount": 1,   "unit": "cup" },
            ],
            "tags": ["pasta", "cheese", "comfort"],
            "dietary_flags": ["vegetarian"],
            "prep_time": 10, "cook_time": 20, "servings": 4,
        },
        {
            "title": "Buffalo Wings",
            "description": "Spicy chicken wings for game day.",
            "category_id": categories[4],
            "author_user_id": users[24],
            "ingredients": [
                { "name": "chicken wings",  "amount": 500, "unit": "g" },
                { "name": "buffalo sauce",  "amount": 1,   "unit": "cup" },
                { "name": "butter",         "amount": 2,   "unit": "tbsp" },
                { "name": "garlic powder",  "amount": 1,   "unit": "tsp" },
            ],
            "tags": ["chicken", "spicy", "snack"],
            "dietary_flags": ["none"],
            "prep_time": 15, "cook_time": 25, "servings": 4,
        },
        {
            "title": "Jalapeno Poppers",
            "description": "Spicy stuffed peppers.",
            "category_id": categories[5],
            "author_user_id": users[25],
            "ingredients": [
                { "name": "jalapeno peppers",   "amount": 10,  "unit": "whole" },
                { "name": "cream cheese",        "amount": 100, "unit": "g" },
                { "name": "garlic",              "amount": 2,   "unit": "cloves" },
                { "name": "panko breadcrumbs",   "amount": 1,   "unit": "cup" },
                { "name": "parmesan cheese",     "amount": 50,  "unit": "g" },
            ],
            "tags": ["appetizer", "spicy"],
            "dietary_flags": ["vegetarian"],
            "prep_time": 20, "cook_time": 15, "servings": 4,
        },
        {
            "title": "Chocolate Chip Cookies",
            "description": "Classic cookies for dessert.",
            "category_id": categories[3],
            "author_user_id": users[26],
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
            "dietary_flags": ["vegetarian"],
            "prep_time": 15, "cook_time": 10, "servings": 24,
        },
    ]).inserted_ids
    print(f"Seeded {len(recipes)} recipes.")

    # ── REVIEWS ──
    # TODO expand to 25+ documents
    reviews = db.reviews.insert_many([
        { "user_id": users[0], "recipe_id": recipes[0], "rating": 5, "comment": "Perfect level of spice.", "created_at": datetime.utcnow() },
    ]).inserted_ids
    print(f"Seeded {len(reviews)} reviews.")

    # ── SAVED RECIPES ──
    # TODO: expand to 25+ documents
    saved = db.saved_recipes.insert_many([
        { "user_id": users[0], "recipe_id": recipes[0], "saved_at": datetime.utcnow() },
    ]).inserted_ids
    print(f"Seeded {len(saved)} saved recipes.")

    # ── MEAL PLANS ──
    # TODO: expand to 25+ documents
    meal_plans = db.meal_plans.insert_many([
        {
            "user_id": users[0],
            "week_start": datetime(2026, 4, 13),
            "days": [
                { "day": "Monday", "recipe_id": recipes[0], "notes": "" },
            ],
            "notes": "Test week.",
        },
    ]).inserted_ids
    print(f"Seeded {len(meal_plans)} meal plans.")

    print("\n✓ Seed complete!")
    print(f"  Users:        {len(users)}")
    print(f"  Categories:   {len(categories)}")
    print(f"  Recipes:      {len(recipes)}")
    print(f"  Reviews:      {len(reviews)}")
    print(f"  Saved:        {len(saved)}")
    print(f"  Meal plans:   {len(meal_plans)}")

if __name__ == "__main__":
    seed()
