from utils.handleTimezone import changeTimezone
from utils.validations import validateSchedule, validateInfo
from utils.misc import isEmpty

def editDB(changes, cursor, offset, indexedSchedule, programs):
  id = changes["id"]
  info = changes["info"]
  schedule = changes["schedule"]

  # Store what we're going to do to the DB
  infoToChange = {}
  infoToDelete = []
  scheduleToChange = {}
  scheduleToDelete = []
  
  if bool(schedule): # Check that there are changes in the schedule
    # Validate schedule
    scheduleValidated = validateSchedule(schedule, indexedSchedule, id)
    if scheduleValidated["res"] is False:
      return scheduleValidated["message"]

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
      return infoValidated["message"]
    
    # Prepare the elements to change
    for key in info:
      if key == "length":
        infoToChange[key] = int(info[key])
      elif key == "presenters":
        if isEmpty(info[key]) or info[key] == ("Desconocido" or "desconocido"):
          infoToDelete.append(key)
        else:
          elements = info[key].strip().split(", ")
          capitalized = [el.capitalize() for el in elements]
          infoToChange[key] = ", ".join(capitalized)
      elif key == "topics":
        elements = info[key].strip().split(", ")
        capitalized = [el.capitalize() for el in elements]
        infoToChange[key] = ", ".join(capitalized)
      else:
        infoToChange[key] = info[key].strip()

  print(infoToChange)


    # Should move all of this into a getChanges() function so I can reuse this code for the addProgram()
    # MAYBE! What do to with delete?

  # cursor.execute("SELECT * from Programs")
  # programsToDict = cursor.fetchall()
  # print(programsToDict)
  return "Éxito"