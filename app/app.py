from flask import Flask, request, render_template, flash
import recipeconverter as rc
# import win32clipboard

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f28567d441fb6176a'

@app.route('/', methods=['GET', 'POST'])
def hello():
    input_text = """1⁄2 cup butter
1 cup sugar
2 eggs, beaten
3 bananas, finely crushed (for serious and extreme moist and delicious, try 4 bananas)
1 1⁄2 cups flour
1 teaspoon baking soda
1⁄2 teaspoon salt
1⁄2 teaspoon vanilla (optional)"""

    multiplier = 1.0

    return render_template('form.html', textarea=input_text, multiplier=multiplier)


@app.route("/convert", methods=["POST"])
def convert():
    recipe = rc.RecipeConverter()

    text = request.form["data"]
    multiplier = float(request.form["multiplier"])
    print(text.strip())

    text_converted = recipe.convert_recipe(text, multiplier)

    return text_converted


if __name__ == '__main__':
    app.run(debug=False)
