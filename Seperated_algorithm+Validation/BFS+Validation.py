from collections import deque, defaultdict
import pandas as pd
import pickle

# Load dataset
df = pd.read_excel(r"C:\Users\Zhi Ling.DELL-ZLPG\OneDrive - 厦门大学(马来西亚分校) (1)\cleaned_recipe.xlsx", 
                   usecols = ["recipe_name", "ingredients"])

recipes = []

for index, row in df.iterrows():
    recipe = {"dish": row["recipe_name"], "ingredients": row["ingredients"].split(", ")}
    recipes.append(recipe)

uniqueIngredient = defaultdict(list)

for i, recipe in enumerate(recipes):
    for ingredient in recipe["ingredients"]:
        uniqueIngredient[ingredient].append(i)
        
with open("uniqueIngredient.pkl", "wb") as f:
    pickle.dump(uniqueIngredient, f)
    
with open("recipes.pkl", "wb") as f:
    pickle.dump(recipes, f)

with open("uniqueIngredient.pkl", "rb") as f:
    uniqueIngredient = pickle.load(f)
    
with open("recipes.pkl", "rb") as f:
     recipes = pickle.load(f)
     

# Example user input
userIngredients = "ice cream, whipping cream, flour"
userIngredients = userIngredients.split(", ")
userIngredientSet = set(userIngredients)

def bfsRecommendations(userIngredients, uniqueIngredient, recipes, maxRecommendations = 3):
    queue = deque(userIngredients)
    visitedRecipes = set()
    recommendations = []
    recommendationIngredients = []
    
    seenIngredients = set(userIngredients)
    
    while queue and len(recommendations) < maxRecommendations:
        ingredient = queue.popleft()
        
        for recipeIndex in uniqueIngredient[ingredient]:
            if recipeIndex not in visitedRecipes:
                visitedRecipes.add(recipeIndex)
                recommendations.append(recipes[recipeIndex]["dish"])
                recommendationIngredients.append(recipes[recipeIndex]["ingredients"])

                if len(recommendations) >= maxRecommendations:
                    break

        for neighbourIngredient in uniqueIngredient[ingredient]:
            if neighbourIngredient not in seenIngredients:
                seenIngredients.add(neighbourIngredient)
                queue.append(neighbourIngredient)
                
    return recommendations, recommendationIngredients


recommendedRecipes, recommendedIngredients = bfsRecommendations(userIngredients, uniqueIngredient, recipes)

def findMissingIngredients(userIngredients, recommendations, recipes):
    print("Recommended Recipes: ")
                
    for dish in recommendations:
        for recipe in recipes:
            if dish == recipe["dish"]:
                recipeIngredientSet = set(recipe["ingredients"])
                missingIngredientList = list(recipeIngredientSet - userIngredientSet)
                missingIngredients = ", ".join(missingIngredientList)
                
                if not missingIngredientList:
                    print(dish)
                    print("You have all ingredients needed!")
                            
                else:
                    print(dish)
                    print("Missing Ingredients: ", missingIngredients)
                    print("\n")

missingIngredient = findMissingIngredients(userIngredients, recommendedRecipes, recipes)


# Validation
import numpy as np

def calculateAccuracy(userInput, systemRecommendation, allIngredients):
    userSet = set(userInput)
    recommendationSet = set(systemRecommendation)
    allIngredientSet = set(allIngredients)
    
    # Correctly recommended ingredients
    TP = userSet.intersection(recommendationSet)
    
    # Ingredients recommended but not in user's list
    FP = recommendationSet.difference(userSet)
    
    # Ingredients in user's list but not recommended
    FN = userSet.difference(recommendationSet)
    
    if (len(TP) + len(FP) + len(FN)) > 0:
        accuracy = (len(TP)) / (len(TP) + len(FP) + len(FN))  
    else:
        accuracy = 0
    
    
    return accuracy

def calculatePrecision(userInput, systemRecommendation):
    userSet = set(userInput)
    recommendationSet = set(systemRecommendation)
    
    TP = userSet.intersection(recommendationSet)
    
    FP = recommendationSet.difference(userSet)
    
    if (len(TP) + len(FP)) > 0:
        precision = len(TP) / (len(TP) + len(FP))  
    else:
        precision = 0
    
    
    return precision

def calculateRecall(userInput, systemRecommendation):
    userSet = set(userInput)
    recommendationSet = set(systemRecommendation)
    
    TP = userSet.intersection(recommendationSet)
    
    FN = userSet.difference(recommendationSet)

    if (len(TP) + len(FN)) > 0:
        recall = len(TP) / (len(TP) + len(FN))
    else:
        recall = 0
    
    return recall

accuracyScore = []
precisionScore = []
recallScore = []

for recommendedIngredient in recommendedIngredients:
    accuracy = calculateAccuracy(userIngredients, recommendedIngredient, uniqueIngredient)
    precision = calculatePrecision(userIngredients, recommendedIngredient)
    recall = calculateRecall(userIngredients, recommendedIngredient)
    accuracyScore.append(accuracy)
    precisionScore.append(precision)
    recallScore.append(recall)

meanAccuracy = np.mean(accuracyScore)
meanPrecision = np.mean(precisionScore)
meanRecall = np.mean(recallScore)

print(f"Accuracy: {meanAccuracy:.2f}")
print(f"Precision: {meanPrecision:.2f}")
print(f"Recall: {meanRecall:.2f}")