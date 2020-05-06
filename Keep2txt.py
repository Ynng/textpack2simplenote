from pathlib import Path
import json
import string
import random
from datetime import datetime
import sys
import os

stdout_fileno = sys.stdout
sys.stdout = open('output.json', "w")


def randomString(stringLength=32):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


pathlist = Path("D:/User/Downloads/Test").glob("*")
output = {"activeNotes": [], "trashedNotes": []}

for path in pathlist:
    path_in_str = str(path)
    with open(path_in_str+"\\info.json", encoding='utf-8') as fh:
        data = json.load(fh)


    timestamp = data["noteEntity"]["creationDate"]/1000
    dt_object = datetime.fromtimestamp(timestamp)
    creationDate = "{:%Y-%m-%dT%H:%M:%S.000Z}".format(dt_object)
    timestamp = data["noteEntity"]["modificationDate"]/1000
    dt_object = datetime.fromtimestamp(timestamp)
    modificationDate = "{:%Y-%m-%dT%H:%M:%S.000Z}".format(dt_object)

    with open(path_in_str+"\\text.markdown", encoding='utf-8') as fh:
      content = fh.read()
      
    # print(content)

    noteId = data["noteEntity"]["identifier"]
    output["activeNotes"].append({"id": noteId, "content": content, "creationDate" : creationDate, "lastModified": modificationDate})

sys.stdout.write(json.dumps(output))
