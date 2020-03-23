from flask import Flask, request, render_template
import recipeconverter as rc


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f28567d441fb6176a'


@app.route('/', methods=["GET"])
def hello():
    return render_template('form.html')


@app.route("/convert", methods=["POST"])
def convert():
    recipe = rc.RecipeConverter()

    text = request.form["data"]
    multiplier = float(request.form["multiplier"])

    return recipe.convert_recipe(text, multiplier)


if __name__ == '__main__':
    app.run(debug=False)
