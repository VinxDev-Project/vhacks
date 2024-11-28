import json, argparse

parse = argparse.ArgumentParser()
parse.add_argument("username")
parse.add_argument("file")
parse.add_argument("homedir")

args = parse.parse_args()

print("")
print("Core Commands")
print("==============")
print("")
print("\tCommand          Description")
print("\t--------         ------------")

commands = json.loads(
    open(f"{args.homedir}/assets/commands/list-command.json", "r").read()
)["commands"]

for command in commands:
    print(f"                         {command['description']}")
    print(f"\033[A\t{command['name']}")
print("")