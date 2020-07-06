# Radio Reforma Programs' DB Manager

This is my final project for CS50's Introduction to Computer Science 2020 (I took the 2019's course but did this project in 2020)


Web application to visualize and manage the Radio Reforma programs' database.

In the main page you can view the list of programs, filter them, sort them. You can edit, add or delete a program. You can also change the timezone of the displayed information.
In the schedule page you can see a weekly schedule and perform filtering and viewing operations with it.
In the notifications page you can retrieve the notifications information from the AWS DynamoDB and view it in relationship with the programs.

This web app uses Flask for the backend and HTML with jQuery for the frontend.

## Installation

Simply clone the repository and install all the required packages via:

```bash
pip install -r requirements.txt
```

## Usage
Make sure to run the app via `python` rather than with `flask run` since you need to pass the path to the database as an argument.

```python
python app.py path-to-the-database/programs.db
```