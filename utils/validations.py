from utils.misc import isEmpty

# Schedule validation
# schedule = {"monday": "05:10, 15:00"}
def validateSchedule(schedule, indexedSchedule, id):
  for day in schedule:
    # Skip the day if it's empty or contains only whitespaces
    if isEmpty(schedule[day]):
      continue

    ogTime = schedule[day].strip() # Remove any trailing whitespaces
    times = ogTime.split(", ")

    # Check that the times are separated by ", "
    for c in range(len(ogTime)):
      if ogTime[c] == ",":
        if c == len(ogTime)-1:
          return {"res": False, "message": f"Quita las comas al final de los tiempos para el día {day.upper()}"}
        if ogTime[c+1] != " ":
          return {"res": False, "message": f"Pon un espacio después de las comas en las separaciones de los tiempos para el día {day.upper()}"}

    # Check if a time was input
    if times[0] == ",":
      return {"res": False, "message": f"ERROR: El día {day.upper()} no contiene ninguna hora"}
    
    # Check if the time contains invalid characters
    validCharacters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ",", " "]
    for c in range(len(ogTime)):
      if ogTime[c] not in validCharacters:
        return {"res": False, "message": f"ERROR: La hora para el {day.upper()} contiene caracteres inválidos: {ogTime[c]}"}
    
    for time in times:
      split = time.split(":")
      
      # Check if the time is formatted properly
      # Avoid 05:5
      if len(split[1]) < 2:
        return {"res": False, "message": f"La hora para el {day.upper()} tiene un formato incorrecto. El formato debe ser: hh:mm, hh:mm"}
      # Avoid 050:00 or 05:000
      for i in split:
        if len(i) > 2 :
          return {"res": False, "message": f"La hora para el {day.upper()} tiene un formato incorrecto. El formato debe ser: hh:mm, hh:mm"}
      
      # Check that the time doesn't exist already for other programs, in other words, that it's unique
      timeIndex = (int(split[0]) * 60) + int(split[1])
      if timeIndex in indexedSchedule[day].keys():
        # If the timeIndex already exists, check that it belongs to a different program
        # This handles if you add a time to an existing day of a program,
        # because it will try to validate the already existing time
        if id != indexedSchedule[day][timeIndex]:
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
      if programs[id]["streamID"] != info["streamID"].strip(): # In case it's a none-modification for the same program
        return {"res": False, "message": f"El streamID {info['streamID']} ya está asignado a otro programa"}
  

  # Check that the program has a name, and that it is unique
  if "name" in info:
    if isEmpty(info["name"]):
      return {"res": False, "message": f"Debes añadir un nombre para el programa"}
    programNames = [programs[program]["name"] for program in programs]
    if info["name"].strip() in programNames:
      if programs[id]["name"] != info["name"].strip(): # In case it's a none-modification for the same program
        return {"res": False, "message": f"El nombre '{info['name']}' ya está asignado a otro programa"}
  
  # Check the author
  if "author" in info:
    if isEmpty(info["author"]):
      return {"res": False, "message": f"Debes añadir el productor del programa"}

  # Validate the length
  if "length" in info:
    if int(info["length"]) < 1:
      return {"res": False, "message": f"La duración debe ser mayor a 0"}

  # Check the topics
  if "topics" in info:
    if isEmpty(info["topics"]):
      return {"res": False, "message": f"Debes añadir al menos un tema para el programa"}
    # Check that the topics are separated by ", "
    topics = info["topics"].strip()
    for c in range(len(topics)):
      if topics[c] == ",":
        if c == len(topics)-1:
          return {"res": False, "message": f"Quita las comas al final de los temas"}
        if topics[c+1] != " ":
          return {"res": False, "message": f"Pon un espacio después de las comas para los temas"}

  # Check that the presenters are separated by ", "
  if "presenters" in info:
    presenters = info["presenters"].strip()
    for c in range(len(presenters)):
      if presenters[c] == ",":
        if c == len(presenters)-1:
          return {"res": False, "message": f"Quita las comas al final de los presentadores"}
        if presenters[c+1] != " ":
          return {"res": False, "message": f"Pon un espacio después de las comas para los presentadores"}

  # Check the descriptionShort
  if "descriptionShort" in info:
    if isEmpty(info["descriptionShort"]):
      return {"res": False, "message": f"Debes añadir una descripción corta (sinopsis) del programa"}
    # Validate descriptionShort character count
    if len(info["descriptionShort"]) > 250:
      return {"res": False, "message": f"La sinópsis contiene más de 250 caracteres"}
  
  # Check the descriptionLong
  if "descriptionLong" in info:
    if isEmpty(info["descriptionLong"]):
      return {"res": False, "message": f"Debes añadir una descripción larga del programa"}
  
  return {"res": True, "message": "La información es válida"}