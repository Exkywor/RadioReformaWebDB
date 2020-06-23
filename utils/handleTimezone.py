# Changes the times and days of the programs depending on the timezone
def changeTimezone(schedule, timeoffset):
  offset = int(timeoffset)
  newSchedule = {}

  # Splits the time into hours and minutes
  def arrayTime(time): return [round(time / 60), time % 60]

  print(offset)