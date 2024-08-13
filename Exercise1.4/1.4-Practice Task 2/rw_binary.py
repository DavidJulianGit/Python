import pickle

recipe = {
   'name':'Tea',
   'ingredients': ['Tea leaves','Water','Sugar'],
   'cooking_time': 5,
   'difficulty': 'Easy'}

with open('recipe_binary.bin','wb') as my_file:
   pickle.dump(recipe, my_file)


with open('recipe_binary.bin','rb') as my_file:
   loaded_recipe = pickle.load(my_file)

print("\nRecipe details")
print("________________")
print("\nName:  " + loaded_recipe['name'])
print("Ingredients:" )
for ingredient in loaded_recipe['ingredients']:
    print(ingredient )
print("Cooking time (min):  " + str(loaded_recipe['cooking_time']))
print("Difficulty: " + loaded_recipe['difficulty'] + "\n")