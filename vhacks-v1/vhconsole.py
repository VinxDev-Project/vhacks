#!/usr/bin/python
#coding: utf-8

import os, sys, time, json, random, shutil, hashlib, base64, platform, requests, mysql.connector
from datetime import datetime as ltime
from faker import Faker as generate
from pwinput import pwinput
from assets.script import core
from assets.script import script

mysqlAccount = json.loads(open(f"{core.homeDirectory}/assets/mysql-account/account.json", "r").read())
#mysqlAccount = json.loads(base64.b64decode(open("{core.homeDirectory}/assets/mysql-account/account_enc", "r").read()))

def prefix():
    return f"[\033[1;30m{ltime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[1;37m]"

def md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def mysqlGETALL(**arg):
    try:
        mysqlConnect = mysql.connector.connect(
            host = mysqlAccount["host"],
            user = mysqlAccount["user"],
            passwd = mysqlAccount["pass"],
            database = arg["database"],
            port = mysqlAccount["port"]
        )
        try:
            listColumns = []
            mysqlCursor = mysqlConnect.cursor()
            mysqlCursor.execute(f"describe {arg['table']}")
            for column in mysqlCursor.fetchall():
                listColumns.append(column[0])
            mysqlCursor.execute(f"select * from {arg['table']}")
            dataJson = {
                "success": True,
                "data": []
            }
            for dataUser in mysqlCursor.fetchall():
                dataJsonNew = {}
                num = 0
                for column in listColumns:
                    dataJsonNew.update({column: dataUser[num]})
                    num += 1
                dataJson["data"].append(dataJsonNew)
            if len(dataJson["data"]) == 0:
                dataJson["success"] = False
                return dataJson
            else:
                return dataJson
        except mysql.connector.errors.ProgrammingError:
            print(f"{prefix()} Unknown table '{arg['table']}'")
            sys.exit()
        except KeyError:
            print(f"{prefix()} Please select the table")
            sys.exit()
    except mysql.connector.errors.InterfaceError:
        print(f"{prefix()} Can't connect to server")
        sys.exit()
    except mysql.connector.errors.ProgrammingError:
        print(f"{prefix()} Unknown database: '{arg['database']}'")
        sys.exit()
    except KeyError:
        print(f"{prefix()} Please select the database")
        sys.exit()

def mysqlGETONE(**arg):
    try:
        mysqlConnect = mysql.connector.connect(
            host = mysqlAccount["host"],
            user = mysqlAccount["user"],
            passwd = mysqlAccount["pass"],
            database = arg["database"],
            port = mysqlAccount["port"]
        )
        try:
            listColumns = []
            mysqlCursor = mysqlConnect.cursor()
            mysqlCursor.execute(f"describe {arg['table']}")
            for column in mysqlCursor.fetchall():
                listColumns.append(column[0])
            try:
                mysqlCursor.execute(f"select * from {arg['table']} where {arg['key']}='{arg['value']}'")
                dataJson = {
                    "success": True,
                    "data": []
                }
                dataJsonNew = {}
                num = 0
                dataUser = mysqlCursor.fetchone()
                try:
                    for column in listColumns:
                        dataJsonNew.update({column: dataUser[num]})
                        num += 1
                    dataJson["data"].append(dataJsonNew)
                    if len(dataJson["data"]) == 0:
                        dataJson["success"] = False
                        return dataJson
                    else:
                        return dataJson
                except TypeError:
                    dataJson["success"] = False
                    return dataJson
            except KeyError:
                print(f"{prefix()} Please enter the key and value")
                sys.exit()
        except mysql.connector.errors.ProgrammingError:
                print(f"{prefix()} Unknown table '{arg['table']}'")
                sys.exit()
        except KeyError:
                print(f"{prefix()} Please select the table")
                sys.exit()
    except mysql.connector.errors.InterfaceError:
        print(f"{prefix()} Can't connect to server")
        sys.exit()
    except mysql.connector.errors.ProgrammingError:
        print(f"{prefix()} Unknown database: '{arg['database']}'")
        sys.exit()
    except KeyError:
        print(f"{prefix()} Please select the database")
        sys.exit()

def mysqlQUERY(**arg):
    try:
        mysqlConnect = mysql.connector.connect(
            host = mysqlAccount["host"],
            user = mysqlAccount["user"],
            passwd = mysqlAccount["pass"],
            port = mysqlAccount["port"]
        )
        try:
            mysqlCursor = mysqlConnect.cursor()
            mysqlCursor.execute(arg["command"])
            mysqlConnect.commit()
            return True
        except mysql.connector.errors.ProgrammingError:
            print(f"{prefix()} You have an error in your SQL syntax")
            sys.exit()
        except KeyError:
            print(f"{prefix()} Please enter the command")
            sys.exit()
    except mysql.connector.errors.InterfaceError:
        print(f"{prefix()} Can't connect to server")
        sys.exit()

def checkSession(**arg):
    try:
        dataUser = json.loads(
            base64.b64decode(
                open(f"{core.homeDirectory}/assets/session/{md5(arg['username'])}", "r").read()
            )
        )["password"]
        return {
            "status": "auto_login"
        }
    except KeyError:
        return {
            "status": "login"
        }

def vhacksRegister():
    time.sleep(2)
    os.system("clear")
    print("\t\033[1;30;47m [ R E G I S T E R - V H A C K S ] \033[0m\n")
    usernameNew = input("\033[1;37m[?] New Username: ")
    if usernameNew == "":
        print(f"\n{prefix()} Please enter the username you want to use")
    else:
        print(f"\n{prefix()} Checking username ...")
        time.sleep(random.randint(3, 5))
        if len(usernameNew) < 4:
            print(f"{prefix()} The username you entered is too short")
        else:
            if mysqlGETONE(database="vhacks", table="users", key="username", value=usernameNew)["success"]:
                print(f"{prefix()} Username is already in use")
            else:
                print(f"{prefix()} Currently creating your account ...")
                time.sleep(random.randint(3, 5))
                passwordNew = generate().password(random.randint(8, 12))
                rhostNew = generate().ipv4()
                platformNew = platform.system()
                dateCreateNew = ltime.now().strftime("%Y-%m-%d %H:%M:%S")
                if mysqlQUERY(command=f"insert into vhacks.users (username, password, rhost, platform, date_create) values ('{usernameNew}', '{hashlib.md5(passwordNew.encode('utf-8')).hexdigest()}', '{rhostNew}', '{platformNew}', '{dateCreateNew}')"):
                    mysqlQUERY(command=f"insert into password_saved.password (password_decrypt, password_encrypt) values ('{passwordNew}', '{hashlib.md5(passwordNew.encode('utf-8')).hexdigest()}')")
                    print(f"{prefix()} Your account has been successfully created\n")
                    if os.path.exists(f"{core.homeDirectory}/assets/session"):
                        pass
                    else:
                        os.mkdir(f"{core.homeDirectory}/assets/session")
                    if os.path.exists(f"{core.homeDirectory}/assets/account-saved"):
                        pass
                    else:
                        os.mkdir(f"{core.homeDirectory}/assets/account-saved")
                    if os.path.exists(f"{core.homeDirectory}/assets/data/folder-{md5(usernameNew)}"):
                        pass
                    else:
                        os.makedirs(f"{core.homeDirectory}/assets/data/folder-{md5(usernameNew)}/home")
                    open(f"{core.homeDirectory}/assets/session/{md5(usernameNew)}", "wb").write(
                        base64.b64encode(
                            str(
                                json.dumps({
                                    "username": usernameNew,
                                    "password": passwordNew
                                }, indent=4)
                            ).encode("utf-8")
                        )
                    )
                    open(f"{core.homeDirectory}/assets/account-saved/{md5(usernameNew)}", "w").write(
                        f"[*]     Username : {usernameNew}\n[*]     Password : {passwordNew} => {hashlib.md5(passwordNew.encode('utf-8')).hexdigest()}\n[*]        RHOST : {rhostNew}\n[*]     Platform : {platformNew}\n[*] Date created : {ltime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    )
                    print(open(f"{core.homeDirectory}/assets/account-saved/{md5(usernameNew)}", "r").read())
                    requests.post("http://localhost:8080", data={
                        "folder_name": f"folder-{md5(usernameNew)}",
                        "create_folder": "submit"
                    })
                    requests.post("http://localhost:8080", data={
                        "folder_name": f"folder-{md5(usernameNew)}/home",
                        "create_folder": "submit"
                    })
                    requests.post("http://localhost:8080", data={
                        "file_name": f"folder-{md5(usernameNew)}/home/your.log",
                        "file_data": f"{ltime.now().strftime('[%Y-%m-%d %H:%M:%S]')} Admin has prepared your account",
                        "create_file": "submit"
                    })
                    open(f"{core.homeDirectory}/assets/data/folder-{md5(usernameNew)}/home/your.log", "w").write(
                        f"{ltime.now().strftime('[%Y-%m-%d %H:%M:%S]')} Admin has prepared your account"
                    )
                    time.sleep(5)
                else:
                    print(f"{prefix()} Your account failed to create")

def vhacksLoading(**arg):
	spinner = ["|", "/", "-", "\\", " "]
	num_spinner = 0
	num = 0
	for i in range(arg["delay"]):
		if i == arg["delay"] - 1:
			num_spinner = 4
		sys.stdout.write(f"\r[*] {arg['message'][:num]+arg['message'][num:].capitalize()} ...{spinner[num_spinner]}")
		sys.stdout.write("\r")
		sys.stdout.flush()
		time.sleep(15./100)
		num_spinner += 1
		num += 1
		if num_spinner == 4:
			num_spinner = 0
		if num == len(arg["message"]):
			num = 0
	sys.stdout.write(f"\r[*] {arg['message']} ... ")
	time.sleep(2)
	os.system("clear")

def convert(uang):
	x = str(uang)
	if len(x) <= 3:
		return "$" + x
	else:
		a = x[:-3]
		b = x[-3:]
		return convert(a) + "." + b

def vhacksConsole(**arg):
    dataUser = mysqlGETONE(database="vhacks", table="users", key="username", value=arg["username"])["data"][0]
    os.chdir(f"{core.homeDirectory}/assets/data/folder-{md5(str(dataUser['username']))}/home")
    print(f"\033[1;37m[*] {arg['username']} ({dataUser['rhost']}) - {convert(dataUser['vhcoin'])} VHCOIN\n[*] Lv.{dataUser['firewall']} FIREWALL - Lv.{dataUser['sdk']} SDK - Lv.{dataUser['ip_spoofing']} IP-SPOOFING - Lv.{dataUser['scan']} SCAN\n")
    while True:
        try:
            dataUser = mysqlGETONE(database="vhacks", table="users", key="username", value=arg["username"])["data"][0]
            if checkSession(username=dataUser["username"])["status"] == "login":
                break
            elif os.path.exists(f"{core.homeDirectory}/assets/session/exit"):
                print(f"{prefix()} Bye Bye ^_^")
                os.remove(f"{core.homeDirectory}/assets/session/exit")
                sys.exit()
            else:
                home = os.getcwd
                prompt = input(f"{dataUser['username']}@{dataUser['connection']}: ({os.getcwd()[len(os.getcwd())-5:]}) #").split()
                try:
                    open(f"{core.homeDirectory}/assets/commands/{prompt[0]}.py")
                    open(f"{core.homeDirectory}/assets/data/folder-{md5(dataUser['username'])}/{md5(dataUser['username'])}", "wb").write(
                        base64.b64encode(
                            str(
                                json.dumps(
                                    dataUser,
                                    indent=4
                                )
                            ).encode("utf-8")
                        )
                    )
                    try:
                        os.system(f"python {core.homeDirectory}/assets/commands/{prompt[0]}.py {dataUser['username']} {prompt[1]} {core.homeDirectory}")
                    except IndexError:
                        os.system(f"python {core.homeDirectory}/assets/commands/{prompt[0]}.py {dataUser['username']} your.log {core.homeDirectory}")
                except IndexError:
                    pass
                except IOError:
                    print(f"{prefix()} Command not found '{prompt[0]}'")
        except IndexError:
            print(f"{prefix()} Log out of account")
            break

while True:
    time.sleep(2)
    os.system("clear")
    if os.path.exists(f"{core.homeDirectory}/assets/session"):
        num = 1
        print("\t\033[1;30;47m [ A C C O U N T S - V H A C K S ] \033[0m\n\033[1;37m")
        for account in os.listdir(f"{core.homeDirectory}/assets/session"):
            try:
                dataAccount = json.loads(
                    base64.b64decode(
                        open(f"{core.homeDirectory}/assets/session/{account}", "r").read()
                    )
                )
                if mysqlGETONE(database="vhacks", table="users", key="username", value=dataAccount["username"])["success"]:
                    print(f"[0{num}] {dataAccount['username']} => {account}")
                    num += 1
                else:
                    print(f"[0{num}] {dataAccount['username']} => {account} => \033[1;31mDeleted\033[1;37m")
                    if os.path.exists(f"{core.homeDirectory}/assets/session/{account}"):
                        os.remove(f"{core.homeDirectory}/assets/session/{account}")
                        shutil.rmtree(f"{core.homeDirectory}/assets/data/folder-{account}")
                    else:
                        pass
                    if os.path.exists(f"{core.homeDirectory}/assets/account-saved/{account}"):
                        os.remove(f"{core.homeDirectory}/assets/account-saved/{account}")
                    else:
                        pass
                    num += 1
            except KeyError:
                pass
        print("[98] Forgot password\n[99] Register")
        try:
            pil = int(input("\n[*] Select: "))
            if pil == 99:
                vhacksRegister()
            elif pil == 98:
                print(f"\n{prefix()} Coming soon")
            else:
                dataAccount = json.loads(
                    base64.b64decode(
                        open(core.homeDirectory+"/assets/session/"+os.listdir(f"{core.homeDirectory}/assets/session")[pil-1], "r").read()
                    )
                )
                print(f"\n{prefix()} Checking the session ...")
                time.sleep(random.randint(3, 5))
                if checkSession(username=dataAccount["username"])["status"] == "auto_login":
                    print("")
                    vhacksLoading(delay=random.randint(100, 500), message="Starting the vhacks console")
                    vhacksConsole(username=dataAccount["username"])
                else:
                    password = pwinput(prompt=f"{prefix()} {dataAccount['username']} Password: ", mask="*")
                    dataUser = mysqlGETONE(database="vhacks", table="users", key="username", value=dataAccount["username"])["data"][0]
                    if md5(password) == dataUser["password"]:
                        open(f"{core.homeDirectory}/assets/session/{md5(dataUser['username'])}", "wb").write(
                            base64.b64encode(
                                str(
                                    json.dumps({
                                        "username": dataUser["username"],
                                        "password": password
                                    }, indent=4)
                                ).encode("utf-8")
                            )
                        )
                        print(f"{prefix()} Signed in successfully\n")
                        time.sleep(random.randint(3, 5))
                        vhacksLoading(delay=random.randint(100, 500), message="Starting the vhacks console")
                        vhacksConsole(username=dataUser["username"])
                    else:
                        print(f"{prefix()} Incorrect password")
        except IndexError:
            print(f"{prefix()} Enter correctly")
        except ValueError:
            print(f"\n{prefix()} Please enter the number you chose")
    else:
        vhacksRegister()