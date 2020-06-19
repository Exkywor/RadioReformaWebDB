from flask import Flask, render_template, request, redirect
from cs50 import SQL

from utils.prepareDB import prepareDB

# Configure app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
  response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
  response.headers["Expires"] = 0
  response.headers["Pragma"] = "no-cache"
  return response

# Open the db
db = SQL("sqlite:///programs.db")
programsList = db.execute("SELECT * from Programs")
# We could join programs and airs but it would make it harder to filter an iterate through empty days
airingList = db.execute("SELECT * from Airs")

# Prepares the programs and schedule
processed = prepareDB(programsList, airingList)
programs = processed["programs"]
schedule = processed["schedule"]

@app.route("/")
def index():
  return render_template("index.html", programs=programs)

@app.route("/programs")
def programsSomething():
  return render_template("index.html", title="Something something")