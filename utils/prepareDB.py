# Modifies, cleans, and adds the information of each program for our needs
def preparePrograms(programsList, airsList):
  # We use a dictionary instead of a list to store the programs to avoid confusion since the program's index in the list will be programID-1,
  # while on the DB and in the program info it is just progamID, which is prone to causing bugs.
  programs = {}
  schedule = {}

  for i in range(len(programsList)):
    filteredSchedule = {}

    # Excludes elements if they're null or programID
    for key in airsList[i]:
      if airsList[i][key] is not None and key != "programID":
        # Put each time in a list
        filteredSchedule[key] = airsList[i][key].split(", ")

    # Put each presenter in a list
    if programsList[i]["presenters"] is not None:
      programsList[i]["presenters"] = programsList[i]["presenters"].split(", ")
    else:
      programsList[i]["presenters"] = ["Desconocido"]
    # Sets the route for the image thumbnail
    programsList[i]["image"] = {"cover": programsList[i]["image"].replace("library/", "") + "-cover.jpg"}
    # Adds the schedule
    programsList[i]["schedule"] = filteredSchedule

    # Add elements to their corresponding dictionaries
    # We use i+1 to make sure the key correlates with the programID
    schedule[i+1] = filteredSchedule
    programs[i+1] = programsList[i]

  return {"programs": programs, "schedule": schedule}


# Creates a schedule based on the programs list
def createSchedule(schedule, programs):
  tempSchedule = {}
  # We store the programs that are in the schedule and only the information related to the schedule
  # This way we avoid passing the whole programs dictionary, which has unncessary information
  # We do it like this instead of assigning a dict to each time to avoid storing repeated information
  programsInfo = {}
  # A global list of all the times that have programs so we can render a side column with the times
  timesList = []

  # Used to convert a timeIndex (time in minutes) into a readable string
  def makeReadable(time):
    hour = str(round(time / 60))
    minutes = str(time % 60)
    if len(hour) == 1: hour = "0" + hour
    if len(minutes) == 1: minutes = "0" + minutes
    return hour + ":" + minutes
  
  for program in schedule:
    for day in schedule[program]:
      # Add a day if it doesn't exist in the temp schedule
      if not day in tempSchedule.keys():
        tempSchedule[day] = {}

      # We get make each time an index value and save it in its corresponding day
      # We use this value to: a) Sort and order every day b) Make sure a day doesn't repeat
      for time in schedule[program][day]:
        split = time.split(":") # We split the time so we can manipulate the hours and minutes separately
        timeIndex = (int(split[0]) * 60) + int(split[1]) # The time index is stored in minutes
        
        # We add the timeIndex to the times list in case it doesn't exist
        if timesList.count(timeIndex) == 0:
          timesList.append(timeIndex)

        tempSchedule[day][timeIndex] = program
        programsInfo[program] = {"name": programs[program]["name"], "length": programs[program]["length"]}

  # We sort the days and times in the tempSchedule so they are in order
  days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] # Used to get the days in order
  tupledSchedule = {day:sorted(tempSchedule[day].items()) for day in days if day in tempSchedule.keys()}

  # The sorting gives a tuple in return, we remake the dict here
  sortedSchedule = {}
  for day in tupledSchedule.keys():
    sortedSchedule[day] = {time[0]:time[1] for time in tupledSchedule[day]}

  # Sort the timesList
  timesList.sort()

  # NEED TO PROCESS TO GET READABLE TIME

  return {"schedule": sortedSchedule, "times": timesList, "programsInfo": programsInfo}


# Works with the database elements and returns what will be used by the site
def prepareDB(programsList, airsList):
  # This comes from a separate function in case we need to add more functions and processes before returning
  processed = preparePrograms(programsList, airsList)
  schedule = createSchedule(processed["schedule"], processed["programs"])

  return {"programs": processed["programs"], "schedule": schedule}