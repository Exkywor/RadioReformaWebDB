from utils.handleTimezone import changeTimezone
from utils.validations import validateSchedule

def editDB(changes, cursor, offset, indexedSchedule):
  id = changes["id"]
  info = changes["info"]
  schedule = changes["schedule"]

  # Convert schedule by timezone
  toTimezoneSchedule = {}

  # Proceed only if the schedule has days to convert
  if bool(schedule):
    # Validate schedule
    scheduleValidated = validateSchedule(schedule, indexedSchedule, id)
    if scheduleValidated["res"] is False:
      return print(scheduleValidated["message"])

    for day in schedule:
      # Add to delete list
      if schedule[day] in ("", " "):
        print("TO DELETE")
      else:
        ogTime = schedule[day].strip() # Remove any trailing whitespaces
        times = ogTime.split(", ")

        print("TO ADD")        

  print("Hi")

  # for key in info:
  #   print(key)
  #   print(info[key])

  # cursor.execute("SELECT * from Programs")
  # programsToDict = cursor.fetchall()
  # print(programsToDict)