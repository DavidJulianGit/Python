recipes_list = []
ingredients_list = []

# Define the take_recipe function
def take_recipe():
    name = input("Recipe name: ")
    cooking_time = int(input("Cooking time (min): "))
    ingredients = input("Ingredients, separated by comma ',': ").split(", ")  

    recipe = {
        'name': name, 
        'cooking_time': cooking_time, 
        'ingredients': ingredients
    }
    return recipe

# Main code
n = int(input("\nHow many recipes would you like to enter? "))

for i in range(n):
    print(f"\nEntering details for recipe #{i+1}")
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    num_ingredients = len(recipe['ingredients'])
    if recipe['cooking_time'] < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif recipe['cooking_time'] < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif recipe['cooking_time'] >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"
    
    print(f"\nRecipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print("Ingredients:")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print(f"Difficulty level: {difficulty}")
    
# Sort the ingredients list alphabetically
ingredients_list.sort()

print("\nIngredients Available Across All Recipes")
print("----------------------------------------")
for ingredient in ingredients_list:
    print(ingredient)
