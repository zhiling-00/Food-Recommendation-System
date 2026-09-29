import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split

class RecipeRecommender:
    def __init__(self, file_path):

        self.df = pd.read_excel(file_path)
        self.data_dict = self.df.to_dict(orient='records')

        self.ingredients = [recipe['ingredients'] for recipe in self.data_dict]
        self.recipe_names = [recipe['recipe_name'] for recipe in self.data_dict]

        self.vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split(', '), token_pattern=None)
        self.X = self.vectorizer.fit_transform(self.ingredients)

        self.X_train, self.X_test, self.y_train, self.y_test, self.ingredients_train, self.ingredients_test = train_test_split(
            self.X, self.recipe_names, self.ingredients, test_size=0.2, random_state=42
        )

        # Fit the KNN model
        self.knn = NearestNeighbors(n_neighbors=5, algorithm='auto')
        self.knn.fit(self.X_train)

    def recommend_recipes(self, user_ingredients, n_recommendations=3):
        user_ingredients_vector = self.vectorizer.transform([user_ingredients])
        distances, indices = self.knn.kneighbors(user_ingredients_vector, n_neighbors=n_recommendations)

        recommendations = []
        for idx in indices[0]:
            original_index = self.df.index[self.df['recipe_name'] == self.y_train[idx]].tolist()[0]
            recipe = self.data_dict[original_index]

            recommendations.append({
                'recipe_name': self.y_train[idx],
                'ingredients': self.ingredients_train[idx],
                'ingredients details': recipe['ingredients details'],
                'instructions': recipe['instructions'],
                'total_time_filled': recipe['total_time_filled'],
                'nutrition': recipe['nutrition']
            })

        return recommendations

    def missing_ingredients(self, user_ingredients, recipes):
        user_ingredients_set = set(user_ingredients.split(', '))
        missing = []

        for recipe in recipes:
            recipe_ingredients_set = set(recipe['ingredients'].split(', '))
            missing_ingredients = recipe_ingredients_set - user_ingredients_set

            missing.append({'recipe_name': recipe['recipe_name'], 'missing_ingredients': list(missing_ingredients)})

        return missing
