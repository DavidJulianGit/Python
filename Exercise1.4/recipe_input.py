import pickle

# Functions
def take_recipe():
    name = input("Recipe name: ")
    cooking_time = int(input("Cooking time (min): "))
    ingredients = input("Ingredients, separated by comma ',': ").split(", ")
    
    difficulty = calc_difficulty(cooking_time, len(ingredients))

    recipe = {
        'name': name, 
        'cooking_time': cooking_time, 
        'ingredients': ingredients,
        'difficulty': difficulty
    }

    return recipe


def calc_difficulty( cooking_time, num_ingredients):
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard" 

    return difficulty


# Open file and load data 
filename = input("Enter the filename: ")
try:
    with open(filename, 'rb') as recipes_file:
        data = pickle.load(recipes_file)
        
except FileNotFoundError:
    print("File not found. Creating a new data structure.")
    data = {'recipes_list': [], 'all_ingredients': []}

except:
    print("Unexpected error occurred. Creating a new data structure.")
    data = {'recipes_list': [], 'all_ingredients': []}

else:
    recipes_file.close()

finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

# get new recipes
recipe_count = int(input("\nHow many recipes would you like to enter? "))

for i in range(1, recipe_count+1):
    print(f"\nEntering details for recipe #{i}")

    recipe = take_recipe()
    recipes_list.append(recipe)

    for ingredient in recipe['ingredients']:
        if ingredient not in  all_ingredients:
             all_ingredients.append(ingredient)

# write data to file  
data['recipes_list'] = recipes_list
data['all_ingredients'] =  sorted(all_ingredients)

with open(filename, 'wb') as recipes_file:
    pickle.dump(data, recipes_file)