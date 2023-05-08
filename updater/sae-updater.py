# Updater script for SAE

import os
import re
import subprocess
import logging
from systemd.journal import JournalHandler
log = logging.getLogger(__name__)
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

def parse(str):
    inblock = 0
    DATA = {}
    manager = ""
    pkg = ""
    i = 0
    while i<len(str):
        while not inblock and i < len(str):
            if re.match('[a-zA-Z]', str[i]):
                manager += str[i]
            if str[i] == ' ':
                while str[i] != '{':
                    if i == len(str)-1:
                        log.info("Updater: parse: SyntaxError: Parser has hitted EOF and '{' was missing.")
                        return None
                    i+=1
                DATA[manager] = []
                inblock = 1
                break
            if str[i] == '{':
                inblock = 1
                DATA[manager] = []
                break
            i += 1
        while inblock:
            if i == len(str)-1:
                log.info("Updater: parse: SyntaxError: Parser has hitted EOF and '}' was missing.")
                return None
            if re.match("[a-zA-Z]",str[i]):
                pkg += str[i]
            if str[i] == '\n':
                if not pkg:
                    i+=1
                    continue
                DATA[manager].append(pkg)
                pkg = ""
            if str[i] == '}':
                inblock = 0
                manager = ""
            i+=1
    return DATA

os.chdir(f"/home/pupet/SAE-T")
subprocess.Popen(("git", "pull"), stdout=subprocess.PIPE)
F = open("deps.saec")
DEPS = parse(F.read())
if DEPS:
    for i in DEPS:
        if not os.path.exists(i):
            log.info(f"Updater: Error. Manager {i} does not exist on /usr/bin.")
            continue
        for e in DEPS[i]:
            x=subprocess.Popen((e, 'install', '--yes', e), stdout=subprocess.PIPE)
            if x.wait():
                log.info(f"Updater: Failed to install {e} using {i}.")

F.close()

