import json, requests, base64, argparse, os, hashlib
from datetime import datetime as lhost

parse = argparse.ArgumentParser()
parse.add_argument("username")
parse.add_argument("file")
parse.add_argument("homedir")
args = parse.parse_args()

def md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()
    
req = requests.get(f"http://localhost:8080/assets/data/folder-{md5(str(args.username))}/home/{args.file}")
if req.status_code == 404:
    print(f"\033[1;37m[\033[1;30m{lhost.now().strftime('%Y-%m-%d %H:%M:%S')}\033[1;37m] File not found")
else:
    open(f"{args.homedir}/assets/data/folder-{md5(str(args.username))}/home/{args.file}", "w").write(
        req.text
    )
    os.system(f"nano {args.homedir}/assets/data/folder-{md5(str(args.username))}/home/{args.file}")
    requests.post(f"http://localhost:8080", data={
        "file_name": f"folder-{md5(str(args.username))}/home/{args.file}",
        "file_data": open(f"{args.homedir}/assets/data/folder-{md5(str(args.username))}/home/{args.file}", "r").read(),
        "create_file": "submit"
    })