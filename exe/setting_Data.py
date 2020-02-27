import os
from util import openJSON, writeJSON
import SES as ses

class setting_Data:
  """
  Module for creating the raw JSON file associated with the program.
  
  
  """
  path = "config\\config.json"
  JSON = {}
  User = {}
  #####################################
  reset = ses.SES() #Replace with any other module that creates a dict for settings.
  #####################################
  
  def __init__(self, file_stream = "config\\config.json"):

    if not os.path.exists('config'):
      os.mkdir('config')
    try:
      if not os.path.isfile(file_stream):
        self.resetSettings()   
      else:
        self.JSON = openJSON(file_stream)
        self.path = file_stream
    except Exception as e: print(e)

  
  def resetSettings(self):
    
    self.JSON = self.reset.returnMaster()
    writeJSON(self.JSON, self.path)
    
  def return_Specified_Setting(self, setting_Name):
    return self.JSON[setting_Name]
  def return_Raw_Settings(self):
    return self.JSON
  def return_List_Of_Keys(self):
    keys = []
    for setting in self.JSON:
      keys.append(setting)
      
    return keys
  def write_Specified_Setting(self, setting_Label, raw_Buffer):
    self.JSON[setting_Label] = raw_Buffer
    writeJSON(self.JSON, self.path)
  def write_All_Settings(self, raw_Buffer):
    writeJSON(raw_Buffer, self.path)
  def printJSON(self):
    print(self.JSON)
