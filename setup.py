from setuptools import find_packages, setup

setup(
    name="recipeconverter",
    version="2.0.0",
    description="A tool to convert baking ingredients from volume to weight",
    author="Justin Lam",
    author_email="contact@justinmklam.com",
    url="https://github.com/namtonthat/recipe-converter",
    packages=find_packages(),
    scripts=[],
    install_requires=["flask", "gunicorn", "recipe-scrapers"],
    include_package_data=True,
    zip_safe=False,
)
