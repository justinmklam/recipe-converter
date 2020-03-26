from flask import Flask, request, render_template, jsonify
from recipe_scrapers import scrape_me
import recipeconverter as rc

app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "7d441f27d441f28567d441fb6176a"


@app.route("/", methods=["GET"])
def hello():
    return render_template("form.html")


@app.route("/convert", methods=["POST"])
def convert():
    response = request.get_json()
    recipe = rc.RecipeConverter()

    text = response["data"]
    multiplier = float(response["multiplier"])

    return jsonify({"data": recipe.convert_recipe(text, multiplier)})


@app.route("/ingredients_from_url", methods=["POST"])
def ingredients_from_url():
    response = request.get_json()
    scraper = scrape_me(response["url"])

    return jsonify({
        "ingredients": "\n".join(scraper.ingredients()),
        "instructions": scraper.instructions().replace("\n", "\n\n")
    })


if __name__ == "__main__":
    app.run(debug=False)
