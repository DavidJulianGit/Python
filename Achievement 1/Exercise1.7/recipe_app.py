# 1.3
import textwrap
import string 
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from functools import partial

# Constants
TABLE_NAME = "final_recipes"

# 1.4 Create Engine object
engine = create_engine("mysql://cf-python:password@localhost/task_database")

# 1.5 Create Session object
Session = sessionmaker(bind=engine)
session = Session()

# 2
# 2.1 
Base = declarative_base()
class Recipe(Base):
    # 2.2
    __tablename__ = TABLE_NAME

    # 2.3
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Constructor method
    def __init__(self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.calculate_difficulty()
        
    # 2.4
    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + ">"

    # 2.5
    def __str__(self):
        ingredients_list = self.return_ingredients_as_list()
        ingredients_str = ""

        for index, ingredient in enumerate(ingredients_list, start=1):
            ingredients_str += f" \t  {index}. {ingredient}\n"

        output = (
            f"Recipe: {self.name} \n"
            "------------------------------------------\n"
            f"\tCooking Time (min): {self.cooking_time} \n"
            f"\tIngredients:\n{ingredients_str}"
            f"\tDifficulty: {self.difficulty}\n"
            "------------------------------------------\n"
        )

        return output
    
    # 2.6
    def calculate_difficulty(self):
        cooking_time = int(self.cooking_time)
        num_ingredients = len(self.return_ingredients_as_list())
       
        if cooking_time < 10 and num_ingredients < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and num_ingredients >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and num_ingredients < 4:
            difficulty = "Intermediate"
        else:
            difficulty = "Hard" 
        
        self.difficulty = difficulty

    # 2.7
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        else:
            return self.ingredients.split(', ')

# 2.8
Base.metadata.create_all(engine)

# Helper functions for getting validated user input
def get_valid_input(prompt, validation_func):
    while True:
        try:
            user_input = input(prompt).strip()
            return validation_func(user_input)
        except ValueError as e:
            print(e)

def validate_name(name_input):
    name = string.capwords(name_input)
    if not name:
        raise ValueError("Recipe name must not be empty.")

    elif len(name) > 50:
        raise ValueError("Name must be shorter than 50 characters.")

    return name

def validate_num_ingredients(ingredients_input):
    if not ingredients_input.isdigit():
        raise ValueError("Enter a positive integer for the number of ingredients.")

    elif int(ingredients_input) < 1 or int(ingredients_input) > 20:
        raise ValueError("Enter a valid number of ingredients (1 - 20).")

    else:
        return int(ingredients_input)

def validate_ingredient(ingredient_input):
    ingredient = string.capwords(ingredient_input)

    if len(ingredient) <= 0:
        raise ValueError("Ingredient must not be empty.")
    return ingredient
    
def validate_cooking_time(cooking_time_input):
    if not cooking_time_input.isdigit() or int(cooking_time_input) <= 0:
        raise ValueError("Cooking time must be a positive integer.")
    return cooking_time_input

def validate_search_ingredient(search_ingredients_numbers, all_ingredients):
    if not search_ingredients_numbers:
        raise ValueError("Enter the numbers of all the ingredients you want to search for, seperated by spaces!")
    
    search_ingredients_list = search_ingredients_numbers.split(" ")

    for index, ingredient in enumerate(search_ingredients_list,start=1):
        # 3.3.7
        if not ingredient.isdigit():
            raise ValueError(f"Enter the number of an ingredient. (1 - {len(all_ingredients)})")

        elif int(ingredient) < 1 or int(ingredient) > len(all_ingredients):
            raise ValueError(f"Ingredient #{index} that you entered '{ingredient}' does not correspond to an ingredient listed above. (1 - {len(all_ingredients)})")

    return search_ingredients_list

def validate_recipe_to_edit_id(recipe_to_edit_id):
    if not recipe_to_edit_id.isdigit():
        raise ValueError("Enter the number of the recipe you want to edit.")

    elif int(recipe_to_edit_id) < 1:
        raise ValueError("Enter an integer bigger than 0.")

    else:
        return int(recipe_to_edit_id)

def validate_attribute_to_edit(attribute_to_edit_input):
    if not attribute_to_edit_input.isdigit() or int(attribute_to_edit_input) < 1 or int(attribute_to_edit_input) > 3:
        raise ValueError("Enter the number of the attribute you want to edit. (1-3)")
    return attribute_to_edit_input

def validate_recipe_to_edit_number(recipe_to_edit_number_input, results):
    if not recipe_to_edit_number_input.isdigit():
        raise ValueError("Enter a positive integer.")
                    
    elif int(recipe_to_edit_number_input) < 1 or int(recipe_to_edit_number_input) > len(results):
        raise ValueError(f"Enter a number between 1 and {len(results)}.")
    return recipe_to_edit_number_input

def get_validated_ingredients_str():
    ingredients = []
    while True:
        try: 
            num_ingredients = get_valid_input("\nHow many ingredients do you want to enter: ", validate_num_ingredients)
            
            for index in range(num_ingredients):
                ingredient = get_valid_input(f"Ingredient #{index+1}: ", validate_ingredient)
                if ingredient not in ingredients:
                    ingredients.append(ingredient)
            
            # 3.1.4 Convert ingredients into string
            ingredients_str = ", ".join(ingredients)
            if len(ingredients_str) > 255:
                raise ValueError("You entered too many characters for your ingredients. (max. 255)")
            break
        except ValueError as e:
            print(e)
    
    return ingredients_str

def is_table_recipe_empty():
    try:
        # 3.5.1 Check if table is empty
        if not session.query(Recipe).count():
            print("Sorry, you don't have any recipes to delete yet. Why not create your first one?")
            return True
        return False
    except Exception as e:
        print(e)

# 3
# 3.1
def create_recipe():    
    # 3.1.1 Getting user inputs 
    name = get_valid_input("Recipe name: ", validate_name)

    # 3.1.3 Get ingredients
    ingredients_str = get_validated_ingredients_str()
    

    # Get cooking time
    cooking_time = get_valid_input("Cooking time (min): ", validate_cooking_time)
    
    try:
        # 3.1.5 Create Recipe object
        recipe_entry = Recipe(name, ingredients_str, cooking_time)
       
        # 3.1.7 add & commit
        session.add(recipe_entry)
        session.commit()
        print(f"Recipe for '{name}' has been succesfully created.")
        print(recipe_entry) 

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# 3.2
def view_all_recipes():

    try:
        all_recipes = session.query(Recipe).all()
        
        if not all_recipes:
            print("No recipes found.")
            return 
        
        for index, recipe in enumerate(all_recipes, start=1):
            print(f"#{index} ")
            print(recipe)

    except Exception as e:
        print(f"Sorry, an unexpected error occurred: {e}")

# 3.3 
def search_by_ingredients():
    # 3.3.3
    all_ingredients = []
    search_ingredients = []
    try:
        # 3.3.1 Check if table is empty
        if not session.query(Recipe).count():
            print("Sorry, you don't have any recipes to search through yet. Why not create your first one?")
            return

        # 3.3.2
        results = session.query(Recipe).with_entities(Recipe.ingredients).all()

        # 3.3.4
        for ingredients in results:
            ingredients_list = ingredients[0].split(', ')
            for ingredient in ingredients_list:
                if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)
        
        # 3.3.5
        print("\n" + "-"*5 + f" These are all available ingredients ({len(all_ingredients)}) " + "-"*5)
        for index, ingredient in enumerate(all_ingredients, start=1):
            print(f"{index} {ingredient}")

      
        # 3.3.6
        # getting all_ingredients into validate_search_ingredient
        validate_search_ingredient_partial = partial(validate_search_ingredient, all_ingredients=all_ingredients)
        search_ingredients_list = get_valid_input("\nEnter the numbers of all ingredients you want to search for, separated by spaces: ", validate_search_ingredient_partial)         

        # 3.3.8
        for ingredient in search_ingredients_list:
            search_ingredients.append(all_ingredients[int(ingredient)-1])        
           

        ingredients_str = ", ".join(search_ingredients)
        print(f"\nYour search results for '{ingredients_str}':")
        print("..........................................................")
        conditions = []
        
        for ingredient in search_ingredients:
            like_term = Recipe.ingredients.like("%"+ingredient+"%")
            conditions.append(like_term)
        
        filtered_recipes = session.query(Recipe).filter(*conditions)
        for recipe in filtered_recipes:
            print(recipe) 

    except ValueError as e:
        print(f"{e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# 3.4
def edit_recipe():
    try:
         # 3.4.1 Check if table is empty
        if is_table_recipe_empty():
            return

        # 3.4.2 Get name and Id of all recipes
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
        
        # 3.4.3 Display id and name to the user
        print("\nWhich of the following recipes do you want to edit?")
        for index, recipe in enumerate(results, start=1):
            print(f"\t{index} {recipe[1]}")

        # 3.4.4 Let user pick Id
        validate_recipe_to_edit_number_partial = partial(validate_recipe_to_edit_number, results=results)
        recipe_to_edit_number = get_valid_input("\nNumber of the recipe you want to edit: ", validate_recipe_to_edit_number_partial)         
               
        # 3.4.5 Retrieve recipe to delete from DB
        recipe_to_edit_id = results[int(recipe_to_edit_number)-1][0]
        recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_to_edit_id).all()[0]
    

        # 3.4.6
        output = (
                    f" 1 Recipe: {recipe_to_edit.name} \n"
                    f" 2 Cooking Time (min): {recipe_to_edit.cooking_time} \n"
                    f" 3 Ingredients:{recipe_to_edit.ingredients}"
        )
        print(output)

        # 3.4.7
        attribute_to_edit_input = int(get_valid_input("\nNumber of the attribute you want to edit: ", validate_attribute_to_edit))
        
        # 3.4.8
        if attribute_to_edit_input == 1:
            new_attribute_value = get_valid_input("\nEnter the new name: ", validate_name)       
            recipe_to_edit.name = new_attribute_value

        elif attribute_to_edit_input == 2:
            new_attribute_value = get_valid_input("\nEnter the new cooking time in minutes: ", validate_cooking_time)  
            recipe_to_edit.cooking_time = new_attribute_value
            recipe_to_edit.calculate_difficulty()

        elif attribute_to_edit_input == 3:
            new_attribute_value = get_validated_ingredients_str()
            recipe_to_edit.ingredients = new_attribute_value
            recipe_to_edit.calculate_difficulty()

        else:
            raise ValueError("Enter an integer between 1 and 3.")
        
        # 3.4.8
        session.commit()
        print(f"\n -> Recipe for '{recipe_to_edit.name}' successfully updated.\n")
        print(recipe_to_edit)

    except ValueError as e:
        print(f"{e}")
    except Exception as e:
        print(f"Unexpected error: {e}")   

# 3.5
def delete_recipe():
    try:
        # 3.5.1 Check if table is empty
        if is_table_recipe_empty():
            return

        # 3.5.2
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
        
        print("\nWhich of the following recipes do you want to delete?")
        for index, recipe in enumerate(results, start=1):
            print(f"\t{index} {recipe[1]}")

        # 3.5.3
        while True:
            try:
                recipe_to_delete_number_input = input("\nEnter the number of the recipe you want to delete: ").strip()
                
                if not recipe_to_delete_number_input.isdigit():
                    raise ValueError("Enter a positive integer.")
                    
                elif int(recipe_to_delete_number_input) < 1 or int(recipe_to_delete_number_input) > len(results):
                    raise ValueError(f"Enter a number between 1 and {len(results)}.")
            
                break
            except ValueError as e:
                print(f"Input Error: {e}")

        # 3.5.2 Retrieve recipe to delete from DB
        recipe_to_delete_id = results[int(recipe_to_delete_number_input)-1][0]
        recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_to_delete_id).all()[0]

        really_delete_input = input(f"Enter 'yes' if you really want to delete the recipe for '{recipe_to_delete.name}': ").strip().lower()

        if really_delete_input == 'yes':
            session.delete(recipe_to_delete)
            session.commit()
            print(f"Recipe for '{recipe_to_delete.name}' has been deleted.")
        else:
            print("Recipe not deleted.")
            return

    except ValueError as e:
        print(f"{e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# 4 Main Menu
def main_menu():
    choice = 0

    while choice != 'quit':
        print(textwrap.dedent("""\n\
        =================================================================
                                  Main Menu                                                                                                        
        =================================================================
        Pick a choice
            1. Create a new recipe
            2. View all recipes
            3. Search for a recipe by ingredients
            4. Edit an existing recipe
            5. Delete a recipe

            Type 'quit' to exit the program.
    """))
                
        choice = input("Your choice: ").strip()

        try:
            if choice == '1':
                create_recipe()
            elif choice == '2':
                view_all_recipes()
            elif choice == '3':
                search_by_ingredients()
            elif choice == '4':
                edit_recipe()
            elif choice == '5':
                delete_recipe()
            elif choice == 'quit':
                engine.close()
                session.close()
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

main_menu()