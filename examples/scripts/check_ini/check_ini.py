from alx.app import ALXapp
from alx.strings import date_subst
import os
import sys


sep = "------------------------------"
names = ['environment', 'loglevel', 'datafile', 'number',
         'list', 'date_format', 'pi']


def print_vars():
    print(sep)
    for k in names:
        print(f"app.{k} = {getattr(app, k)}")
    print(sep)


app = ALXapp("Demonstrate the ini file reading in dev mode")

print("Typically, you would create different installations of the code")
print("like in /opt/local/env, where env is dev, test or prod")
print("\nBut we can simulate it for this example")
print("\nconfiguration file:")
print()

with open(app.paths.config, 'r') as f:
    print(f.read())

print(sep)

print("app.paths:")
print(app.paths)
print(sep)

print("Currently running in dev mode")
print_vars()

print("Re-initialize app in test mode")
sys.argv = [sys.argv[0], '-e', 'test']

app = ALXapp("Demonstrate the ini file reading in test mode")
print_vars()

print("Re-initialize app in prod mode")
sys.argv = [sys.argv[0], '-e', 'prod']

app = ALXapp("Demonstrate the ini file reading in prod mode")
print_vars()

print("You can add other ini file sections as you need with")
print("whatever names you desire and use the included routines")
print("to add to new classes")





