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
        { "name": "Dinner", "description": "Evening meals", "tags": ["hearty", "main course"] },
    ]).inserted_ids

    # ── USERS ──
    users = db.users.insert_many([
        {
            "name": "Maria Santos",
            "email": "maria@example.com",
            "dietary_preferences": ["vegetarian", "gluten-free"],
            "favorite_categories": [categories[0]],
        },
        def seedusers ():
    users = [
        {
            "name": "Alice Johnson",
            "email": "alice@gmail.com",
            "dietpreferences": ["vegetarian"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Bob Smith",
            "email": "bob@bobby.com",
            "dietpreferences": ["high-protein"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Laura Palmer",
            "email": "laurapalmer@twinpeaks.com",
            "dietpreferences": ["gluten-free"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Dale Cooper",
            "email": "dalecooper@fbi.gov",
            "dietpreferences": ["low-carb"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Roger Huntington",
            "email": "borntobleed@gmail.com",
            "dietpreferences": ["high-protein"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "John Doe",
            "email": "john.doe@missing.com",
            "dietpreferences": ["vegan"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "John Wick",
            "email": "john.wick@continental.com",
            "dietpreferences": ["high-protein"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Stu Macher",
            "email": "stu.macher@scarymovies.com",
            "dietpreferences": ["low-carb"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Billy Loomis",
            "email": "billy.loomis@scarymovies.com",
            "dietpreferences": ["low-carb"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Silent Bob",
            "email": "silentbob@viewaskew.com",
            "dietpreferences": ["vegan"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Fox Mulder",
            "email": "fox.mulder@fbi.gov",
            "dietpreferences": ["mediterranean"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Ash Williams",
            "email": "ash.williams@necronomicon.com",
            "dietpreferences": ["paleo"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Vincent Vega",
            "email": "vincent.vega@pulpfiction.com",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Jules Winnfield",
            "email": "jules.winnfield@pulpfiction.com",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Charlie Dompler",
            "email": "charlie.dompler@SmilingFriends.net",
            "dietpreferences": ["vegan"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Pim Pimling",
            "email": "pim.pimling@smilingfriends.net",
            "dietpreferences": ["vegetarian"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Allan Red",
            "email": "allan.red@smilingfriends.net",
            "dietpreferences": ["high-protein"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Walter White",
            "email": "walter.white@breakingbad.com",
            "dietpreferences": ["high-protein"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Jesse Pinkman",
            "email": "jesse.pinkman@breakingbad.com",
            "dietpreferences": ["low-carb"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Dexter Morgan",
            "email": "dexter.morgan@darkmatter.com",
            "dietpreferences": ["paleo"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Sneakers O'Toole",
            "email": "sneakers.otoole@gmail.com",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Dio Brando",
            "email": "dio.brando@gmail.com",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Dan Smith",
            "email": "dan.smith@gmail.com",
            "dietpreferences": ["vegan"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Terry Crews",
            "email": "terry.crews@gmail.com",
            "dietpreferences": ["high-protein"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Sarah Connor",
            "email": "sarah.connor@terminator.com",
            "dietpreferences": ["paleo"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "James Bond",
            "email": "james.bond@mi6.uk",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Jane Kilcher",
            "email": "jane.kilcher@gmail.com",
            "dietpreferences": ["paleo"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Kurt Hummel",
            "email": "kurt.hummel@gmail.com",
            "dietpreferences": ["vegetarian"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Rachel Green",
            "email": "rachel.green@friends.com",
            "dietpreferences": ["vegetarian"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Jay Mewes",
            "email": "jay.mewes@viewaskew.com",
            "dietpreferences": ["vegan"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Shaggy Rogers",
            "email": "shaggy.rogers@monsterhunters.com",
            "dietpreferences": ["vegetarian"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Fred Jones",
            "email": "fred.jones@monsterhunters.com",
            "dietpreferences": ["high-protein"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Velma Dinkley",
            "email": "velma.dinkley@twinpeaks.com",
            "dietpreferences": ["gluten-free"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Daphnie Blake",
            "email": "daphnie.blake@monsterhunters.com",
            "dietpreferences": ["vegetarian"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Chev Chelios",
            "email": "unstoppable@crank.com",
            "dietpreferences": ["high-protein"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "John McClane",
            "email": "john.mcclane@diehard.com",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Black Dynamite",
            "email": "black.dynamite@fbi.gov",
            "dietpreferences": ["high-protein"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Duke Nukem",
            "email": "duke.nukem@3drealms.com",
            "dietpreferences": ["low-carb"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Richard B. Riddick",
            "email": "richard.riddick@pitchblack.com",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Henry Dorsett Case",
            "email": "henry.dorsett.case@Neuromancer.com",
            "dietpreferences": ["futuristic"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Neo Anderson",
            "email": "neo.anderson@matrix.com",
            "dietpreferences": ["red-pills-only"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Morpheus",
            "email": "morpheus@matrix.com",
            "dietpreferences": ["red-pills-only"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Masao Kakihara",
            "email": "kakihara@yakuza.com",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Ronnie James Dio",
            "email": "holydiver@thelastinline.com",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Bob Clarkson",
            "email": "bob.clarkson@gmail.com",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Terry Gilliam",
            "email": "tgilliam@montypython.com",
            "dietpreferences": ["vegan"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "The Black Knight",
            "email": "BlackKnight@montypython.com",
            "dietpreferences": ["rabbit-only"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Hiro Protagonist",
            "email": "hiro.protagonist@snowcrash.com",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Kirby Reed",
            "email": "kirby.reed@fbi.gov",
            "dietpreferences": ["none"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        },
        {
            "name": "Daria Morgendorffer",
            "email": "daria.morgendorffer@sadsickworld.com",
            "dietpreferences": ["vegetarian"],
            "favcategories": [],
            "creationdate": datetime.utcnow()
        }
        
    ]
    ]).inserted_ids

    # ── RECIPES ──
    recipes = db.recipes.insert_many([
        {
            "title": "Chicken Tikka Masala",
            "description": "A rich, creamy tomato-based curry.",
            "category_id": categories[0],
            "author_user_id": users[0],
            "ingredients": [
                { "name": "chicken breast", "amount": 500, "unit": "g" },
                { "name": "heavy cream",    "amount": 200, "unit": "ml" },
                { "name": "garam masala",   "amount": 2,   "unit": "tsp" },
            ],
            "tags": ["curry", "Indian", "comfort food"],
            "dietary_flags": ["gluten-free", "high-protein"],
            "prep_time": 20,
            "cook_time": 35,
            "servings": 4,
        },
        {
            "title": "Veggie Omelette",
            "description": "Healthy vegetarian omelette",
            "categoryid": categoryids[0],
            "authoruserid": userids[0],
            "ingredients": [
                {"name": "Eggs", "quantity": 2},
                {"name": "Spinach", "quantity": "1 cup"}
            ],
            "tags": ["vegetarian"],
            "dietary_flags": ["vegetarian"],
            "preptime": 5,
            "cooktime": 10,
            "servings": 1
        },
        {
            "title": "Grilled Chicken",
            "description": "High protein dinner",
            "categoryid": categoryids[1],
            "authoruserid": userids[1],
            "ingredients": [
                {"name": "Chicken breast", "quantity": "200g"}
            ],
            "tags": ["protein"],
            "dietary_flags": ["high-protein"],
            "preptime": 10,
            "cooktime": 20,
            "servings": 2
        },
        {
            "title": "Gluten-Free Pasta",
            "description": "Pasta for gluten-sensitive",    
            "categoryid": categoryids[1],
            "authoruserid": userids[2],
            "ingredients": [
                {"name": "Gluten-free pasta", "quantity": "100g"},
                {"name": "Tomato sauce", "quantity": "1 cup"}
            ],
            "tags": ["gluten-free"],
            "dietary_flags": ["gluten-free"],
            "preptime": 15,
            "cooktime": 15,
            "servings": 2
        },
        {   
            "title": "Keto Salad",
            "description": "Low-carb salad for keto diet",
            "categoryid": categoryids[1],
            "authoruserid": userids[3],
            "ingredients": [
                {"name": "Lettuce", "quantity": "2 cups"},
                {"name": "Avocado", "quantity": 1},
                {"name": "Bacon", "quantity": "50g"}
            ],          
            "tags": ["keto", "salad"],
            "dietary_flags": ["low-carb"],
            "preptime": 10,
            "cooktime": 0,
            "servings": 1
        },
        {
            "title": "Vegan Stir-Fry",
            "description": "Quick and easy vegan stir-fry",
            "categoryid": categoryids[1],
            "authoruserid": userids[4],
            "ingredients": [
                {"name": "Tofu", "quantity": "200g"},
                {"name": "Mixed vegetables", "quantity": "2 cups"},
                {"name": "Soy sauce", "quantity": "2 tbsp"}
            ],
            "tags": ["vegan", "stir-fry"],
            "dietary_flags": ["vegan"],
            "preptime": 15,
            "cooktime": 10,
            "servings": 2
        },
        {
            "title": "Paleo Beef Stew",
            "description": "Hearty beef stew for paleo diet",
            "categoryid": categoryids[1],
            "authoruserid": userids[5],
            "ingredients": [
                {"name": "Beef chunks", "quantity": "300g"},
                {"name": "Carrots", "quantity": "2"},
                {"name": "Potatoes", "quantity": "2"},
                {"name": "Beef broth", "quantity": "2 cups"}
            ],
            "tags": ["paleo", "stew"],
            "dietary_flags": ["paleo"],
            "preptime": 20,
            "cooktime": 120,
            "servings": 4
        },
        {
            "title": "Mediterranean Quinoa Salad",
            "description": "Light and healthy quinoa salad",    
            "categoryid": categoryids[1],
            "authoruserid": userids[6], 
            "ingredients": [
                {"name": "Quinoa", "quantity": "1 cup"},
                {"name": "Cucumber", "quantity": 1},
                {"name": "Tomatoes", "quantity": "2"},
                {"name": "Feta cheese", "quantity": "50g"},
                {"name": "Olive oil", "quantity": "2 tbsp"}
            ],  
            "tags": ["mediterranean", "salad"],
            "dietary_flags": ["mediterranean"],
            "preptime": 15,
            "cooktime": 15,
            "servings": 2
        },
        {
            "title": "Red Smoothie",
            "description": "A simple red berry smoothie.",
            "categoryid": categoryids[0],
            "authoruserid": userids[7],
            "ingredients": [
                {"name": "Red berries", "quantity": "1 cup"},
                {"name": "Almond milk", "quantity": "1 cup"},
                {"name": "Chia seeds", "quantity": "2 tbsp"}
            ],
            "tags": ["red-pill", "smoothie"],
            "dietary_flags": ["red-pills-only"],
            "preptime": 5,
            "cooktime": 0,
            "servings": 1
        },
            {
                "title": "Rabbit Stew",
                "description": "Stew made with rabbit meat.",
                "categoryid": categoryids[1],
                "authoruserid": userids[8],
                "ingredients": [
                    {"name": "Rabbit meat", "quantity": "300g"},
                    {"name": "Carrots", "quantity": "2"},
                    {"name": "Potatoes", "quantity": "2"},
                    {"name": "Onions", "quantity": 1},
                    {"name": "Garlic", "quantity": 2},
                    {"name": "Rabbit broth", "quantity": "2 cups"}
                ],
                "tags": ["rabbit-only", "stew"],
                "dietary_flags": ["rabbit-only"],
                "preptime": 20,
                "cooktime": 120,
                "servings": 4   
            },
            {
                "title": "Asian Salad",
                "description": "A futuristic salad inspired by Asian flavors.",
                "categoryid": categoryids[1],
                "authoruserid": userids[9],
                "ingredients": [
                    {"name": "Lettuce", "quantity": "2 cups"},
                    {"name": "Avocado", "quantity": 1},
                    {"name": "Quinoa", "quantity": "1 cup"},
                    {"name": "Edamame", "quantity": "1 cup"},
                    {"name": "Soy sauce", "quantity": "2 tbsp"}
                ],  
                "tags": ["futuristic", "salad"],
                "dietary_flags": ["futuristic"],
                "preptime": 15,
                "cooktime": 10,     
                "servings": 2
            },
            {
                "title": "Kale Smoothie",
                "description": "A simple kale smoothie.",
                "categoryid": categoryids[0],
                "authoruserid": userids[10],
                "ingredients": [
                    {"name": "Kale", "quantity": "2 cups"},
                    {"name": "Banana", "quantity": 1},
                    {"name": "Almond milk", "quantity": "1 cup"}
                ],
                "tags": ["kale", "smoothie"],
                "dietary_flags": ["kale-only"],
                "preptime": 5,
                "cooktime": 0,
                "servings": 1
            },
            {
                "title": "Fish and Chips",
                "description": "Classic British dish for those who follow Daria Morgendorffer's diet",
                "categoryid": categoryids[1],
                "authoruserid": userids[11],
                "ingredients": [
                    {"name": "Fish fillets", "quantity": "200g"},
                    {"name": "Potatoes", "quantity": "2"},
                    {"name": "Flour", "quantity": "1 cup"},
                    {"name": "Beer", "quantity": "1 cup"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Pepper", "quantity": "to taste"}
                ],
                "tags": ["fish-and-chips", "british"],
                "dietary_flags": ["fish-and-chips"],
                "preptime": 15,
                "cooktime": 20,
                "servings": 2
            },
            {
                "title": "Vegan Chocolate Cake",
                "description": "A delicious vegan chocolate cake for those who follow Jay Mewes' diet",
                "categoryid": categoryids[1],
                "authoruserid": userids[12],
                "ingredients": [
                    {"name": "Flour", "quantity": "1.5 cups"},
                    {"name": "Cocoa powder", "quantity": "0.5 cup"},
                    {"name": "Sugar", "quantity": "1 cup"},
                    {"name": "Baking soda", "quantity": "1 tsp"},
                    {"name": "Salt", "quantity": "0.5 tsp"},
                    {"name": "Water", "quantity": "1 cup"},
                    {"name": "Vegetable oil", "quantity": "0.5 cup"},
                    {"name": "Vanilla extract", "quantity": "1 tsp"}
                ],
                "tags": ["vegan", "dessert"],
                "dietary_flags": ["vegan"],
                "preptime": 20,
                "cooktime": 30,
                "servings": 8
            },
            {
                "title": "Pasta Primavera",
                "description": "A light pasta dish for those who follow Shaggy Rogers' diet",
                "categoryid": categoryids[1],
                "authoruserid": userids[13],
                "ingredients": [
                    {"name": "Pasta", "quantity": "200g"},
                    {"name": "Zucchini", "quantity": 1},
                    {"name": "Bell pepper", "quantity": 1},
                    {"name": "Cherry tomatoes", "quantity": "1 cup"},
                    {"name": "Olive oil", "quantity": "2 tbsp"},
                    {"name": "Garlic", "quantity": 2},
                    {"name": "Parmesan cheese", "quantity": "50g"}
                ],
                "tags": ["pasta", "vegetarian"],
                "dietary_flags": ["vegetarian"],
                "preptime": 15,
                "cooktime": 20,
                "servings": 2
            },
            {
                "title": "Steak and Eggs",
                "description": "A hearty meal for those who follow Chev Chelios' diet",
                "categoryid": categoryids[1],
                "authoruserid": userids[14],
                "ingredients": [
                    {"name": "Steak", "quantity": "300g"},
                    {"name": "Eggs", "quantity": 2},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Pepper", "quantity": "to taste"}
                ],
                "tags": ["steak", "eggs", "high-protein"],
                "dietary_flags": ["high-protein"],
                "preptime": 10,
                "cooktime": 15,
                "servings": 1
            },
            {
                "title": "Birria Tacos",
                "description": "Delicious birria tacos for those who follow John McClane's diet",
                "categoryid": categoryids[1],
                "authoruserid": userids[15],
                "ingredients": [
                    {"name": "Beef", "quantity": "300g"},
                    {"name": "Taco shells", "quantity": "4"},
                    {"name": "Onions", "quantity": 1},
                    {"name": "Garlic", "quantity": 2},
                    {"name": "Chili powder", "quantity": "1 tbsp"},
                    {"name": "Cumin", "quantity": "1 tsp"},
                    {"name": "Oregano", "quantity": "1 tsp"},
                    {"name": "Beef broth", "quantity": "2 cups"}
                ],
                "tags": ["birria", "tacos"],
                "dietary_flags": ["none"],
                "preptime": 20,
                "cooktime": 120,
                "servings": 4
            },
            {
                "title": "Chicken Teriyaki",
                "description": "A savory dish for those who follow Goku's diet",
                "categoryid": categoryids[1],
                "authoruserid": userids[16],
                "ingredients": [
                    {"name": "Chicken", "quantity": "300g"},
                    {"name": "Teriyaki sauce", "quantity": "2 tbsp"},
                    {"name": "Ginger", "quantity": "1 tsp"},
                    {"name": "Garlic", "quantity": 2},
                    {"name": "Soy sauce", "quantity": "1 tbsp"}
                ],
                "tags": ["chicken", "teriyaki"],
                "dietary_flags": ["none"],
                "preptime": 15,
                "cooktime": 20,
                "servings": 2
            },
            {
                "title": "Caesar Salad",
                "description": "A refreshing salad for those who follow Vegeta's diet",
                "categoryid": categoryids[0],
                "authoruserid": userids[17],
                "ingredients": [
                    {"name": "Romaine lettuce", "quantity": "1 head"},
                    {"name": "Croutons", "quantity": "1 cup"},
                    {"name": "Parmesan cheese", "quantity": "50g"},
                    {"name": "Caesar dressing", "quantity": "2 tbsp"}
                ],
                "tags": ["salad", "caesar"],
                "dietary_flags": ["vegetarian"],
                "preptime": 10,
                "cooktime": 0,
                "servings": 2
            }
            {
                "title": "Miso Soup",
                "description": "A comforting soup for those who follow Bulma's diet",
                "categoryid": categoryids[0],
                "authoruserid": userids[18],
                "ingredients": [
                    {"name": "Miso paste", "quantity": "2 tbsp"},
                    {"name": "Tofu", "quantity": "100g"},
                    {"name": "Green onions", "quantity": 2},
                    {"name": "Dashi broth", "quantity": "4 cups"}
                ],
                "tags": ["soup", "miso"],
                "dietary_flags": ["vegetarian"],
                "preptime": 10,
                "cooktime": 15,
                "servings": 4
            }
            {
                "title": "Spaghetti Carbonara",
                "description": "A classic Italian pasta dish for those who follow Piccolo's diet",
                "categoryid": categoryids[1],
                "authoruserid": userids[19],
                "ingredients": [
                    {"name": "Spaghetti", "quantity": "200g"},
                    {"name": "Pancetta", "quantity": "100g"},
                    {"name": "Eggs", "quantity": 2},
                    {"name": "Parmesan cheese", "quantity": "50g"},
                    {"name": "Black pepper", "quantity": "to taste"}
                ],
                "tags": ["pasta", "carbonara"],
                "dietary_flags": ["none"],
                "preptime": 15,
                "cooktime": 20,
                "servings": 2

            },
            { 
                "title": "Gabagool Sandwich",
                "description": "A delicious sandwich inspired by Italy.",
                "categoryid": categoryids[1],
                "authoruserid": userids[20],
                "ingredients": [
                    {"name": "Gabagool", "quantity": "100g"},
                    {"name": "Italian bread", "quantity": "1 loaf"},
                    {"name": "Provolone cheese", "quantity": "50g"},
                    {"name": "Lettuce", "quantity": "1 cup"},
                    {"name": "Tomato", "quantity": 1},
                    {"name": "Italian dressing", "quantity": "2 tbsp"}
                ],
                "tags": ["sandwich", "italian"],
                "dietary_flags": ["none"],
                "preptime": 10,
                "cooktime": 0,
                "servings": 2
            },
            {
                "title": "Cordon Bleu",
                "description": "A classic French dish.",
                "categoryid": categoryids[2],
                "authoruserid": userids[21],
                "ingredients": [
                    {"name": "Chicken breast", "quantity": "2 pieces"},
                    {"name": "Bacon", "quantity": "4 slices"},
                    {"name": "Swiss cheese", "quantity": "4 slices"},
                    {"name": "Breadcrumb", "quantity": "1 cup"}
                ],
                "tags": ["chicken", "cordon-bleu"],
                "dietary_flags": ["none"],
                "preptime": 15,
                "cooktime": 25,
                "servings": 2
            }
            {
                "title": "Four Cheese Mac and Cheese",
                "description": "A cheesy comfort food.",
                "categoryid": categoryids[3],
                "authoruserid": userids[22],
                "ingredients": [
                    {"name": "Macaroni", "quantity": "200g"},
                    {"name": "Cheddar cheese", "quantity": "100g"},
                    {"name": "Mozzarella cheese", "quantity": "100g"},
                    {"name": "Parmesan cheese", "quantity": "50g"},
                    {"name": "Milk", "quantity": "1 cup"}
                ],
                "tags": ["pasta", "cheese"],
                "dietary_flags": ["none"],
                "preptime": 10,
                "cooktime": 20,
                "servings": 4
            },
            {
                "title": "Buffalo Wings",
                "description": "Spicy chicken wings for game day.",
                "categoryid": categoryids[4],
                "authoruserid": userids[23],
                "ingredients": [
                    {"name": "Chicken wings", "quantity": "500g"},
                    {"name": "Buffalo sauce", "quantity": "1 cup"},
                    {"name": "Butter", "quantity": "2 tbsp"},
                    {"name": "Garlic powder", "quantity": "1 tsp"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Pepper", "quantity": "to taste"}
                ],
                "tags": ["chicken", "buffalo-wings"],
                "dietary_flags": ["none"],
                "preptime": 15,
                "cooktime": 25,
                "servings": 4
            },
            {
                "title": "Jalapeno Poppers",
                "description": "Spicy stuffed peppers.",
                "categoryid": categoryids[5],
                "authoruserid": userids[24],
                "ingredients": [
                    {"name": "Jalapeno peppers", "quantity": "10 pieces"},
                    {"name": "Cream cheese", "quantity": "100g"},
                    {"name": "Garlic", "quantity": "2 cloves"},
                    {"name": "Panko breadcrumbs", "quantity": "1 cup"},
                    {"name": "Parmesan cheese", "quantity": "50g"}
                ],
                "tags": ["appetizer", "spicy"],
                "dietary_flags": ["none"],
                "preptime": 20,
                "cooktime": 15,
                "servings": 4
            }
            {
                "title": "Chocolate Chip Cookies",
                "description": "Classic cookies for dessert.",
                "categoryid": categoryids[6],
                "authoruserid": userids[25],
                "ingredients": [
                    {"name": "Flour", "quantity": "2 cups"},
                    {"name": "Sugar", "quantity": "1 cup"},
                    {"name": "Butter", "quantity": "1 cup"},
                    {"name": "Eggs", "quantity": 2},
                    {"name": "Chocolate chips", "quantity": "1 cup"},
                    {"name": "Vanilla extract", "quantity": "1 tsp"},
                    {"name": "Baking soda", "quantity": "1 tsp"},
                    {"name": "Salt", "quantity": "0.5 tsp"}
                ],
                "tags": ["dessert", "cookies"],
                "dietary_flags": ["none"],
                "preptime": 15,
                "cooktime": 10,
                "servings": 24
            }
    ]).inserted_ids

    # ── REVIEWS ──
    reviews = db.reviews.insert_many([
        {
            "user_id":   users[0],
            "recipe_id": recipes[0],
            "rating":    5,
            "comment":   "Perfect level of spice.",
        },
    ]).inserted_ids

    # ── SAVED RECIPES ──
    saved = db.saved_recipes.insert_many([
        { "user_id": users[0], "recipe_id": recipes[0] },
    ]).inserted_ids

    # ── MEAL PLANS ──
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

    print("✓ Seed complete — 1 document per collection.")

if __name__ == "__main__":
    seed()
