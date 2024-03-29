import datetime, json, pytz, sqlite3, sys
from flask import Flask, g, jsonify, render_template, request, redirect, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from urllib.request import pathname2url

from utils.awsController import getDynamoItems
from utils.prepareDB import prepareDB
from utils.modifyDB import editProgram, addProgram, deleteProgram

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
    try:
      dburi = 'file:{}?mode=rw'.format(pathname2url(sys.argv[1])) # Opens the db in read and write (not create) mode only
      db = g._database = sqlite3.connect(dburi, uri=True, check_same_thread=False)
    except Exception as e:
      print(e)
      sys.exit()
  db.row_factory = sqlite3.Row # We'll use this to convert the tuples into rows
  
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
      db.close()

# Parses the route to the database
def parseDBRoute():
  if len(sys.argv) < 2:
    print("Debes introducir la ruta a la base de datos")
    sys.exit()
  elif len(sys.argv) > 2:
    print("Debes introducir solo un argumento en la ruta de la base de datos")
    sys.exit()
  else:
    # Tests the db path to check if it works
    try:
      testuri = 'file:{}?mode=rw'.format(pathname2url(sys.argv[1]))
      sqlite3.connect(testuri, uri=True, check_same_thread=False)
    except Exception as e:
      print("No se pudo abrir la base de datos")
      sys.exit()
parseDBRoute()

# Sets the programs and the schedule, which we'll use in the app
def getData(fullLoad =False):
  if fullLoad:
    cursor = getDB().cursor()
    # This would give us tuples, so we changed it to get Rows. We'll convert them into a dict later
    try:
      cursor.execute("SELECT * from Programs")
    except Exception as e:
        print(e)
    programsToDict = cursor.fetchall()
    
    try:
      cursor.execute("SELECT * from Airs") # We could join programs and airs but it would make it harder to filter an iterate through empty days
    except Exception as e:
        print(e)
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

  processed = prepareDB(session["programsList"], session["airingList"], session["timeoffset"])
  session["programs"] = processed["programs"]
  session["schedule"] = processed["schedule"]
  
  if "loaded" not in session:
    session["loaded"] = True


@app.route("/", methods=["GET", "POST"])
def index():
  # Timezone variables
  if "timezone" not in session:
    session["timezone"] = "America/El_Salvador"
  if "timeoffset" not in session:
    session["timeoffset"] = -360

  if "loaded" not in session:
    getData(True)

  return render_template("index.html", title="Programas")


# MAIN DATA RETRIEVAL ENDPOINTS
@app.route("/programs", methods=["GET", "POST"])
def getPrograms():
  if request.method == "POST":
    return jsonify(programs=session["programs"], schedule=session["schedule"])

@app.route("/schedule", methods=["GET", "POST"])
def getSchedule():
  if "loaded" in session:
    if request.method == "POST":
      return jsonify(programs=session["programs"], schedule=session["schedule"])

    return render_template("schedule.html", title="Horarios")
  else:
    return redirect(url_for("index"))


# TIMEZONE RELATED ENDPOINTS
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


# DB OPERATIONS ENDPOINT
@app.route("/modifyProgram", methods=["POST"])
def modifyProgram():
  if request.method == "POST":
    action = request.form.get("action")
    data = json.loads(request.form.get("data")) # Converts the serialized js object back into a dictionary
    res = ""
    if action == "edit":
      res = editProgram(data, getDB(), session["timeoffset"], session["schedule"]["schedule"], session["programs"])
    elif action == "add":
      res = addProgram(data, getDB(), session["timeoffset"], session["schedule"]["schedule"], session["programs"])
    elif action == "delete":
      res = deleteProgram(data, getDB())
    
    getData(True)
    return jsonify(res)


# NOTIFICATIONS ENPOINT
@app.route("/notifications", methods=["POST", "GET"])
def getNotifications():
  if "loaded" in session:
    if request.method == "POST":
      return jsonify(notifications=getDynamoItems(), programs=session["programs"])
  else:
    return redirect(url_for("index"))

  return render_template("notifications.html", title="Notificaciones")

if __name__ == "__main__":
  app.run(debug=True)