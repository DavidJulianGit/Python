class Recipe:
    
    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.cooking_time = 0
        self.ingredients = []
        self.difficulty = ""
       
    def calc_difficulty(self):
        cooking_time = int(self.cooking_time)
        num_ingredients = len(self.ingredients)
        
        if cooking_time < 10 and num_ingredients < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and num_ingredients >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and num_ingredients < 4:
            difficulty = "Intermediate"
        else:
            difficulty = "Hard" 
 
        self.difficulty = difficulty
    
    def set_name(self, name):
        self.name = name
    
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
    
    def get_name(self):
        return self.name
    
    def get_cooking_time(self):
        return self.cooking_time

    def get_ingredients(self):
        return self.ingredients
    
    def get_difficulty(self):
        if self.difficulty == "":
            self.calc_difficulty()

        return self.difficulty

    def add_ingredients(self, *ingredients):    
        for ingredient in ingredients:
            if ingredient not in self.ingredients:
                self.ingredients.append(ingredient)
        self.update_all_ingredients()

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
    
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)
    
    def __str__(self):
        ingredients_str = ""

        for index, ingredient in enumerate(self.ingredients, start=1):
            ingredients_str += f" {index}. {ingredient}\n"

        output = (
            f"Recipe: {self.name} \n"
            f"Cooking Time (min): {self.cooking_time} \n"
            f"Ingredients:\n{ingredients_str}"
            f"Difficulty: {self.get_difficulty()}\n"
        )

        return output

def recipe_search(data, search_term):
    print(f"Recipes containing '{search_term}': \n-----------------------------------")
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe) 

# Main
# Instanciate, fill and print the "Tea Recipe"
tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)
print(tea)

# Instanciate and fill the "Coffee Recipe"
coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)


# Instanciate and fill the "Cake Recipe"
cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)


# Instanciate and fill the "Banana Smoothie Recipe"
banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)


recipes_list = [tea, coffee, cake, banana_smoothie]

# Recipe Searches
recipe_search(recipes_list, "Water")
recipe_search(recipes_list, "Sugar")
recipe_search(recipes_list, "Bananas")