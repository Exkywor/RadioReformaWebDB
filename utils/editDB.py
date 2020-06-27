from utils.handleTimezone import changeTimezone
from utils.validations import validateSchedule, validateInfo
from utils.misc import isEmpty

def editDB(changes, db, offset, indexedSchedule, programs):
  id = changes["id"]
  info = changes["info"]
  schedule = changes["schedule"]

  # Store what we're going to do to the DB
  infoToChange = {}
  scheduleToChange = {}
  
  if bool(schedule): # Check that there are changes in the schedule
    # Validate schedule
    scheduleValidated = validateSchedule(schedule, indexedSchedule, id)
    if scheduleValidated["res"] is False:
      return scheduleValidated["message"]

    # Prepare the schedule to change it by the timezone
    toTimezoneSchedule = {}
    for day in schedule:
      if isEmpty(schedule[day]): # If empty we'll set it to None (NULL)
        scheduleToChange[day] = None
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
    infoValidated = validateInfo(info, id, programs)
    if infoValidated["res"] is False:
      return infoValidated["message"]
    
    # Prepare the elements to change
    for key in info:
      if key == "length":
        infoToChange[key] = int(info[key])
      elif key == "presenters":
        if isEmpty(info[key]) or info[key] == ("Desconocido" or "desconocido"):
          infoToChange[key] = None
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

  # EDIT THE DB
  cursor = db.cursor()
  # Update information
  if bool(infoToChange):
    for item in infoToChange:
      cursor.execute(f"UPDATE Programs SET {item}=? WHERE programID={id}", [infoToChange[item]])
    db.commit()
  if bool(scheduleToChange):
    for item in scheduleToChange:
      cursor.execute(f"UPDATE Airs SET {item}=? WHERE programID={id}", [scheduleToChange[item]])
    db.commit()

  return "Éxito"