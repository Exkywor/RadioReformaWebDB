import datetime, json, pytz, sqlite3
from flask import Flask, jsonify, render_template, request, redirect, session
from flask_session import Session
from tempfile import mkdtemp

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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Open the db
db = sqlite3.connect("programs.db", check_same_thread=False)
db.row_factory = sqlite3.Row # We'll use this to convert the tuples into rows
cursor = db.cursor()

# Sets the programs and the schedule, which we'll use in the app
def getData():
  processed = prepareDB(session["programsList"], session["airingList"], session["timeoffset"])
  session["programs"] = processed["programs"]
  session["schedule"] = processed["schedule"]
  
  if session.get("loaded") is None:
    session["loaded"] = True


@app.route("/", methods=["GET", "POST"])
def index():
  # This would give us tuples, so we changed it to get Rows. We'll convert them into a dict later
  cursor.execute("SELECT * from Programs")
  programsToDict = cursor.fetchall()
  cursor.execute("SELECT * from Airs") # We could join programs and airs but it would make it harder to filter an iterate through empty days
  airingToDict = cursor.fetchall()

  # We extract the information from the Rows and convert them to dicts
  programsList = []
  for program in programsToDict:
    programsList.append({key:program[key] for key in program.keys()})
  airingList = []
  for airing in airingToDict:
    airingList.append({key:airing[key] for key in airing.keys()})

  session["programsList"] = programsList
  session["airingList"] = airingList

  # Timezone variables
  if session.get("timezone") is None:
    session["timezone"] = "America/El_Salvador"
  if session.get("timeoffset") is None:
    session["timeoffset"] = -360

  if session.get("loaded") is None:
    getData()

  return render_template("index.html", title="Programas")


@app.route("/programs", methods=["GET", "POST"])
def getPrograms():
  if request.method == "POST":
    return jsonify(session["programs"])


@app.route("/schedule", methods=["GET", "POST"])
def getSchedule():
  if request.method == "POST":
    return jsonify(session["schedule"])

  return render_template("schedule.html", title="Horarios")


@app.route("/getTimezone", methods=["POST"])
def getTimezone():
  if request.method == "POST":
    return jsonify(timezone=session["timezone"], timezones=pytz.common_timezones)


@app.route("/changeTimezone", methods=["POST"])
def changeTimezone():
  if request.method == "POST":
    session["timezone"] = request.form.get("timezone")
    # We get the utcoffset in seconds, then convert it to minutes, then use int() to remove the decimal point
    session["timeoffset"] = int(datetime.datetime.now(pytz.timezone(session["timezone"])).utcoffset().total_seconds()/60)

    getData()

    return jsonify(timezone=session["timezone"])


@app.route("/editProgram", methods=["POST"])
def editProgram():
  if request.method == "POST":
    # Converts the serialized string back into a dictionary
    data = json.loads(request.form.get("data"))
    print(data["info"]["name"])

    return jsonify(True)