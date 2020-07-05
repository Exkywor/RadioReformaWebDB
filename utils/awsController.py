import boto3

# Configures the dynamodb
dynamo_client = boto3.client('dynamodb')

def getDynamoItems():
  items = None
  try:
    items = dynamo_client.scan(TableName='notifications-dev')
  except Exception as e:
    print(e)

  # Create empty lists of the users (tokens) and programs (IDs)
  users = {el["token"]["S"]: [] for el in items["Items"]}
  programs = {el["program"]["N"]: [] for el in items["Items"]}

  # Append the tokens and IDs to the corresponding lists
  for el in items["Items"]:
    users[el["token"]["S"]].append(el["program"]["N"])
    programs[el["program"]["N"]].append(el["token"]["S"])

  # Sorts the lists
  for user in users: users[user].sort(key=int)
  for program in programs: programs[program].sort()
  # Sort the dictionaries
  users = {user: users[user] for user in sorted(users)}
  programs = {program: programs[program] for program in sorted(programs, key=int)}

  return {"tokens": users, "IDs": programs, "count": items["Count"]}