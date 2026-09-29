import pandas as pd
import tkinter as tk
import tkinter.messagebox as messagebox
from threading import Thread

class App:
    def __init__(self, root, model, file_path):
        self.model = model
        self.root = root
        self.root.title("Food Recommendation System")
        self.root.configure(background="peach puff")
 
        self.df = pd.read_excel(file_path)
        self.data_dict = self.df.to_dict(orient='records')

        # Size of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}") 

        # Font settings
        font_title = ("Times New Roman", 18)
        font_button = ("Times New Roman", 16)
        font_settings = ("Cooper Black", 20)
        font_big = ("Cooper Black", 26)
        font_tips = ("Times New Roman", 14)

        top = tk.Label(self.root, text="Welcome To \n", font=font_settings, bg="lightpink")
        top.place(x=0, y=0, width=screen_width)
        top = tk.Label(self.root, text="What To Eat Today?\n", font=font_big, bg="lightpink")
        top.place(x=0, y=30, width=screen_width)
        top = tk.Label(self.root, text="Food Recommendation System", font=font_settings, bg="lightpink")
        top.place(x=0, y=65, width=screen_width)

        # Left frame
        self.left_frame = tk.Frame(self.root, width=screen_width // 2, height=screen_height, bg="peach puff")
        self.left_frame.place(x=0, y=105)

        # Right frame
        self.right_frame = tk.Frame(self.root, width=screen_width // 2, height=screen_height, bg="peach puff")
        self.right_frame.place(x=screen_width // 2, y=105)

        # "Enter ingredients" label
        label = tk.Label(self.left_frame, text="Enter ingredients:", font=font_title)
        label.place(x=30, y=30)

        # Entry box for ingredients
        self.entry = tk.Text(self.left_frame, width=50, height=10, font=font_title)
        self.entry.place(x=30, y=85)

        # Notes
        notes = tk.Label(self.left_frame, text="***Please use comma and space ', ' to separate the ingredients***\n***Please enter more than 2 ingredients***\n***Please input ingredients in singular form***", font=font_tips)
        notes.place(x=30, y=375)

        # Button to get the ingredients
        button = tk.Button(self.left_frame, text="Get Recommendations", command=self.start_thread, font=font_button)
        button.place(x=30, y=465)

        # Recommended Recipe
        output = tk.Label(self.right_frame, text="Recommended Recipe: ", font=font_title)
        output.place(x=30, y=30)

        # Output text box
        self.output_position = tk.Text(self.right_frame, width=50, height=20, font=font_title, state=tk.DISABLED, bg="white")
        self.output_position.place(x=30, y=85)

    def start_thread(self):
        thread = Thread(target=self.get_ingredients)
        thread.start()

    def get_ingredients(self):
        ingredients = self.entry.get("1.0", tk.END).strip()

        input_ingredients = [item.strip() for item in ingredients.split(",")]
        
        ingredient_count = len(input_ingredients)

        uniqueIngredient = set()

        recipes = []

        for index, row in self.df.iterrows():
            recipe = {"dish": row["recipe_name"], "ingredients": row["ingredients"].split(", ")}
            recipes.append(recipe)

        for recipe in recipes:
            for unique in recipe["ingredients"]:
                uniqueIngredient.add(unique)

        matchingCount = 0
        #Check whether the ingredients input are in the ingredient list
        for ingredient in (item.lower() for item in input_ingredients):
            for recipeIngredient in uniqueIngredient:
                if ingredient == recipeIngredient:
                    matchingCount += 1

        if ingredient_count == 1:
            error1 = "Please enter more than 2 ingredients."
            messagebox.showerror("Error", error1)
            return
        
        if ", " not in ingredients:
            if ingredient_count >1:
                error2 = "Please use comma and space (', ') to separate the ingredients."
                messagebox.showerror("Error", error2)
                return
        
        if matchingCount < 2:
            error3 = "No recommended recipe found.\nPlease try again with your other available ingredients."
            messagebox.showerror("Error", error3)
            return
        
        # Call the backend class
        recommended_recipes = self.model.recommend_recipes(ingredients)

        # Update recommended recipe
        self.update_output(recommended_recipes)

    def update_output(self, recommended_recipes):
        self.output_position.config(state=tk.NORMAL)  # Make the Text widget editable
        self.output_position.delete("1.0", tk.END)  # Clear previous content

        font_button = ("Times New Roman", 16)
        # Create buttons for recommended recipes
        for recipe in recommended_recipes:
            missing_ingredients = self.model.missing_ingredients(self.entry.get("1.0", tk.END).strip(), [recipe])[0]['missing_ingredients']

            missing_ingredients_str = ', '.join(missing_ingredients)
            max_missing_length = 50  
            if len(missing_ingredients_str) > max_missing_length:
                missing_ingredients_str = '\n'.join([missing_ingredients_str[i:i+50] for i in range(0, len(missing_ingredients_str), 50)])   

            if len(missing_ingredients) ==0:
                button_text = f"{recipe['recipe_name']} \nYou have all the ingredients needed!"

            else:
                button_text = f"{recipe['recipe_name']} \n(Missing: {', '.join(missing_ingredients)})"

            button = tk.Button(self.output_position, text=button_text, command=lambda r=recipe: self.display_recipe_details(r), font=font_button, wraplength=550)  
            self.output_position.window_create("end", window=button)
            self.output_position.insert("end", "\n")

        self.output_position.config(state=tk.DISABLED)

    def display_recipe_details(self, recipe):
        # Create a new window to display the recipe details
        details_window = tk.Toplevel(self.root)
        details_window.title(recipe['recipe_name'])
        details_window.configure(bg="peach puff")

        #Screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        details_window.geometry(f"{screen_width}x{screen_height}")

        font_title = ("Times New Roman", 18)
        font_content = ("Times New Roman", 14)
        font_recipename = ("Times New Roman", 20)

        # Create frames for left and right 
        left_frame = tk.Frame(details_window, bg="peach puff")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") 

        right_frame = tk.Frame(details_window, bg="peach puff")
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Display recipe name
        recipe_name = tk.Label(left_frame, text=f"Recipe: {recipe['recipe_name']}", font=font_recipename, bg="peach puff")
        recipe_name.pack()

        # Display ingredients
        ingredients = tk.Label(left_frame, text="\nIngredients:", font=font_title, bg="peach puff")
        ingredients.pack()
        ingredients_content = tk.Text(left_frame, width=70, height=2, font=font_content, bg="white")
        ingredients_content.insert(tk.END, recipe['ingredients'] if 'ingredients' in recipe else 'No ingredients available')
        ingredients_content.config(state=tk.DISABLED)
        ingredients_content.pack()

        # Display detailed ingredients
        detailed_ingredients_label = tk.Label(left_frame, text="\nDetailed Ingredients:", font=font_title, bg="peach puff")
        detailed_ingredients_label.pack()
        detailed_ingredients_content = tk.Text(left_frame, width=70, height=10, font=font_content, bg="white")
        detailed_ingredients_content.insert(tk.END, recipe['ingredients details'] if 'ingredients details' in recipe else 'No details available')
        detailed_ingredients_content.config(state=tk.DISABLED)
        detailed_ingredients_content.pack()

        # Display nutrition information
        nutrition_label = tk.Label(left_frame, text="\nNutrition Information:", font=font_title, bg="peach puff")
        nutrition_label.pack()
        nutrition_content = tk.Text(left_frame, width=70, height=7, font=font_content, bg="white")
        nutrition_content.insert(tk.END, recipe.get('nutrition', 'No nutrition information available'))
        nutrition_content.config(state=tk.DISABLED)
        nutrition_content.pack()

        # Display total time
        total_time_label = tk.Label(left_frame, text="\nTotal Time:", font=font_title, bg="peach puff")
        total_time_label.pack()
        total_time_content = tk.Text(left_frame, width=70, height=1, font=font_content, bg="white")
        total_time_content.insert(tk.END, recipe.get('total_time_filled', 'No total time available'))
        total_time_content.config(state=tk.DISABLED)
        total_time_content.pack()

        # Display instructions
        instructions_label = tk.Label(right_frame, text="\n\nInstructions:", font=font_title, bg="peach puff")
        instructions_label.pack()
        instructions_content = tk.Text(right_frame, width=70, height=30, font=font_content, bg="white")
        instructions_content.insert(tk.END, recipe.get('instructions', 'No instructions available'))
        instructions_content.config(state=tk.DISABLED)
        instructions_content.pack()

        # Make the grid expandable
        details_window.grid_rowconfigure(0, weight=1)
        details_window.grid_columnconfigure(0, weight=1)
        details_window.grid_columnconfigure(1, weight=1)