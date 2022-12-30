# Base image
FROM python:3-alpine

# Create app directory
WORKDIR /recipe-converter

# Install app dependencies
COPY . .
RUN pip install -e .

# Run the app
WORKDIR /recipe-converter/app
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]