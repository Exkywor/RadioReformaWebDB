# Converts a timeIndex (time in minutes) into a readable string
def makeReadable(time):
  hour = str(int(time / 60))
  minutes = str(time % 60)
  if len(hour) == 1: hour = "0" + hour
  if len(minutes) == 1: minutes = "0" + minutes
  return hour + ":" + minutes

# Check if a string is empty or only whitespaces
def isEmpty(string):
  if (string == "") or (string.isspace()):
    return True
  else:
    return False