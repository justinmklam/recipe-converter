# Metric Recipe Converter

![Python application](https://github.com/justinmklam/recipe-converter/workflows/Python%20application/badge.svg?branch=master) [![Build Status](https://travis-ci.org/justinmklam/recipe-converter.svg?branch=master)](https://travis-ci.org/justinmklam/recipe-converter) [![Coverage Status](https://coveralls.io/repos/github/justinmklam/recipe-converter/badge.svg?branch=master)](https://coveralls.io/github/justinmklam/recipe-converter?branch=master) [![Documentation Status](https://readthedocs.org/projects/recipe-converter/badge/?version=latest)](https://recipe-converter.readthedocs.io/en/latest/?badge=latest)


Web app to convert recipes from imperial volume to metric weight units.

**Link to live project:** [recipe-converter-app.herokuapp.com](http://recipe-converter-app.herokuapp.com/)

<p align="center">
<img src="docs/imgs/recipe-converter.gif">
</p>

## Features

+ Convert cups, tablespoons, and teaspoons of common ingredients to grams
+ Scale the recipe up or down
+ Option to load recipe from URL (if website is supported)
+ Reader view for distraction-free viewing (no ads or other fluff!)

## Built With
+ [Flask](http://flask.pocoo.org/) backend
+ [Spectre](https://picturepan2.github.io/spectre/) frontend
+ [Heroku](https://www.heroku.com/) hosting

## Getting Started

### General

To install the package:

```bash
pip install -e .
```

To run the web app:

```bash
cd app/
flask run
```

### For Developers

To install dependencies:

```bash
pip install -r requirements-dev.txt
pip install -r docs/requirements.txt
```

To run development tasks:

```bash
# Run the tests
pytest tests/

# Build the docs
cd docs
make html
```

## Usage

Example usage of the module is shown below:

```python
import recipeconverter
rc = recipeconverter.RecipeConverter()

rc.convert_volume_to_mass("1 cup flour")
# 142 g flour

rc.convert_volume_to_mass("1 tsp sugar")
# 4.2 g sugar

recipe = """2/3 cup butter
1 cup sugar
3 bananas
1/2 teaspoon salt"""

rc.convert_recipe(recipe, mutliplier=2.0)
# 302.7 g butter
# 396 g sugar
# 6 bananas
# 5 g salt

rc.convert_recipe_from_url("https://www.allrecipes.com/recipe/20144/banana-banana-bread/")
# 284 g all-purpose flour
# 6 g baking soda
# 1.2 g salt
# 113.5 g butter
# 148.5 g brown sugar
# 2 eggs, beaten
# 2.3 cup mashed overripe bananas
```
