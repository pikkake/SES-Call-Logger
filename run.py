from util import strip_input, clear
from time import localtime, strftime
from pyperclip import copy

INITIAL = ""
RELEASE_CODE = ""
storeNum = ""
copypasta = {
    "S-":"",
    "Name" :  "",
    "phone" : "",
    "WS" : "",
    "Old" : "",
    "New" : ""
    }
tmpList = [
    {"WS":"", "Old":"","New":""}
    
    ]
formattedString = ""
ex = ['exit','q','quit']
def releaseCode(empl_num = RELEASE_CODE):
  if storeNum == "":
    print("")
  else:
    print(" Release Code: " + empl_num + strftime("%m%d", localtime()) + storeNum)
    
def KDS_Changer_TS(init = INITIAL):
  clipboard = init + " " + strftime("%I:%M%p", localtime())
  copy(clipboard)
def comment_TS(init = INITIAL):
  clipboard = strftime("%m/%d @%I:%M%p ("+init+") ", localtime())
  copy(clipboard)
def setStoreNum(stdin):
  global storeNum
  global copypasta
  storeNum = stdin
  copypasta["S-"] = storeNum
def setCopyPasta(args):
  global copypasta
  try:
    argument = args[0]
    value = args[1]
    for key in copypasta:
      if key.lower() == argument.lower():
        if key == "WS":
          copypasta[key] = value.upper()
        elif key == "Old" or key == "New":
          copypasta[key] = splitMAC(value.upper())
        elif key == "Name":
          try: 
            value += " " + args[2]
            copypasta[key] = value.title()
          except:
            copypasta[key] = value.title()
        elif key == "phone":
          try:
            if len(value) == 10:
              s = value[:3] + "-" + value[3:6]+"-"+value[6:]
              copypasta[key] = s
            elif len(value) == 12:
              s = value[2:5] + "-" + value[5:8]+"-"+value[8:]
              copypasta[key] = s
            elif value == "store":
              copypasta[key] = "- Called From Store"
          except:
            pass
  except:
    pass
def printCopyPasta():
  
  print("\n\n S-"+copypasta["S-"])
  print(" Name: "+copypasta["Name"]+"\n Phone: "+copypasta["phone"])
  print(" WS: "+copypasta["WS"])
  print(" Old: "+copypasta["Old"]+"\n" + " New: " + copypasta["New"]+"\n")
  
def setPastaToClipboard():
   clip = "S-"+copypasta["S-"]
   clip += "\nName: "+copypasta["Name"]+"\nPhone: "+copypasta["phone"]
   clip += "\nWS: "+copypasta["WS"]
   clip += "\nOld: "+copypasta["Old"]+"\n" + "New: " + copypasta["New"]
   copy(clip)
def clearDict():
  global storeNum
  global copypasta
  copypasta = {
    "S-":"",
    "Name" :  "",
    "phone" : "",
    "WS" : "",
    "Old" : "",
    "New" : ""
    }
  storeNum = ""
def splitMAC(mac):
  try:
    split_mac = mac.split(":")
    mac = ""
    for i in split_mac:
      mac += i
    return mac
  except:
    return mac
if __name__ == "__main__":
  
  while True:
    clear()
    print("\n Store Number: " + storeNum)
    releaseCode()
    printCopyPasta()
    
    try:
      args = []
      stdin = strip_input("\n>> ")
      args = stdin.split()
    except IndexError:
      args.appent(stdin)    
    except EOFError:
      break
    
    try:
      if stdin.lower() in ex:
        break
      elif args[0] == "store" or args[0] == 's':
        setStoreNum(args[1])
      elif args[0] == "clear":
        clearDict()
      elif args[0] == "copy":
        setPastaToClipboard()
      elif args[0] == "ts":
        KDS_Changer_TS()
      elif args[0] == "comment":
        comment_TS()
      else:
        setCopyPasta(args)
    except IndexError:
      continue