import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# Load dataset
file_path = r"C:\Users\Zhi Ling.DELL-ZLPG\OneDrive - 厦门大学(马来西亚分校) (1)\cleaned_recipe.xlsx"
df = pd.read_excel(file_path)

data_dict = df.to_dict(orient='records')

ingredient = [recipe['ingredients'] for recipe in data_dict]
recipe_name = [recipe['recipe_name'] for recipe in data_dict]

vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split(', '), token_pattern=None)
X = vectorizer.fit_transform(ingredient)
y = recipe_name


# Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = MultinomialNB()
model.fit(X_train, y_train)

def recommend_dish(ingredients, top=3):
    ingredients_list = ingredients.split(',')
    unique_ingredients = set(ingredients_list)
    ingredients_str = ', '.join(unique_ingredients)
    ingredients_str = ingredients_str.lower()

    # Vectorize the input ingredients
    input_vector = vectorizer.transform([ingredients_str])
    # Predict the probabilities
    probabilities = model.predict_proba(input_vector)[0]
    # Get indices of top N predictions
    top_indices = probabilities.argsort()[-top:][::-1]

    top_dishes = []
    for index in top_indices:
        dish_name = model.classes_[index]
        top_dishes.append(dish_name)
    return top_dishes


def find_missing_ingredients(user_ingredients, recipe_ingredients): 
    user_ingredients_set = set(user_ingredients)
    recipe_ingredients_set = set(recipe_ingredients.split(', '))
    missing_ingredients = recipe_ingredients_set - user_ingredients_set

    return missing_ingredients


# Example user input
user_ingredients = 'ice cream, whipping cream, flour'
recommended_dishes = recommend_dish(user_ingredients)

for dish in recommended_dishes:
    filtered_df = df[df['recipe_name'] == dish]
    recipe_ingredients = filtered_df['ingredients'].values[0]
    missing_ingredients = find_missing_ingredients(user_ingredients.split(','), recipe_ingredients)

    print(f"Recommended Dish: {dish}")
    if not missing_ingredients:
        print("You have all the ingredients needed!")
        print()
        
    else:
        print(f"Missing ingredients:\n{', '.join(missing_ingredients)}")
        print()


#Validation
def calculate_accuracy(user_input, recommended_ingredients):
    user_set = set(user_input)
    recommendation_set = set(recommended_ingredients)
    
    # Correctly recommended ingredients
    TP = user_set.intersection(recommendation_set)
    
    # Ingredients recommended but not in user's list
    FP = recommendation_set.difference(user_set)
    
    # Ingredients in user's list but not recommended
    FN = user_set.difference(recommendation_set)
    
    if (len(TP) + len(FP) + len(FN)) > 0:
        accuracy = len(TP) / (len(TP) + len(FP) + len(FN))

    else:
        accuracy = 0
    
    return accuracy

def calculate_precision(user_input, recommended_ingredients):
    user_set = set(user_input)
    recommendation_set = set(recommended_ingredients)
    
    TP = user_set.intersection(recommendation_set)
    
    FP = recommendation_set.difference(user_set)
    
    if (len(TP) + len(FP)) > 0:
        precision = len(TP) / (len(TP) + len(FP))

    else:
        precision = 0
    
    return precision

def calculate_recall(user_input, recommended_ingredients):
    user_set = set(user_input)
    recommendation_set = set(recommended_ingredients)
    
    TP = user_set.intersection(recommendation_set)
    
    FN = user_set.difference(recommendation_set)
    
    if (len(TP) + len(FN)) > 0:
        recall = len(TP) / (len(TP) + len(FN))

    else:
        recall = 0
    
    return recall

accuracy_scores = []
precision_scores = []
recall_scores = []

for dish in recommended_dishes:
    filtered_df = df[df['recipe_name'] == dish]
    recipe_ingredients = filtered_df['ingredients'].values[0]
    recommended_ingredients = recipe_ingredients.split(', ')
    accuracy = calculate_accuracy(user_ingredients.split(','), recommended_ingredients)
    precision = calculate_precision(user_ingredients.split(','), recommended_ingredients)
    recall = calculate_recall(user_ingredients.split(','), recommended_ingredients)
    accuracy_scores.append(accuracy)
    precision_scores.append(precision)
    recall_scores.append(recall)

mean_accuracy = np.mean(accuracy_scores)
mean_precision = np.mean(precision_scores)
mean_recall = np.mean(recall_scores)

print(f"Precision: {mean_precision:.2f}")
print(f"Accuracy: {mean_accuracy:.2f}")
print(f"Recall: {mean_recall:.2f}")