# import win32clipboard
import unicodedata
import csv

class RecipeConverter:
    def __init__(self):
        # Conversion table from volumetric to metric grams
        self.conversions = self.import_conversions('gram-conversions.csv')
                
    def import_conversions(self, filename):
        with open(filename) as csvfile:
            conversion_table = list(csv.reader(csvfile, delimiter=','))

            # Remove header
            conversion_table.pop(0)

            return conversion_table
        
    def parse_line(self, ingredient):
        # From Genius recipes
        ingredient = ingredient.replace('1⁄4', '.25')
        ingredient = ingredient.replace('1⁄3', '.33')
        ingredient = ingredient.replace('1⁄2', '.5')
        ingredient = ingredient.replace('2⁄3', '.66')
        ingredient = ingredient.replace('3⁄4', '.75')

        # Standard float expressions
        ingredient = ingredient.replace('1/8', '.125')
        ingredient = ingredient.replace('1/4', '.25')
        ingredient = ingredient.replace('1/3', '.33')
        ingredient = ingredient.replace('1/2', '.5')
        ingredient = ingredient.replace('2/3', '.66')
        ingredient = ingredient.replace('3/4', '.75')
        
        # Replace abbreviations
        ingredient = ingredient.replace('tbsp','tablespoon')
        ingredient = ingredient.replace('tsp','teaspoon')
        ingredient = ingredient.replace('oz','ounces')

        return ingredient

    def convert_ingredient(self, line, unit, conversion):
        try:
            # Extract number from measurement
            number_string = line.split(unit)[0].replace(' ','')
            number_float = float(number_string)

            # Convert butter cup to grams
            converted = number_float * float(conversion)

            # Construct the output ingredient line with original line
            line_out = '%.1f g%s'%(converted, line.split(unit)[1].strip('s'))
        except:
            # Return the original line if any error occurred)
            line_out = line

        return line_out

    def parse_recipe(self, text):
        output = []

        for recipe_line in text:
            flag_converted = False

            # For each recipe line item, look it up in the conversion table
            for ingredient_gram in self.conversions:
                if ingredient_gram[0] in recipe_line:
                    flag_converted = True

                    # Convert fractions to floats and remove abbreviations
                    line = self.parse_line(recipe_line)

                    if 'cup' in line:
                        output.append(self.convert_ingredient(line, 'cup', ingredient_gram[1]))
                        break
                    elif 'tablespoon' in line:
                        output.append(self.convert_ingredient(line, 'tablespoon', ingredient_gram[2]))
                        break
                    elif 'teaspoon' in line:
                        output.append(self.convert_ingredient(line, 'teaspoon', ingredient_gram[3]))
                        break
                    else:
                        flag_converted = False

            # If nothing was found, then use original line
            if not flag_converted:
                output.append(recipe_line)

        return output

def display_lines(text_list):
    for line in text_list:
        print(line)
        
    print()