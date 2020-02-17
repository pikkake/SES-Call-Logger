import sys, json
from os import system, name, mkdir, makedirs
from datetime import datetime

def fetchPythonVersion(action):
  tmp = sys.version.split(' ')
  tmp = tmp[0].split('.')
  tmp = tmp[0]+ '.' + tmp[1]
    
  if action == "list":
    print(sys.version)
  elif action == "num":
    return float(tmp)
    
def clear():
  if name == 'nt': 
    _ = system('cls') 
  
  else: 
    _ = system('clear')  
def closePy():
  if name == 'nt': 
    _ = system('exit()') 
  
  else: 
    _ = system('exit()') 
        
def strip_input(inputMsg):
  """
    Runs a test for the version of python, then runs the input function for
    its respective version.
  """
  if fetchPythonVersion("num") < 3:
    stdin = raw_input(inputMsg).strip()
  else:
    stdin = input(inputMsg).strip()
  return stdin

def openJSON(file_path, perms = 'r'):
  with open(file_path, perms) as json_file:
    file = json.loads(json_file.read())
  return file
def writeJSON(buffer, file_path, perms = 'w'):
  with open(file_path, perms) as json_file:
    json_file.write(json.dumps(buffer))
def createDirectory(path):
  try:
    mkdir(path)
  except OSError:
    print("An error has occurred...")
  