# Used to convert a timeIndex (time in minutes) into a readable string
def makeReadable(time):
  hour = str(int(time / 60))
  minutes = str(time % 60)
  if len(hour) == 1: hour = "0" + hour
  if len(minutes) == 1: minutes = "0" + minutes
  return hour + ":" + minutes