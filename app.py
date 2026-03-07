from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for now
# Later you can replace this with SQLite
pantry_items = []
recipes = []
next_recipe_id = 1


def normalize(text: str) -> str:
    return text.strip().lower()


def compare_recipe_to_pantry(recipe_ingredients, pantry):
    pantry_set = {normalize(item) for item in pantry}

    have = []
    need = []

    for ingredient in recipe_ingredients:
        if normalize(ingredient) in pantry_set:
            have.append(ingredient)
        else:
            need.append(ingredient)

    return have, need


@app.route("/")
def home():
    return redirect(url_for("view_pantry"))


@app.route("/pantry", methods=["GET", "POST"])
def view_pantry():
    if request.method == "POST":
        item = request.form.get("item", "").strip()
        if item:
            pantry_items.append(item)
        return redirect(url_for("view_pantry"))

    return render_template("pantry.html", pantry_items=pantry_items)


@app.route("/pantry/delete/<int:item_index>", methods=["POST"])
def delete_pantry_item(item_index):
    if 0 <= item_index < len(pantry_items):
        pantry_items.pop(item_index)
    return redirect(url_for("view_pantry"))


@app.route("/recipes")
def view_recipes():
    return render_template("recipes.html", recipes=recipes)


@app.route("/recipes/add", methods=["GET", "POST"])
def add_recipe():
    global next_recipe_id

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        ingredients_text = request.form.get("ingredients", "").strip()

        if name and ingredients_text:
            ingredients = [
                line.strip()
                for line in ingredients_text.splitlines()
                if line.strip()
            ]

            recipes.append({
                "id": next_recipe_id,
                "name": name,
                "ingredients": ingredients
            })
            next_recipe_id += 1

            return redirect(url_for("view_recipes"))

    return render_template("add_recipe.html")


@app.route("/recipes/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = next((r for r in recipes if r["id"] == recipe_id), None)

    if recipe is None:
        return "Recipe not found", 404

    have, need = compare_recipe_to_pantry(recipe["ingredients"], pantry_items)

    return render_template(
        "recipe_detail.html",
        recipe=recipe,
        have=have,
        need=need
    )


if __name__ == "__main__":
    app.run(debug=True)