#!/usr/bin/python
#coding: utf-8

import os, sys, time, datetime, itertools, base64, hashlib, requests, json, pwinput, getpass, random, math

from datetime import datetime 
from faker import Faker as gen
from pwinput import pwinput 
from getpass import getpass
from tqdm import tqdm
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

url = "http://localhost:4040/api"
key = AESGCM(AESGCM.generate_key(bit_length=256))
nonce = os.urandom(12)
ver = "v1.0.3"

array = []
class auto(object):
	def __init__(self, options):
		self.options = sorted(options)
		
	def complete(self, text, state):
		if state == 0:
			if text:
				self.matches = [s for s in self.options if s and s.startswith(text)]
			else :
				self.matches = self.options[:]
		try:
			return self.matches[state]
		except IndexError:
			return None
def complete(array):
	completer = auto(array)
	readline.set_completer(completer.complete)
	readline.parse_and_bind("tab:complete")

class Apps:
    def __init__(self, url):
        self.url = url

    def getDataUsers(self):
        try:
            req = requests.get(
                f"{self.url}/get/users"
            ).json()
            return req
        except requests.exceptions.JSONDecodeError:
            return {
                "success": False,
                "msg": "Internal server error"
            }

    def getDataWithUsername(self, username):
        try:
            req = requests.get(
                f"{self.url}/get/users?username={username}"
            ).json()
            return req
        except requests.exceptions.JSONDecodeError:
            return {
                "success": False,
                "msg": "Internal server error"
            }

    def getDataWithIpAddress(self, ipAddress):
        try:
            req = requests.get(
                f"{self.url}/get/users?ipAddress={ipAddress}"
            ).json()
            return req
        except requests.exceptions.JSONDecodeError:
            return {
                "success": False,
                "msg": "Internal server error"
            }

    def getDataWithMacAddress(self, macAddress):
        try:
            req = requests.get(
                f"{self.url}/get/users?macAddress={macAddress}"
            ).json()
            return req
        except requests.exceptions.JSONDecodeError:
            return {
                "success": False,
                "msg": "Internal server error"
            }

    def addDataUsers(self, username, password, server):
        try:
            return requests.post(
                f"{self.url}/post/users",
                data = {
                    "username": username,
                    "password": password,
                    "otpCode": random.randint(100000000, 999999999),
                    "ipAddress": gen().ipv4(),
                    "macAddress": gen().mac_address(),
                    "vServer": server
                }
            ).json()
        except requests.exceptions.JSONDecodeError:
            return {
                "success": False,
                "msg": "Internal server error"
            }

    def updateDataUsers(self, **data):
        try:
            parts = []
            try:
                data["username"]
                for i in data:
                    parts.append(f"{i}='{data[i]}'")
                return requests.post(
                    f"{self.url}/post/custom",
                    data={
                        "query": f"UPDATE data_users SET {', '.join(parts)} WHERE username='{data['username']}'"
                    }
                ).json()
            except KeyError:
                try:
                    data["ipAddress"]
                    for i in data:
                        parts.append(f"{i}='{data[i]}'")
                    return requests.post(
                        f"{self.url}/post/custom",
                        data={
                            "query": f"UPDATE data_users SET {', '.join(parts)} WHERE username='{data['ipAddress']}'"
                        }
                    ).json()
                except KeyError:
                    return {
                        "success": False,
                        "msg": "Invalid data"
                    }
        except requests.exceptions.JSONDecodeError:
            return {
                "success": False,
                "msg": "Internal server error"
            }

    def updateDataServer(self, **data):
        try:
            parts = []
            try:
                data["name"]
                for i in data:
                    parts.append(f"{i}='{data[i]}'")
                return requests.post(
                    f"{self.url}/post/custom",
                    data={
                        "query": f"UPDATE data_servers SET {', '.join(parts)} WHERE name='{data['name']}'"
                    }
                ).json()
            except KeyError:
                return {
                    "success": False,
                    "msg": "Please enter the name of server"
                }
        except requests.exceptions.JSONDecodeError:
            return {
                "success": False,
                "msg": "Internal server error"
            }

    def getDataServer(self, **data):
        try:
            data["name"]
            req = requests.get(
                f"{self.url}/get/servers?name={data['name']}"
            ).json()
            return req
        except requests.exceptions.JSONDecodeError:
            return {
                "success": False,
                "msg": "Internal server error"
            }
        except KeyError:
            return requests.get(
                f"{self.url}/get/servers"
            ).json()


class Console:
    def log(prefix, msg):
        if prefix == "!":
            prefix = f"\033[1;33m[{prefix}]\033[1;37m"
        elif prefix == "-":
            prefix = f"\033[1;34m[{prefix}]\033[1;37m"
        elif prefix == "!!":
            prefix = f"\033[1;31m[{prefix}]\033[1;37m"
        elif prefix == "+":
            prefix = f"\033[1;32m[{prefix}]\033[1;37m"
        else:
            prefix = f"\033[1;37m[{prefix}]"
        print(f"{prefix} {msg}")
        time.sleep(2)

    def download(file, size, msg):
        for i in tqdm(range(int(size)), desc=f"{msg} {file}", unit="b", unit_scale=True, unit_divisor=1024):
            time.sleep(0.000000000000000000001)
        time.sleep(2)

    def loading(msg):
        spinner = ["\\", "|", "/", "-"]
        s = 0
        m = 0
        for i in range(50):
            sys.stdout.write(f"\r\033[1;34m[*] \033[1;37m{msg[:m]}{msg[m:].capitalize()} ...{spinner[s]}")
            sys.stdout.flush()
            time.sleep(0.2)
            m += 1
            s += 1
            if s == 3:
                s = 0
            if m == len(msg):
                m = 0
        sys.stdout.write(f"\r\033[1;34m[*] \033[1;37m{msg} ... ")
        print()
        time.sleep(2)

class System:
    def __init__(self, file):
        self.file = file

    def loadData(self, types):
        return key.decrypt(
            nonce,
            open(self.file, "rb").read(),
            str(types).encode()
        )

    def convertBytes(size, precision=1):
        if size == 0:
            return "0B"
        abbrevs = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size * 1024 * 1024, 1024)))
        return f"{size * 1024 * 1024 / (1024 ** i):.{precision}f}{abbrevs[i]}"
