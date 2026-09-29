import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load dataset
file_path = r"C:\Users\Zhi Ling.DELL-ZLPG\OneDrive - 厦门大学(马来西亚分校) (1)\cleaned_recipe.xlsx"
df = pd.read_excel(file_path)
data_dict = df.to_dict(orient='records')

ingredients = [recipe['ingredients'] for recipe in data_dict]
recipe_names = [recipe['recipe_name'] for recipe in data_dict]

vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split(', '), token_pattern=None)
X = vectorizer.fit_transform(ingredients)


# Model
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test, ingredients_train, ingredients_test = train_test_split(
    X, recipe_names, ingredients, test_size=0.2, random_state=42
)

knn = NearestNeighbors(n_neighbors=5, algorithm='auto')
knn.fit(X_train)

def recommend_recipes(user_ingredients, n_recommendations=3):
    user_ingredients_vector = vectorizer.transform([user_ingredients])
    distances, indices = knn.kneighbors(user_ingredients_vector, n_neighbors=n_recommendations)
    
    recommendations = []
    for idx in indices[0]:
        recommendations.append({'recipe_name': y_train[idx], 'ingredients': ingredients_train[idx]})

    return recommendations

def missing_ingredients(user_ingredients, recipes):
    user_ingredients_set = set(user_ingredients.split(', '))
    missing = []
    
    for recipe in recipes:
        recipe_ingredients_set = set(recipe['ingredients'].split(', '))
        missing_ingredients = recipe_ingredients_set - user_ingredients_set
        
        missing.append({'recipe_name': recipe['recipe_name'], 'missing_ingredients': missing_ingredients})
        
    return missing


# Example user input
user_ingredients = 'ice cream, whipping cream, flour'
recommendations = recommend_recipes(user_ingredients)
missing_ingredients_info = missing_ingredients(user_ingredients, recommendations)

for i, info in enumerate(missing_ingredients_info):
    print(f"Recommendation {i+1}: {info['recipe_name']}")
    
    if not info['missing_ingredients']:
        print("You have all the ingredients needed!")
        print()
        
    else:
        print(f"Missing ingredients: {', '.join(info['missing_ingredients'])}")
        print()
    

# Validation (Accuracy with TN Value)
import numpy as np

def calculate_accuracy(user_input, system_recommendation, all_ingredients):
    user_set = set(user_input)
    recommendation_set = set(system_recommendation)
    all_ingredients_set = set(all_ingredients)
    
    # Correctly recommended ingredients
    TP = user_set.intersection(recommendation_set)
     
    # Ingredients recommended but not in user's list
    FP = recommendation_set.difference(user_set)

    # Ingredients in user's list but not recommended
    FN = user_set.difference(recommendation_set)

    # Ingredients not in user's list and not recommended
    TN = all_ingredients_set.difference(user_set.union(recommendation_set))
    
    accuracy = (len(TP) + len(TN)) / (len(TP) + len(FP) + len(FN) + len(TN)) if (len(TP) + len(FP) + len(FN) + len(TN)) > 0 else 0
    precision = len(TP) / (len(TP) + len(FP)) if (len(TP) + len(FP)) > 0 else 0
    recall = len(TP) / (len(TP) + len(FN)) if (len(TP) + len(FN)) > 0 else 0
    
    return accuracy, precision, recall

accuracy_scores = []
precision_scores = []
recall_scores = []

unique_ingredients = list(set([ingredient.strip() for combo in ingredients for ingredient in combo.split(',')]))

for recommendation in recommendations:
    recommended_ingredients = recommendation['ingredients'].split(', ')
    accuracy, precision, recall = calculate_accuracy(user_ingredients.split(', '), recommended_ingredients, unique_ingredients)
    accuracy_scores.append(accuracy)
    precision_scores.append(precision)
    recall_scores.append(recall)

mean_accuracy = np.mean(accuracy_scores)
mean_precision = np.mean(precision_scores)
mean_recall = np.mean(recall_scores)

print(f"Precision: {mean_precision:.2f}")
print(f"Accuracy (including TN value): {mean_accuracy:.2f}")
print(f"Recall: {mean_recall:.2f}\n")


# Validation (Accuracy without TN Value)
import numpy as np

def calculate(user_input, system_recommendation):
    user_set = set(user_input)
    recommendation_set = set(system_recommendation)
    
    TP = user_set.intersection(recommendation_set)

    FP = recommendation_set.difference(user_set)
    
    FN = user_set.difference(recommendation_set)
    
    accuracy = len(TP) / (len(TP) + len(FP) + len(FN)) if (len(TP) + len(FP) + len(FN)) > 0 else 0
    precision = len(TP) / (len(TP) + len(FP)) if (len(TP) + len(FP)) > 0 else 0
    recall = len(TP) / (len(TP) + len(FN)) if (len(TP) + len(FN)) > 0 else 0
    
    return accuracy, precision, recall


accuracy_scores = []
precision_scores = []
recall_scores = []

for recommendation in recommendations:
    recommended_ingredients = recommendation['ingredients'].split(', ')
    accuracy, precision, recall = calculate(user_ingredients.split(', '), recommended_ingredients)
    accuracy_scores.append(accuracy)
    precision_scores.append(precision)
    recall_scores.append(recall)

mean_accuracy = np.mean(accuracy_scores)
mean_precision = np.mean(precision_scores)
mean_recall = np.mean(recall_scores)

print(f"Precision: {mean_precision:.2f}")
print(f"Accuracy: {mean_accuracy:.2f}")
print(f"Recall: {mean_recall:.2f}")