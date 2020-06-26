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
      # Delete the day if it's empty
      if schedule[day] == "":
        print("TO DELETE")
      else:
        print("TO ADD")        

  print("Hi")

  # for key in info:
  #   print(key)
  #   print(info[key])

  # cursor.execute("SELECT * from Programs")
  # programsToDict = cursor.fetchall()
  # print(programsToDict)