# The Team system project

## Application setup

```bash
# Set up a virtual environment
pip install pipenv

pipenv shell
pipenv sync

# Install migrations
python src/manage.py migrate

# Project launch
python src/manage.py runserver
```

## Swagger documentation:

http://localhost:8000/docs/
