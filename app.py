from flask import Flask, request, render_template, flash
import recipeConverter as rc

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f28567d441f2b6176a'

@app.route('/', methods=['GET', 'POST'])
def hello():
    input_text = "Enter your recipe in volumetric units (cups, tablespoons, teaspoons)"

    if request.method == 'POST':
        # store the given text in a variable
        text = request.form.get("text")

        # split the text to get each line in a list
        text2 = text.split('\n')

        recipe = rc.RecipeConverter()
        text_converted = recipe.parse_recipe(text2)

        # change the text (add 'Hi' to each new line)
        # input_text = '\n'.join(text_converted)
        input_text = text
        # (i used <br> to materialize a newline in the returned value)

        for line in text_converted:
            flash(line)

    return render_template('form.html', textarea=input_text)

if __name__ == '__main__':
    app.run()