# Project Title

A flower shop used to base the price of their flowers on an item by item cost. So if a
customer ordered 10 roses then they would be charged 10x the cost of single rose. The
flower shop has decided to start selling their flowers in bundles and charging the customer
on a per bundle basis. So if the shop sold roses in bundles of 5 and 10 and a customer
ordered 15 they would get a bundle of 10 and a bundle of 5.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or above installed on your machine
- SQLite3 installed if not included in your Python installation

## Installation

To install this project, follow these steps:

1. **Install Poetry**

   Poetry is a tool for dependency management and packaging in Python. To install Poetry, run:

   ```bash
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
## Clone the repository
Clone this repository to your local machine:
```bash 
git clone https://github.com/vinod008rs/flower_project.git
```
Navigate into the project directory:
```shell
cd flower_project
```
## Install dependencies

With Poetry installed, run the following command to install the project dependencies:
```shell
poetry install

```

## Initialize the Database

Run the following commands to initialize your database:
```shell
poetry run python manage.py migrate

```

## Create a Superuser

To create an admin user for accessing the Django admin panel, run:

```shell
poetry run python manage.py createsuperuser

```

## Usage
### Running the Development Server
To run the Django development server, use the following command:

```shell
poetry run python manage.py runserver

```

This will start the server on http://127.0.0.1:8000/ by default.

## Adding Bundle Prices
If you need to add bundle prices using the add_bundle_price.py script, you can do so with the following command:
```shell
poetry run python manage.py add_bundle_price

```

## Running Tests
To run the test suite, use the following command:

```shell
poetry run python manage.py test

```

This will discover and run all `tests` in the tests directory.
