import tkinter as tk
from appInterface import App
from recommend_recipe import RecipeRecommender

class Main:
    def __init__(self):
        file_path = r"C:\Users\Zhi Ling.DELL-ZLPG\OneDrive - 厦门大学(马来西亚分校) (1)\cleaned_recipe.xlsx"
        self.model = RecipeRecommender(file_path)
        self.root = tk.Tk()
        self.app = App(self.root, self.model, file_path)
        self.root.mainloop()

if __name__ == "__main__":
    Main()
 
