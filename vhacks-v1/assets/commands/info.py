import argparse, json, base64, hashlib

parse = argparse.ArgumentParser()
parse.add_argument("username")
parse.add_argument("file")
parse.add_argument("homedir")
args = parse.parse_args()

def md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

data = json.loads(
    base64.b64decode(
        open(f"{args.homedir}/assets/data/folder-{md5(str(args.username))}/{md5(str(args.username))}").read()
    )
)

print("\n\t\033[1;30;47m [ Your Account Info ] \033[0m\n\033[1;37m")
print(f"[*] Username: {data['username']} => {md5(str(args.username))}")
print(f"[*] IPv4: {data['rhost']}")
print(f"[*] Platform: {data['platform']}")
print(f"[*] VHC: {data['vhcoin']}")
print(f"[*] Firewall: Lv.{data['firewall']}")
print(f"[*] SDK: Lv.{data['sdk']}")
print(f"[*] IP-Spoofing: Lv.{data['ip_spoofing']}")
print(f"[*] Scan: Lv.{data['scan']}")
print("")