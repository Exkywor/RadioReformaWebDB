import datetime, json, pytz, sqlite3
from flask import Flask, g, jsonify, render_template, request, redirect, session
from flask_session import Session
from tempfile import mkdtemp

from utils.prepareDB import prepareDB
from utils.editDB import editDB

# Configure app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Open the db and save it in the g namespace
def getDB():
  db = getattr(g, "_database", None)
  if db is None:
    db = g._database = sqlite3.connect("programs.db", check_same_thread=False)
  db.row_factory = sqlite3.Row # We'll use this to convert the tuples into rows
  
  return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Sets the programs and the schedule, which we'll use in the app
def getData():
  processed = prepareDB(session["programsList"], session["airingList"], session["timeoffset"])
  session["programs"] = processed["programs"]
  session["schedule"] = processed["schedule"]
  
  if "loaded" not in session:
    session["loaded"] = True


@app.route("/", methods=["GET", "POST"])
def index():
  cursor = getDB().cursor()

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
  if "timezone" not in session:
    session["timezone"] = "America/El_Salvador"
  if "timeoffset" not in session:
    session["timeoffset"] = -360

  if "loaded" not in session:
    getData()

  return render_template("index.html", title="Programas", loaded="True")


@app.route("/programs", methods=["GET", "POST"])
def getPrograms():
  if request.method == "POST":
    return jsonify(session["programs"])


@app.route("/schedule", methods=["GET", "POST"])
def getSchedule():
  if request.method == "POST":
    print(session["timeoffset"])
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

    editDB(data, getDB().cursor(), session["timeoffset"])

    return jsonify(True)

# @app.route("/editProgram", methods=["POST"])
# def editProgram():
#   if request.method == "POST":
#     

#     if "timeoffset" in session:
#       timeoffset = session["timeoffset"]
#       print(timeoffset)
#       editDB(data, getDB().cursor(), timeoffset)

#       return jsonify(True)
#     else:
#       print(session["timeoffset"])

      
#       return jsonify(False)

if __name__ == "__main__":
  app.run(debug=True)