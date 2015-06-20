#!/usr/bin/env python3
import sys
from os import system, path
import subprocess

source = sys.argv[1]
result = sys.argv[2]

print('Compiling %s to %s' % (source, result))

ext = path.splitext(source)[1]

if ext == '.pas':
    failed = False
    try:
        logs = subprocess.check_output('fpc %s -o%s' % (source, result), stderr=subprocess.STDOUT, shell=True)
        system('rm %s.o' % result)
    except subprocess.CalledProcessError as E:
        logs = E.output
        failed = True
    print(logs.decode())
    exit(1 if failed else 0)
elif ext == '.cpp':
    failed = False
    try:
        logs = subprocess.check_output('g++ %s -o%s' % (source, result), stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as E:
        logs = E.output
        failed = True
    print(logs.decode())
    exit(1 if failed else 0)
elif ext == '.py':
    system('echo "#!/usr/bin/env python3" > %s' % result)
    system('cat %s >> %s' % (source, result))
    failed = False
    try:
        logs = subprocess.check_output('python3 -m py_compile %s' % result, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as E:
        logs = E.output
        failed = True
    if failed:
        system('rm %s' % result)
        print(logs.decode())
        exit(1)
    system('chmod +x %s' % result)
    print(logs.decode())
    exit()
else:
    print('Unknown extention: %s' % ext)
    exit(1)
