import pickle

def display_recipe(recipe):
    print(f"Recipe: {recipe['name']}")
    print(f"Cooking Times (min): {recipe['cooking_time']}")
    print(f"Ingredients:")
    for index, ingredient in enumerate(recipe['ingredients'], start=1):
        print(f" {index}. {ingredient}")
    print(f"Difficulty: {recipe['difficulty']}\n")

def search_ingredient(data):
    all_ingredients = data['all_ingredients']
    for index, ingredient in enumerate(all_ingredients, start=1):
        print(f"{index} {ingredient}")
    
    try:
        ingredient_index = int(input("\nSearch for recipes including ingredient#: ")) -1
        ingredient_searched = all_ingredients[ingredient_index]
        print(f"Seraching for: {ingredient_searched}")
    
    except ValueError:
        print("Please enter the NUMBER of the ingredient!")
    
    except IndexError:
        print("Invalid ingredient number!")
    
    else:
        for recipe in data['recipes_list']:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)

# Open file and load data
filename = input("\nEnter the filename: ")

try:
    with open(filename, 'rb') as recipe_file:
        data = pickle.load(recipe_file)

except FileNotFoundError:
    print(f"File '{filename}' not found.")

else:
    recipe_file.close()
    search_ingredient(data)