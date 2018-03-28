from flask import Flask, request, render_template, flash
import recipeConverter as rc
# import win32clipboard

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f28567d441f2b6176a'

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

    if request.method == 'POST':
        if request.form['submit'] == 'Convert':
            # store the given text in a variable
            input_text = request.form.get("text")

            parse_form_text(input_text)

            # change the text (add 'Hi' to each new line)
            # input_text = '\n'.join(text_converted)
            # (i used <br> to materialize a newline in the returned value)

            # for line in text_converted:
            #     flash(line)

        # elif request.form['submit'] == 'Paste From Clipboard':
        #     input_text = get_clipboard_data()

        #     parse_form_text(input_text)

        elif request.form['submit'] == 'Clear':
            input_text = ''

    return render_template('form.html', textarea=input_text)

# def get_clipboard_data():
#     # get clipboard data
#     win32clipboard.OpenClipboard()
#     data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
#     win32clipboard.CloseClipboard()
    
#     return data

def parse_form_text(text):
    recipe = rc.RecipeConverter()

    # split the text to get each line in a list
    text2 = text.split('\n')

    text_converted = recipe.parse_recipe(text2)

    # input_text = text

    for line in text_converted:
        flash(line)

if __name__ == '__main__':
    app.run()