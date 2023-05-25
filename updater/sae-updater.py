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
    SPECIAL = ('install', 'check')
    inblock = 0
    DATA = {}
    manager = ""
    pkg = ""
    i = 0
    while i<len(str):
        while not inblock and i < len(str):
            if re.match('[a-zA-Z0-9]', str[i]):
                manager += str[i]
            if str[i] == ' ':
                while str[i] != '{':
                    if i == len(str)-1:
                        log.info("Updater: parse: SyntaxError: Parser has hitted EOF and '{' was missing.")
                        return None
                    i+=1
                if manager in SPECIAL: DATA[manager] = {}
                else: DATA[manager] = []
                inblock = 1
                i += 1
                break
            if str[i] == '{':
                inblock = 1
                if manager in SPECIAL: DATA[manager] = {}
                else: DATA[manager] = []
                i += 1
                break
            i += 1
        while inblock:
            if i == len(str)-1:
                log.info("Updater: parse: SyntaxError: Parser has hitted EOF and '}' was missing.")
                return None
            if manager in SPECIAL and not re.match('[{}\n]+', str[i]):
                pkg += str[i]
            elif re.match("[a-zA-Z0-9-]",str[i]):
                pkg += str[i]
            if str[i] == '\n':
                if not pkg:
                    i+=1
                    continue
                if manager in SPECIAL:
                    p=pkg.strip().split()
                    DATA[manager][p[0][:-1]] = ' '.join(p[1:])
                else: DATA[manager].append(pkg.strip())
                pkg = ""
            if str[i] == '}':
                inblock = 0
                manager = ""
            i+=1
    return DATA

os.chdir(f"/home/darth/Programming/Erika/SAE/SAE-T")
subprocess.Popen(("git", "pull"), stdout=subprocess.PIPE)
F = open("../deps.saec")
DEPS = parse(F.read())
F.close()
if DEPS:
    for i in DEPS:
        if i in ('install', 'check'): continue
        if not os.path.exists(f'/usr/bin/{i}'):
            log.info(f"Updater: Error. Manager {i} does not exist on /usr/bin.")
            continue
        for e in DEPS[i]:
            # Check
            x=subprocess.Popen(DEPS["check"][i].replace('%', e).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if not x.wait(): continue
            # Install
            x=subprocess.Popen(DEPS["install"][i].replace('%', e).split())
            if x.wait():
                log.info(f"Updater: Failed to install {e} using {i}.")
            else:
                log.info(f"Updater: Installed {e} using {i}")
