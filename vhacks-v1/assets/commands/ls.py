import os, sys, time, json, hashlib, requests, argparse, base64, tabulate

def md5(text):
    return hashlib.md5(str(text).encode("utf-8")).hexdigest()
    
def convert_bytes(size):
    for x in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024.0:
            return "%3.1f%s" % (size, x)
        size /= 1024.0

parse = argparse.ArgumentParser()
parse.add_argument("username")
parse.add_argument("file")
parse.add_argument("homedir")
args = parse.parse_args()

data = json.loads(
    base64.b64decode(
        open(f"{args.homedir}/assets/data/folder-{md5(args.username)}/{md5(args.username)}", "r").read()
    )
)

allDirectory = []
totalSize = 0

dataTable = []

print("")
if args.file == "your.log":
    for file in os.listdir(os.getcwd()):
        path = f"{os.getcwd()}/{file}"
        if os.path.isfile(path):
            dataTable.append([
                "-rw-rw----.",
                1,
                args.username,
                convert_bytes(os.path.getsize(path)),
                time.ctime(os.path.getmtime(path))[4:][:-8],
                file
            ])
            totalSize += float(os.path.getsize(path))
        else:
            dataTable.append([
                "drwxrws---.",
                len(os.listdir(path)),
                args.username,
                convert_bytes(os.path.getsize(path)),
                time.ctime(os.path.getmtime(path))[4:][:-8],
                f"\033[1;34m{file}\033[1;37m"
            ])
            totalSize += float(os.path.getsize(path))
else:
    if os.path.isdir(args.file):
        for file in os.listdir(args.file):
            path = f"{args.file}/{file}"
            if os.path.isfile(path):
                dataTable.append([
                    "-rw-rw----.",
                    1,
                    args.username,
                    convert_bytes(os.path.getsize(path)),
                    time.ctime(os.path.getmtime(path))[4:][:-8],
                    file
                ])
                totalSize += float(os.path.getsize(path))
            else:
                dataTable.append([
                    "drwxrws---.",
                    len(os.listdir(path)),
                    args.username,
                    convert_bytes(os.path.getsize(path)),
                    time.ctime(os.path.getmtime(path))[4:][:-8],
                    f"\033[1;34m{file}\033[1;37m"
                ])
                totalSize += float(os.path.getsize(path))
    else:
        print(f"\033[1;37m[\033[1;30m{ltime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[1;37m] This is not directory")
headersTable = [f"Total {convert_bytes(totalSize)}", "", "", "", "", ""]
print(tabulate.tabulate(dataTable, headersTable, tablefmt="plain", numalign="left"))
print("")