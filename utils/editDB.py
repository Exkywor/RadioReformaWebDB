def editDB(changes, cursor, offset):
  # print(changes)
  print(offset)

  cursor.execute("SELECT * from Programs")
  programsToDict = cursor.fetchall()
  # print(programsToDict)