#!/usr/bin/python
#coding: utf-8

import os
import sys
import time
import json
import shutil
import random
import hashlib
import requests

from datetime import datetime
from faker import Faker
from pwinput import pwinput
from tabulate import tabulate

def md5(text):
  return hashlib.md5(text.encode("utf-8")).hexdigest()

