from utils.misc import makeReadable

# We use this for the getDay and sorting functions
daysList = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# Looks for a previous or next day
def getDay(day, direction):
  index = daysList.index(day)

  # Get the previous day
  if direction == "previous":
    if index == 0: return daysList[6] # Wrap around if we're at the beginning
    return daysList[index - 1]
  elif direction == "next": # Get the next day
    if index == 6: return daysList[0] # Wrap around if we're at the end
    return daysList[index + 1]
  

# Changes the times and days of the programs depending on the timezone
# The offset is in minutes
def changeTimezone(schedule, timeoffset):
  newSchedule = {} # We're gonna store a new schedule since some programs may change day depending on the timezone

  for day in schedule:
    # Get a list containing the times for the day. They are split in times and minutes
    splitTimes = [time.split(":") for time in schedule[day]]

    for time in splitTimes:
      minutes = (int(time[0]) * 60) + int(time[1]) # Convert the time to minutes
      timezonedMinutes = minutes + timeoffset # Change the time by the time offset
      newTime = 0 # The time we're going to store

      # If the minutes are less than 0 it means that the time should go to a previous day
      if timezonedMinutes < 0:
        # Corrects the time and then splits it into an array of numbers
        newTime = timezonedMinutes + 1440
        newDay = getDay(day, "previous") # Gets the previous day to assing the time to

        # If the day doesn't exist in the newSchedule we add a new key and store the new item
        if not newDay in newSchedule.keys(): newSchedule[newDay] = [newTime]
        else: newSchedule[newDay].append(newTime)
      elif timezonedMinutes >= 1440: # More than 1440 means the day should go to a next day
        # Corrects the time and then splits it into an array of numbers
        newTime = timezonedMinutes - 1440
        newDay = getDay(day, "next") # Gets the next day to assing the time to

        # If the day doesn't exist in the newSchedule we add a new key and store the new item
        if not newDay in newSchedule.keys(): newSchedule[newDay] = [newTime]
        else: newSchedule[newDay].append(newTime)
      else: # The time doesn't need to be moved from it's day
        newTime = timezonedMinutes

        # If the day doesn't exist in the newSchedule we add a new key and store the new item
        if not day in newSchedule.keys(): newSchedule[day] = [newTime]
        else: newSchedule[day].append(newTime)
  
  # We're gonna sort the times
  for day in newSchedule:
    # We sort the times for the day
    # This is very useful for when the time gets added from a following day,
    # but needs to be set before a time already place for that day
    newSchedule[day].sort()

    # We convert the times back intro strings
    stringList = [makeReadable(time) for time in newSchedule[day]]
    newSchedule[day] = stringList

  # We're gonna sort the times days
  # We store the indexes of the days so we can easily sort them
  currentOrder = [daysList.index(day) for day in newSchedule]
  currentOrder.sort()
  # We create a new ordered dict based on the sorted indexes
  orderedSchedule = {daysList[index]:newSchedule[daysList[index]] for index in currentOrder}

  return orderedSchedule