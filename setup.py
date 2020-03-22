from setuptools import find_packages, setup

setup(
    name="recipeconverter",
    version="0.1.0",
    description="A tool to convert baking ingredients from volume to weight",
    author="Justin Lam",
    author_email="contact@justinmklam.com",
    url="https://github.com/justinmklam/recipe-converter",
    packages=find_packages(),
    scripts=[],
    install_requires=["flask"],
    zip_safe=False,
)
