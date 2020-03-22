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

    if request.method == 'POST':
        if request.form['submit'] == 'Convert':
            # store the given text in a variable
            input_text = request.form.get("text")

            # recipe multiplier
            try:
                multiplier = float(request.form.get("multiplier"))
            except ValueError:
                multiplier = 1.0
            parse_form_text(input_text, multiplier)

        elif request.form['submit'] == 'Clear':
            input_text = ''

    return render_template('form.html', textarea=input_text, multiplier=multiplier)

def parse_form_text(text, multiplier):
    recipe = rc.RecipeConverter()

    text_converted = recipe.convert_recipe(text, multiplier)

    for line in text_converted.split("\n"):
        flash(line)

if __name__ == '__main__':
    app.run(debug=False)
