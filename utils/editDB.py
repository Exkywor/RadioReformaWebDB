from utils.handleTimezone import changeTimezone
from utils.validations import validateSchedule, validateInfo

def editDB(changes, cursor, offset, indexedSchedule, programs):
  id = changes["id"]
  info = changes["info"]
  schedule = changes["schedule"]

  # Store what we're going to to the DB
  infoToChange = {}
  infoToDelete = []
  scheduleToChange = {}
  scheduleToDelete = []
  
  if bool(schedule): # Check that there are changes in the schedule
    # Validate schedule
    scheduleValidated = validateSchedule(schedule, indexedSchedule, id)
    if scheduleValidated["res"] is False:
      return print(scheduleValidated["message"])

    # Prepare the schedule to change it by the timezone
    toTimezoneSchedule = {}
    for day in schedule:
      if schedule[day] in ("", " "): # Add to delete list
        scheduleToDelete.append(day)
      else:
        toTimezoneSchedule[day] = schedule[day].strip().split(", ") 

    # Covert the schedule to UTC time (the opposite of the current offset)
    timezoned = changeTimezone(toTimezoneSchedule, offset*-1)
    # timezone is of the shape of {day: ["hh:mm", "hh:mm"]}
    # this converts it back into {day: "hh:mm, hh:mm"}
    for d in timezoned:
      scheduleToChange[d] = ", ".join(timezoned[d])

  if bool(info): # Check that there are changes in the info
    # Validate info
    infoValidated = validateInfo(info, id, programs, "edit")
    if infoValidated["res"] is False:
      return print(infoValidated["message"])

    # NEED TO ITERATE OVER EVERY ELEMENT and strip trailing whitespaces
    # NEED TO CAPITALIZE FIRST WORD OF EACH TOPIC AND PRESENTER
      # Split > capitalize > join

    # Should move all of this into a getChanges() function so I can reuse this code for the addProgram()
    # MAYBE! What do to with delete?

  # cursor.execute("SELECT * from Programs")
  # programsToDict = cursor.fetchall()
  # print(programsToDict)