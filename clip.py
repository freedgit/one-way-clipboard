#!/usr/bin/env python3

from utils import *

DEBUG = True
SLEEP_TIME = 5

previous = ""

while (True):
    if DEBUG:
        print("reading clipboard...")

    paths = get_paths()
    insert_path = paths["insert_path"]

    if os.path.exists(insert_path):
        if DEBUG:
            print("insertion incoming")

        with open(insert_path, "r") as f:
            r = f.read()

        ins = json.loads(r)

        content = ins["content"]

        previous = content
        pc.copy(content)

        os.remove(insert_path)

        if DEBUG:
            print("inserted into clipboard.")

        continue
        
    x = pc.paste()
    x = x.lstrip()

    if x == previous:
        if DEBUG:
            print("content is the same.")

        time.sleep(SLEEP_TIME)
        continue

    file_path = paths["clip_path"]

    ret = {}
    ret["type"] = "nothing"
    ret["content"] = ""
    
    if os.path.exists(file_path):
        if DEBUG:
            print("file exists.")
            
        file_exists = True

        with open(file_path, "r") as f:
            r = f.read()

        rr = json.loads(r)

        if rr["type"] != ret["type"] or rr["content"] != ret["content"]:
            file_differs = True

            if DEBUG:
                print("file differs from clipboard.")

            # ret["type"] = rr["type"]
            # ret["content"] = rr["content"]
    else:
        if DEBUG:
            print("file does NOT exist.")
            file_differs = True

    if x != "" and file_differs:
        
        if x.startswith("http://") or x.startswith("https://"):
            if DEBUG:
                print("it is a url.")
            ret["type"] = "url"
            ret["content"] = x
        else:
            if DEBUG:
                print("it is regular content.")            
            ret["type"] = "content"
            ret["content"] = x

        with open(file_path, "w") as f:
            f.write(json.dumps(ret))

        previous = x

    time.sleep(SLEEP_TIME)
