# Schedule validation
# schedule = {"monday": "05:10, 15:00"}
def validateSchedule(schedule, indexedSchedule, id):
  for day in schedule:
    # Skip the day if it's empty
    if schedule[day] in ("", " "):
      continue

    ogTime = schedule[day].strip() # Remove any trailing whitespaces
    times = ogTime.split(", ")

    for c in range(len(ogTime)):
      if ogTime[c] == ",":
        if ogTime[c+1] != " ":
          return {"res": False, "message": f"Pon un espacio después de las comas para el día {day.upper()}"}

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
          return {"res": False, "message": f"Una hora para el {day.upper()} ya existe para el programa con ID {indexedSchedule[day][timeIndex]}"}

  return {"res": True, "message": "El horario es válido"}