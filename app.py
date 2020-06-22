from flask import Flask, jsonify, render_template, request, redirect
import sqlite3

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
db = sqlite3.connect("programs.db", check_same_thread=False)
db.row_factory = sqlite3.Row # We'll use this to convert the tuples into rows
cursor = db.cursor()
# This would give us tuples, so we changed it to get Rows, to convert thme into a dict later
cursor.execute("SELECT * from Programs")
programsToDict = cursor.fetchall()
cursor.execute("SELECT * from Airs") # We could join programs and airs but it would make it harder to filter an iterate through empty days
airingToDict = cursor.fetchall()
# We are gonna get a list of dicts from the Rows
programsList = []
for program in programsToDict:
  programsList.append({key:program[key] for key in program.keys()})
airingList = []
for airing in airingToDict:
  airingList.append({key:airing[key] for key in airing.keys()})

# Prepares the programs and schedule
processed = prepareDB(programsList, airingList)
programs = processed["programs"]
schedule = processed["schedule"]

timeoffset = "GMT-6"

@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
    return jsonify(programs)

  return render_template("index.html", title="Programas")

@app.route("/schedule", methods=["GET", "POST"])
def schedulePage():
  if request.method == "POST":
    return jsonify(schedule)

  return render_template("schedule.html", title="Horarios")

@app.route("/getTimezone", methods=["POST"])
def getTimezone():
  if request.method == "POST":
    return jsonify(timeoffset)

# ROUTE TO HANDLE TIMECHANGE
  # Change the timezone
  # Call preparedDB again (add the timezone as a parameter)
  # Change programs and schedule variables
  # Return true