import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox


class Recipe:
    def __init__(self, name, ingredients, steps, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.steps = steps
        self.cooking_time = cooking_time


class RecipeRecommendationSystem:
    def __init__(self):
        self.user_data = {}
        self.recipe_data = []

    def start(self):
        self.collect_user_information()
        self.collect_recipe_data()
        self.generate_recommendations()
        self.present_recommendations()

    def collect_user_information(self):
        messagebox.showinfo("Recipe Recommendation System", "Welcome to the Recipe Recommendation System!")
        user_name = tk.simpledialog.askstring("Recipe Recommendation System", "Please enter your name:")
        self.user_data["name"] = user_name

        cuisine = tk.simpledialog.askstring("Recipe Recommendation System", "Please enter your preferred cuisine:")
        self.user_data["cuisine"] = cuisine

        cooking_time = tk.simpledialog.askstring("Recipe Recommendation System", "Please enter your preferred cooking time:")
        self.user_data["cooking_time"] = cooking_time

        calorie_count = tk.simpledialog.askstring("Recipe Recommendation System", "Please enter your desired calorie count:")
        self.user_data["calorie_count"] = calorie_count

        allergies = tk.simpledialog.askstring("Recipe Recommendation System", "Please enter any allergies you have (comma-separated):")
        self.user_data["allergies"] = allergies

        ingredients = tk.simpledialog.askstring("Recipe Recommendation System", "Please enter the ingredients you have (comma-separated):")
        self.user_data["ingredients"] = ingredients.split(",")

    def collect_recipe_data(self):
        query = self.user_data["cuisine"] + " recipe"
        search_results = self.search_recipes(query)
        recipe_urls = self.extract_recipe_urls(search_results)

        for url in recipe_urls:
            recipe_data = self.extract_recipe_data(url)
            self.recipe_data.append(recipe_data)

    def search_recipes(self, query):
        url = f"https://www.google.com/search?q={query}"
        response = requests.get(url)
        search_results = response.text
        return search_results

    def extract_recipe_urls(self, search_results):
        soup = BeautifulSoup(search_results, "html.parser")
        search_results = soup.find_all("a")
        recipe_urls = []

        for result in search_results:
            link = result.get("href")
            if link.startswith("https://www.recipe"):
                recipe_urls.append(link)

        return recipe_urls

    def extract_recipe_data(self, recipe_url):
        response = requests.get(recipe_url)
        recipe_html = response.text
        soup = BeautifulSoup(recipe_html, "html.parser")

        recipe_name = soup.find("h1").text

        ingredients = soup.find_all("li", class_="ingredient")
        ingredient_list = [ingredient.text.strip() for ingredient in ingredients]

        preparation_steps = soup.find_all("li", class_="step")
        steps_list = [step.text.strip() for step in preparation_steps]

        cooking_time = soup.find("time", class_="prepTime").text.strip()

        recipe_data = Recipe(recipe_name, ingredient_list, steps_list, cooking_time)
        return recipe_data

    def generate_recommendations(self):
        recommendation_data = self.apply_ml_algorithm()
        self.user_data["recommendations"] = recommendation_data

    def apply_ml_algorithm(self):
        recommendation_data = []

        for recipe in self.recipe_data:
            if recipe.cooking_time == self.user_data["cooking_time"]:
                recommendation_data.append(recipe)

        return recommendation_data

    def present_recommendations(self):
        messagebox.showinfo("Recipe Recommendation System", f"Hello {self.user_data['name']}! Here are your personalized recipe recommendations:")

        for i, recipe in enumerate(self.user_data["recommendations"], start=1):
            recommendation_str = f"Recipe {i}:\n"
            recommendation_str += f"Name: {recipe.name}\n"
            recommendation_str += "Ingredients:\n"
            for ingredient in recipe.ingredients:
                recommendation_str += "- " + ingredient + "\n"
            recommendation_str += "Steps:\n"
            for j, step in enumerate(recipe.steps, start=1):
                recommendation_str += f"{j}. " + step + "\n"
            recommendation_str += "--------\n"
            messagebox.showinfo("Recipe Recommendation System", recommendation_str)


recipe_system = RecipeRecommendationSystem()
recipe_system.start()