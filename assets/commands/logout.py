#!/usr/bin/python
#coding: utf-8

import argparse, hashlib, base64, json

parse = argparse.ArgumentParser()
parse.add_argument("username")
parse.add_argument("file")
parse.add_argument("homedir")

args = parse.parse_args()

open(f"{args.homedir}/assets/session/{hashlib.md5(str(args.username).encode('utf-8')).hexdigest()}", "wb").write(
    base64.b64encode(
        str(
            json.dumps({
                "username": args.username
            }, indent=4)
        ).encode("utf-8")
    )
)