# diary
A very simple diary

## Setup

To develop locally, do following steps:

- Clone the repository and cd to it

```
git clone https://github.com/shivams906/diary.git
cd diary
```

- Create a virtual environment and activate it

```
python -m venv venv
source venv/bin/activate
```

- Install the requirements

```
pip install -r requirements.txt
```

- Set Debug Value

```
export DEBUG=true
```

- Set up the database

```
python manage.py migrate
```

- Run the server

```
python manage.py runserver
```

## Tests

Run the following command

```
python manage.py test --settings diary_app.settings_for_tests
```

## Coverage

Run

```
coverage run --source='.' manage.py test --settings diary_app.settings_for_tests
```

- For report in terminal

```
coverage report
```

- For html report, run the following command and open the file htmlcov/index.html in your browser

```
coverage html
```
