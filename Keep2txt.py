from pathlib import Path
import json
import string
import random
from datetime import datetime
import sys
import os
import re

stdout_fileno = sys.stdout
sys.stdout = open('output.json', "w")


def randomString(stringLength=32):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


pathlist = Path("D:/User/Downloads/Backup").glob("*")
output = {"activeNotes": [], "trashedNotes": []}

for path in pathlist:
    path_in_str = str(path)
    with open(path_in_str+"\\info.json", encoding='utf-8') as fh:
        data = json.load(fh)

    timestamp = data["noteEntity"]["modificationDate"]/1000
    dt_object = datetime.fromtimestamp(timestamp)
    modificationDate = "{:%Y-%m-%dT%H:%M:%S.000Z}".format(dt_object)
    timestamp = data["noteEntity"]["creationDate"]/1000
    dt_object = datetime.fromtimestamp(timestamp)
    creationDate = "{:%Y-%m-%dT%H:%M:%S.000Z}".format(dt_object)


    with open(path_in_str+"\\text.markdown", encoding='utf-8') as fh:
      content = fh.read()
    
    content_list = content.split("\n")
    if content_list[0].startswith("#") and content_list[1].startswith("201"):
      content_list.append("")
      content_list.append(content_list[0])
      del content_list[0]
    
    if not content_list[0].startswith("201"):
      content_list.insert(0, "{:%Y/%m/%d}".format(dt_object))

    content="\n".join(content_list)

    tags = re.findall(r"#([a-zA-Z]+[a-zA-Z])#", content)  

    noteId = data["noteEntity"]["identifier"]
    output["activeNotes"].append({"id": noteId, "content": content, "creationDate" : creationDate, "lastModified": modificationDate, "tags" : tags})

sys.stdout.write(json.dumps(output))
