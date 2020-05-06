from pathlib import Path
import json
import string
import random
from datetime import datetime
import sys
import os

stdout_fileno = sys.stdout
sys.stdout = open('output.json',"w")

def randomString(stringLength=32):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

pathlist = Path("D:/User/Downloads/Takeout/Keep").glob("*.json")
output = {"activeNotes": [], "trashedNotes":[]}

for path in pathlist:
  path_in_str = str(path)

  with open(path_in_str, encoding='utf-8') as fh:
      data = json.load(fh)

  timestamp = data["userEditedTimestampUsec"]/1000000
  dt_object = datetime.utcfromtimestamp(timestamp)
  dateString = "{:%Y-%m-%dT%H:%M:%S.000Z}".format(dt_object)

  textContent = ""
  if 'textContent' in data:
    textContent = data['textContent']
  elif 'listContent' in data:
    textContent = ""
    for item in data['listContent']:
      if(item["isChecked"]):
        textContent = textContent + "- [x] "
      else:
        textContent = textContent + "- [ ] "

      textContent = textContent + item["text"] + "\n"

  if not data['title']:
    content = textContent
  else: 
    content = data['title'] + "\n" + textContent

  noteId = randomString(32)
  if (not data["isArchived"]) and (not data["isTrashed"]):
    output["activeNotes"].append({"id": noteId, "content": content, "creationDate" : dateString, "lastModified": dateString})
  else:
    output["trashedNotes"].append({"id": noteId, "content": content, "creationDate" : dateString, "lastModified": dateString})

sys.stdout.write(json.dumps(output))