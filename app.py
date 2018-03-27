from flask import Flask, request, render_template
import recipeConverter as rc

app = Flask(__name__)

@app.route('/')
def main_form():
    return render_template('form.html')
    # '<form action="submit" id="textform" method="post"><textarea name="text">Hello World!</textarea><input type="submit" value="Submit"></form>'

@app.route('/submit', methods=['POST'])
def submit_textarea():
    # store the given text in a variable
    text = request.form.get("text")

    # split the text to get each line in a list
    text2 = text.split('\n')

    recipe = rc.RecipeConverter()
    text_converted = recipe.parse_recipe(text2)

    # change the text (add 'Hi' to each new line)
    text_changed = '<br>'.join(text_converted)
    # (i used <br> to materialize a newline in the returned value)


    return "{}".format(text_changed)

if __name__ == '__main__':
    app.run()