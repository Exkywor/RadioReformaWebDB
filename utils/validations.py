from utils.misc import isEmpty, isAlphanumeric

# Schedule validation
# schedule = {"monday": "05:10, 15:00"}
def validateSchedule(schedule, indexedSchedule, id, action ="edit"):
  if action == "add":
    if len(schedule) == 0: # Check that the program has at least one airing
      return {"res": False, "message": f"El programa debe estar al aire al menos una vez"}

  if action == "edit":
    # We'll check that we are not erasing all the airings for the day
    if len(schedule) > 0: # Only check if the schedule is not empty
      # Store the days that the program airs
      daysForProgram = [day for day in indexedSchedule for indexID in indexedSchedule[day] if indexedSchedule[day][indexID] == id]
      # Sort the daysToProgram and the schedule
      daysForProgram.sort()
      scheduleDays = list(schedule.keys())
      scheduleDays.sort()

      # We'll abort if:
      # a) Both lists are the same and all the changes are to empty the schedule.
      # b) Incoming schedule has more days but all of them are to empty the schedule
      if daysForProgram == scheduleDays:
        if all(len(value) == 0 for value in schedule.values()):
          return {"res": False, "message": f"El programa debe estar al aire al menos una vez"}
      elif len(scheduleDays) > len(daysForProgram):
        if all(len(value) == 0 for value in schedule.values()):
          return {"res": False, "message": f"El programa debe estar al aire al menos una vez"}
      
  for day in schedule:
    # Skip the day if it's empty or contains only whitespaces
    if isEmpty(schedule[day]):
      continue

    ogTime = schedule[day].strip() # Remove any trailing whitespaces
    times = ogTime.split(", ")

    validCharacters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ",", " "]
    for c in range(len(ogTime)):
      if ogTime[c] not in validCharacters: # Check if the time contains invalid characters
        return {"res": False, "message": f"La hora para el {day.upper()} contiene caracteres inválidos: {ogTime[c]}"}
      # Check that the times are separated by ", "
      if ogTime[c] == ",":
        if c == len(ogTime)-1:
          return {"res": False, "message": f"Quita las comas al final de las horas para el {day.upper()}"}
        if ogTime[c+1] != " ":
          return {"res": False, "message": f"Separa las horas para el {day.upper()} con una coma seguida de un espacio"}

    # Check if a time was input
    if times[0] == ",":
      return {"res": False, "message": f"El {day.upper()} no puede contener solo una coma"}
    
    for time in times:
      split = time.split(":")

      if len(split) <= 1:
        return {"res": False, "message": f"La hora para el {day.upper()} tiene un formato incorrecto. El formato debe ser: hh:mm, hh:mm"}
      
      # Check if the time is formatted properly
      # Avoid 05:5
      if len(split[1]) < 2:
        return {"res": False, "message": f"La hora para el {day.upper()} tiene un formato incorrecto. El formato debe ser: hh:mm, hh:mm"}
      # Avoid 050:00 or 05:000
      for i in split:
        if (len(i) > 2) or (len(i) == 0) :
          return {"res": False, "message": f"La hora para el {day.upper()} tiene un formato incorrecto. El formato debe ser: hh:mm, hh:mm"}
      
      # Check that the time doesn't exist already for other programs, in other words, that it's unique
      timeIndex = (int(split[0]) * 60) + int(split[1])
      if timeIndex in indexedSchedule[day].keys():
        if action == "edit":
          # If the timeIndex already exists, check that it belongs to a different program
          # This handles if you add a time to an existing day of a program,
          # because it will try to validate the already existing time
          if id != indexedSchedule[day][timeIndex]:
            return {"res": False, "message": f"La hora {time} para el {day.upper()} ya está asignada para el programa con ID {indexedSchedule[day][timeIndex]}"}
        else:
          return {"res": False, "message": f"La hora {time} para el {day.upper()} ya está asignada para el programa con ID {indexedSchedule[day][timeIndex]}"}

  return {"res": True, "message": "El horario es válido"}


# Info validation
def validateInfo(info, id, programs, action ="edit"):
  if not bool(programs): # Check that a programs argument has been passed
    return print("ERROR: No programs passed to validateInfo()")

  # Validation for new programs
  if action == "add":
    # Check that all required fields are filled
    if "name" not in info:
      return {"res": False, "message": f"Debes añadir un nombre para el programa"}
    if "streamID" not in info:
      return {"res": False, "message": f"Debes asignar un identificador del programa para el stream de audio"}
    if "author" not in info:
      return {"res": False, "message": f"Debes añadir el productor del programa"}
    if "length" not in info:
      return {"res": False, "message": f"Debes añadir la duración del programa"}
    if "topics" not in info:
      return {"res": False, "message": f"Debes añadir los temas del programa"}
    if "descriptionShort" not in info:
      return {"res": False, "message": f"Debes añadir una descripción corta (sinopsis) del programa"}
    if "descriptionLong" not in info:
      return {"res": False, "message": f"Debes añadir una descripción larga del programa"}
    
    # Validate the streamID
    if isEmpty(info["streamID"]):
      return {"res": False, "message": f"Debes asignar un identificador del programa para el stream de audio"}
    streamIDs = [programs[program]["streamID"] for program in programs]
    if info["streamID"].strip() in streamIDs:
      return {"res": False, "message": f"El streamID {info['streamID']} ya está asignado a otro programa"}
  

  # Check that the program has a name, and that it is unique
  if "name" in info:
    if isEmpty(info["name"]):
      return {"res": False, "message": f"Debes añadir un nombre para el programa"}
    if not isAlphanumeric(info["name"]):
      return {"res": False, "message": f"El nombre no puede contener solo caracteres especiales"}
    programNames = [programs[program]["name"] for program in programs]
    if info["name"].strip() in programNames:
      if action == "edit":
        if programs[id]["name"] != info["name"].strip(): # In case it's a non-modification for the same program
          return {"res": False, "message": f"El nombre '{info['name']}' ya está asignado a otro programa"}
      else:
        return {"res": False, "message": f"El nombre '{info['name']}' ya está asignado a otro programa"}
  
  # Check the author
  if "author" in info:
    if isEmpty(info["author"]):
      return {"res": False, "message": f"Debes añadir el productor del programa"}
    if not isAlphanumeric(info["author"]):
      return {"res": False, "message": f"El productor no puede contener solo caracteres especiales"}

  # Validate the length
  if "length" in info:
    if int(info["length"]) < 1:
      return {"res": False, "message": f"La duración debe ser mayor a 0"}

  # Check the topics
  if "topics" in info:
    if isEmpty(info["topics"]):
      return {"res": False, "message": f"Debes añadir al menos un tema para el programa"}
    topics = info["topics"].strip()
    if not isAlphanumeric(topics):
      return {"res": False, "message": f"El tema no puede contener solo caracteres especiales"}
    # Check that the topics are separated by ", "
    for c in range(len(topics)):
      if topics[c] == ",": # The program finds a ,
        if c == len(topics)-1: # Is it the last character?
          return {"res": False, "message": f"Quita las comas al final de los temas"}
        if topics[c+1] != " ": # Is it followed by a space?
          return {"res": False, "message": f"Separa los temas con una coma seguida de un espacio"}

  # Check that the presenters are separated by ", "
  if "presenters" in info:
    presenters = info["presenters"].strip()
    if (len(presenters) > 0): # Proceed if presenters is not empty, ignore and consider as valid otherwise
      if not isAlphanumeric(presenters):
        return {"res": False, "message": f"Los presentadores no pueden contener solo caracteres especiales"}
      for c in range(len(presenters)):
        if presenters[c] == ",": # The program finds a ,
          if c == len(presenters)-1: # Is it the last character?
            return {"res": False, "message": f"Quita las comas al final de los presentadores"}
          if presenters[c+1] != " ": # Is it followed by a space?
            return {"res": False, "message": f"Separa los presentadores con una coma seguida de un espacio"}

  # Check the descriptionShort
  if "descriptionShort" in info:
    if isEmpty(info["descriptionShort"]):
      return {"res": False, "message": f"Debes añadir una descripción corta (sinopsis) del programa"}
    if not isAlphanumeric(info["descriptionShort"]):
      return {"res": False, "message": f"La descripción corta (sinopsis) no puede contener solo caracteres especiales"}
    
    # Validate descriptionShort character count
    if len(info["descriptionShort"]) > 250:
      return {"res": False, "message": f"La descripción corta (sinopsis) contiene más de 250 caracteres"}
  
  # Check the descriptionLong
  if "descriptionLong" in info:
    if isEmpty(info["descriptionLong"]):
      return {"res": False, "message": f"Debes añadir una descripción larga del programa"}
    if not isAlphanumeric(info["descriptionLong"]):
      return {"res": False, "message": f"La descripción no puede contener solo caracteres especiales"}
  
  return {"res": True, "message": "La información es válida"}