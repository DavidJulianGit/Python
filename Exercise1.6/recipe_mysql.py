import textwrap
import string

# Constants
TABLE_NAME = "Recipes"
COLUMN_ID = "id"
COLUMN_NAME = "name"
COLUMN_INGREDIENTS = "ingredients"
COLUMN_COOKING_TIME = "cooking_time"
COLUMN_DIFFICULTY = "difficulty"

# 1.1 import connector module
import mysql.connector

# 1.2 initialize connection object
conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)

# 1.3 initialize cursor object
cursor = conn.cursor()

# 1.4 create DB
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

# 1.5 access DB
cursor.execute("USE task_database")

# 1.6 create table "Recipes"
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {COLUMN_ID} INT PRIMARY KEY AUTO_INCREMENT,
        {COLUMN_NAME} VARCHAR(50),
        {COLUMN_INGREDIENTS} VARCHAR(255),
        {COLUMN_COOKING_TIME} INT,
        {COLUMN_DIFFICULTY} VARCHAR(20),
        CHECK({COLUMN_DIFFICULTY} IN ('Easy', 'Medium', 'Intermediate', 'Hard'))
""")

# print a recipe
def print_recipe_from_tuple(recipe_tuple):
    Id, name, ingredients, cooking_time, difficulty = recipe_tuple

    ingredients_str = ""
    for index, ingredient in enumerate(ingredients.split(", "), start=1):
        ingredients_str += f" {index}. {ingredient}\n"

    output = (
        f"Name: {name} \n"
        f"Ingredients:\n{ingredients_str}"
        f"Cooking Time (min): {cooking_time}\n"
        f"Difficulty: {difficulty}\n"
    )
    print(output)

# print all recipes
def print_all_recipes(conn, cursor):
    sql = f"SELECT * FROM {TABLE_NAME};"
    cursor.execute(sql) 
    result = cursor.fetchall()
    print("\nAll recipes:\n------------------------------------------")

    for index, recipe_tuple in enumerate(result, start=1):
        print("-"*5 + f" Recipe #{index} " + "-"*5)
        print_recipe_from_tuple(recipe_tuple)

    print("------------------------------------------")

# 3.1 Create a new recipe 
def create_recipe(conn, cursor):
    try:
        # Getting user inputs 
        name = input("Recipe name: ").strip().capitalize()
        if not name:
            raise ValueError("Recipe name must not be empty.")

        cooking_time_input = input("Cooking time (min): ").strip()
        if not cooking_time_input.isdigit() or int(cooking_time_input) <= 0  :
            raise ValueError("Cooking time must be a positive integer.")
        
        cooking_time = int(cooking_time_input)

        ingredients_input = input("Ingredients, separated by comma ',': ").strip()
        if not ingredients_input:
            raise ValueError("Ingredients list cannot be empty.")

        # Split, capitalize, and join ingredients_input again
        ingredients = ", ".join([string.capwords(ingredient.strip()) for ingredient in ingredients_input.split(",")])
        
        difficulty = calc_difficulty(cooking_time, ingredients)
            
        # 3.3 & 3.4 SQL String and its execution to insert recipe into the db table
        sql = f"INSERT INTO {TABLE_NAME} ({COLUMN_NAME}, {COLUMN_INGREDIENTS}, {COLUMN_COOKING_TIME}, {COLUMN_DIFFICULTY}) VALUES (%s, %s, %s, %s);"
        values = (name, ingredients, cooking_time, difficulty)
    
        cursor.execute(sql, values)
        conn.commit()
        print(f"Recipe '{name}' succesfully created.")

    except ValueError as e:
        print(f"Invalid input: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# 3.2 Calculateg a recipes difficulty
def calc_difficulty(cooking_time, ingredients):
    # Split the ingredients by comma and count them
    num_ingredients = len(ingredients.split(','))
    
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard" 

    return difficulty

# 4 Search for a recipe 
def search_recipe(conn, cursor):
    all_ingredients = []
    
    # 4.1 SELECTing the ingredients column and saving the data in "results"
    sql = f"SELECT {COLUMN_INGREDIENTS} FROM {TABLE_NAME};"
    
    try:
        cursor.execute(sql) 
        result = cursor.fetchall()
    except Exception as e:
        print(f"Error loading 'ingredients' from database: {e}")   
        return

    # 4.2 Storing all ingredients in all_ingredients without duplicates
    
    # tuple format: ('Tea Leaves, Water, Sugar',)
    for tuple_rows in result:
        ingredients = tuple_rows[0].split(", ")
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    
    all_ingredients.sort()

    # 4.3 Display all ingredients, Store ingredient to be searched for in "search_ingredient"
    print("\nAll ingredients:")
    for index, ingredient in enumerate(all_ingredients, start=1):
        print(f" {index}. {ingredient}")

    # Getting search ingredient
    try:
        ingredient_num = int(input("\nNumber of the ingredient you want to search for: "))
        
        if ingredient_num < 1 or ingredient_num > len(all_ingredients):
            raise IndexError
        
        search_ingredient = all_ingredients[ingredient_num-1]
        print(f"\nAll recipes including '{search_ingredient}'")
        print(f"-"*len(f"All recipes including '{search_ingredient}'"))

    except ValueError:
        print("Please enter a positive integer.")
        return
    except IndexError:
        print(f"Please enter the number of an ingredient. (1 - {len(all_ingredients)})")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")   



    # 4.4 Searching for rows in Recipe table that contain search_ingredient
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {COLUMN_INGREDIENTS} LIKE %s;"
    
    try:
        cursor.execute(sql, ('%' + search_ingredient + '%',))
        result = cursor.fetchall()
    except Exception as e:
        print(f"Unexpected error occurred: {e}.")
        return#

    for recipe in result:
        print_recipe_from_tuple(recipe)

# 5 Update a recipe 
def update_recipe(conn, cursor):
    update_sql = ""
    update_values = ()
    
    # Get all recipes
    sql = f"SELECT * FROM {TABLE_NAME};"
    cursor.execute(sql)
    result = cursor.fetchall()

    # Print all recipes
    print("\nWhich recipe do you want to update?\n--------------------------")

    for index, recipe_tuple in enumerate(result, start=1):
        print(f"#{index}")
        print_recipe_from_tuple(recipe_tuple)
   
    # Get index of the recipe 
    try:
        index_to_update = int(input("Enter number of the recipe you want to update: ")) - 1
        if index_to_update < 1 or index_to_update > len(result):
            raise IndexError("No recipe found with that number. Please enter a number from the list above.")

        recipe_to_update = result[index_to_update]

    except ValueError:
        print("Invalid input. Please enter a valid number corresponding to the recipe.")
        return

    except IndexError as e:
        print(e)
        return

    
    print(f"Recipe to update: {recipe_to_update[1]}")

    # Get column to update 
    print("\nCategories that can be updated:")
    print(" 1 Name")
    print(" 2 Ingredients")
    print(" 3 Cooking Time")

    try:
        new_name = ""
        column_to_update = int(input("\nPlease enter the number of the category you want to update: ").strip())

        # Update name
        if column_to_update == 1:
            new_name = string.capwords(str(input("Please enter the updated name: ")).strip())

            if not new_name:
                raise ValueError("Name cannot be empty.")

            update_sql = f"UPDATE {TABLE_NAME} SET {COLUMN_NAME} = %s WHERE {COLUMN_ID} = %s;"
            update_values = (new_name, recipe_to_update[0])

        # Update ingredients
        elif column_to_update == 2:
            new_ingredients_input = input("Please enter the updated ingredients. Seperate them by ', ': ").strip()

            if not new_ingredients_input:
                raise ValueError("Ingredients cannot be empty.")

            new_ingredients = ", ".join([string.capwords(ingredient.strip()) for ingredient in new_ingredients_input.split(",")])
            new_difficulty = calc_difficulty(recipe_to_update[3], new_ingredients)
            
            update_sql = f"UPDATE {TABLE_NAME} SET {COLUMN_INGREDIENTS} = %s, {COLUMN_DIFFICULTY} = %s WHERE {COLUMN_ID} = %s;"
            update_values = (new_ingredients, new_difficulty, recipe_to_update[0])

        # Update cooking_time
        elif column_to_update == 3:
            new_cooking_time_input = input("Please enter the updated cooking time in minutes: ")

            if not new_cooking_time_input.isdigit() or int(new_cooking_time_input) <= 0:
                raise ValueError("Cooking time must be a positive integer.")
            
            new_cooking_time = int(new_cooking_time_input)
            new_difficulty = calc_difficulty(new_cooking_time, recipe_to_update[2])
            
            update_sql = f"UPDATE {TABLE_NAME} SET {COLUMN_COOKING_TIME} = %s, {COLUMN_DIFFICULTY} = %s WHERE {COLUMN_ID} = %s;"
            update_values = (new_cooking_time, new_difficulty, recipe_to_update[0])

        else:
            print("Please enter a valid number (1, 2 or 3).")  
            return   
    
    except ValueError as e:
        print(f"Input error: {e}")
        return

    except Exception as e:
        print(f"An unexpected error occurred: {e}.")
        return

    try:
        cursor.execute(update_sql, update_values)
        conn.commit()
        print("Recipe updated successfully!")

    except Exception as e:
        print(f"Database error occurred: {e}.")
            
# 6 Delete a recipe 
def delete_recipe(conn, cursor):
    sql = f"SELECT * FROM {TABLE_NAME};"
    cursor.execute(sql)
    result = cursor.fetchall()

    # Print all recipes
    print("\nWhich recipe do you want to delete?\n--------------------------")

    for index, recipe_tuple in enumerate(result, start=1):
        print(f"#{index}")
        print_recipe_from_tuple(recipe_tuple)
   
    
    # Get index of the recipe 
    try:
        index_to_delete = int(input("Enter number of the recipe you want to delete: ")) 
        if index_to_delete < 1 or index_to_delete > len(result):
            raise IndexError("No recipe found with that number. Please enter a number from the list above.")

        recipe_to_delete = result[index_to_delete]

    except ValueError:
        print("Invalid input. Please enter a valid number corresponding to the recipe.")
        return

    except IndexError as e:
        print(e)
        return

    sql = f"DELETE FROM {TABLE_NAME} WHERE {COLUMN_ID} = %s;"
    
    try:
        cursor.execute(sql, (index_to_delete,))
        conn.commit()

        # check if the row was deleted from the table 
        if cursor.rowcount > 0:
            print(f"Recipe with Id {index_to_delete} was successfully deleted.")
        else:
            print(f"No recipe found with Id '{index_to_delete}'.")

    except ValueError:
        print("Invalid input. Please enter a valid integer for the 'Id'.")

    except Exception as e:
        print(f"Unexpected error occurred: {e}.")

# 2 Main menu
def main_menu(conn, cursor):
    choice = 0

    while choice != 'quit':
        print(textwrap.dedent("""\n\
        Main Menu
        ==========================================
        Pick a choice:
            1. Create a new recipe
            2. Search for a recipe by ingredient
            3. Update an existing recipe
            4. Delete a recipe
            5. Show all recipes
            Type 'quit' to exit the program.
    """))
                
        choice = input("Your choice: ").strip()

        try:
            if choice == '1':
                create_recipe(conn, cursor)
            elif choice == '2':
                search_recipe(conn, cursor)
            elif choice == '3':
                update_recipe(conn, cursor)
            elif choice == '4':
                delete_recipe(conn, cursor)
            elif choice == '5':
                print_all_recipes(conn, cursor)
            elif choice == 'quit':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
    conn.commit()
    conn.close()

# Start the program
main_menu(conn, cursor)

