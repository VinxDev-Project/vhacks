import argparse, hashlib, requests, os, json
from datetime import datetime as ltime

parse = argparse.ArgumentParser()
parse.add_argument("username")
parse.add_argument("file")
parse.add_argument("homedir")

args = parse.parse_args()

def md5(text):
    return hashlib.md5(str(text).encode("utf-8")).hexdigest()

def getData(key):
    data = json.loads(open(f"{args.homedir}/assets/mysql-account/account.json", "r").read())
    return data[key]

helpPage = """
Usage: mkdir DIRECTORY...
Create a directory, if it doesn't exist.
"""

if args.file == "your.log":
    print(helpPage)
else:
    if os.path.exists(args.file):
        print(f"\033[1;37m[\033[1;30m{ltime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[1;37m] Cannot create directory '{args.file}' file exists")
    else:
        if 200 == requests.post(getData("url_server"), data={
            "folder_name": f"folder-{md5(args.username)}/{os.getcwd()}",
            "create_folder": "submit"
        }).status_code:
            os.mkdir()