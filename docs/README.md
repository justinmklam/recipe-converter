# Recipe Converter

A tool to convert baking ingredients from volume to weight

## Getting Started

## Installation

To install the package locally for development (ideally in a virtual environment):

```bash
# Install the package
pip3 install -e .

# Install the development requirements and pre-commit hooks
pip3 install -r requirements-dev.txt
pre-commit install
```

## Documentation

To build the documentation:

```bash
cd docs/

# Install sphinx requirements (if necessary)
pip3 install -r requirements.txt

# Build the docs
make html

# Open the docs in your browser
google-chrome _build/html/index.html
```

## Usage

## Releases

If tagged releases are used, the following script can be run to generate a changelog between tags. This will create/update a `CHANGELOG.md` file.

```bash
./bin/generate-changelog.sh
```
