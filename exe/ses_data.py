# -*- coding: utf-8 -*-

import tkinter as tk
from pyperclip import copy
from collections import OrderedDict
import os
from time import localtime, strftime
import setting_Data as sd


class ses_data:
  
  data_Keys = [
      'store',
      'name',
      'phone',
      'core_port',
      'core_mac',
      'core_Room',
      'core_Check',
      'release'
      ]
  ap_Keys = [
      'cable',
      'port',
      'mac',
      'check'
      ]
  ###########
  widgets = {}          #Dict of widget pointers
  textboxes = {}        #Dict of text boxes pointers
  variables = {}        #Dict of StringVariables pointers
  output_Buffer = {}    #Buffer to store values/outputs to formatted textbox
  ###########
  
  num_of_aps = 0
  
  def __init__(self, root, num_of_aps, menu):
    self.num_of_aps = num_of_aps
    self.data = sd.setting_Data()
    self.menu = menu
    
    def create_Output_Buffer():
      # Initializes the initial output buffer
      for key in self.data_Keys:
        tmp = {key: ''}
        self.output_Buffer.update(tmp)
      i= 0
      while i < self.num_of_aps:
        ap_name = 'ap_' + str(i+1)
        tmp = {}
        for key in self.ap_Keys:
          tmp_dict = {key:''}
          tmp.update(tmp_dict)
        
        tmp_dict = {ap_name: tmp}
        self.output_Buffer.update(tmp_dict)
        
        i+=1
    create_Output_Buffer()
    self.create_Variables()
    
  def create_Variables(self):
    self.variables = tmp = {}

    for key in self.data_Keys:
      var = tk.StringVar()
      
      if key == 'core_port':
        tmp = {key: var}
      elif key == 'core_Room':
        var.set("IDF")
        tmp = {key:var}
      else:
        tmp = {key: var}
      
      self.variables.update(tmp)
    
    i= 0
    
    while i < self.num_of_aps:
      ap_name = 'ap_' + str(i+1)
      tmp = {}
      for key in self.ap_Keys:
        if key == 'check':
          var = tk.IntVar()
        else:
          var = tk.StringVar()
        tmp_dict = {key:var}
        tmp.update(tmp_dict)
      
      tmp_dict = {ap_name: tmp}
      self.variables.update(tmp_dict)
      
      i+= 1
  
  def update_Output_Textbox(self, key, widget, ap_key = "", cable = False, *args):
    
    ###Formatting Functions ######################################
    def formatMAC(mac):
      try:
        split_mac = mac.split(":")
        mac = ""
        for i in split_mac:
          mac += i
        return mac
      except:
        return mac    

    def format_Phone(phone):
      try:
        if len(phone) == 10:
          phone = phone[:3] + "-" + phone[3:6]+"-"+phone[6:]
          return phone
        elif len(phone) == 12:
          if '-' not in phone:
            phone = phone[2:5] + "-" + phone[5:8]+"-"+phone[8:]
            return phone
          else:
            return phone
        elif phone == "store":
          phone = "- Called From Store"
          return phone    
        else:
          return phone
      except:
        return phone   
    def format_Store(store):
      tmp = ''
      if len(store) != 0:
        if len(store) == 1:
          tmp = "000" + store
        elif len(store) == 2:
          tmp = "00" + store
        elif len(store) == 3:
          tmp = "0" + store
        else:
          tmp = store
      
      return tmp
    def format_Release():
      release = str(self.menu.return_Settings()['User']['Emp_Num'])
      release += strftime("%m%d", localtime())
      
      store = self.variables['store'].get()
      tmp = ''
      if len(store) != 0:
        if len(store) == 1:
          tmp = "000" + store
        elif len(store) == 2:
          tmp = "00" + store
        elif len(store) == 3:
          tmp = "0" + store
        else:
          tmp = store
      
      release += tmp
      
      return release
      
    def format_Buffer(ap_key):
      
      # Formats the actual buffer that holds the info to be thrown into the textboxes
      try:
        widget_input = widget.get().strip()
        assert ap_key == ''    #Thows an AssertionError if the ap_key isn't empty (is created on an AP entry widget).
        
        if widget_input != '':
            
          buffer = ''
          if key == 'store':
            tmp = format_Release()
            self.variables['release'].set(tmp)
            buffer = 'S-' + format_Store(widget_input)
          elif key == 'name':
            tmp = widget_input.split(" ")
            if tmp[0].upper() == 'MOD':
              buffer = 'Name: MOD'
              i= 1
              while i < len(tmp):
                buffer+= " " + tmp[i].title()
                i+= 1
            else:
              buffer = 'Name: '+ widget_input.title()
          elif key == 'phone':
            buffer = 'Phone: ' + format_Phone(widget_input) + "\n"
          elif key == 'core_port':
            buffer = 'Core Port: ' + widget_input 
          elif key == 'core_mac':
            buffer = 'MAC: ' + formatMAC(widget_input).upper() 
          elif key == 'release':
            pass
          self.output_Buffer[key] = buffer
        elif widget_input == '':          #If Entry widget is empty
          self.output_Buffer[key] = ''
          if key == 'store':
            self.variables['release'].set('')
            self.otuput_Buffer[key] = ''
          
            
      except AssertionError:              #If the value is a dict, it must be the APs.
        if widget_input != '':
          buffer = ''
          if key == 'cable':
            buffer = " " + widget_input
          elif key == 'port':
            buffer = " Port: " + widget_input
          elif key == 'mac':
            buffer = " MAC: " + formatMAC(widget_input).upper()
          self.output_Buffer[ap_key][key] = buffer
        elif widget_input == '':
          self.output_Buffer[ap_key][key] = ''
      except AttributeError as check:     #If the value is from a Checkbox widget
        
        pass
    ################################################################
    
    
    def output_Buffer():
    
      self.textboxes['output'].delete('1.0', tk.END)
    
      for line in self.data_Keys:
        if self.output_Buffer[line] != '' and line != 'release':
          assert not isinstance(self.output_Buffer[line], dict)
          tmp = self.output_Buffer[line]
          if line == 'store':
            self.textboxes['output'].insert(tk.END, tmp)
          elif line == 'core_port':
            self.textboxes['output'].insert(tk.END, "\n"+tmp)  
          elif line == 'core_mac':
            self.textboxes['output'].insert(tk.END, " "+tmp)  
          elif line != 'core_Room':
            self.textboxes['output'].insert(tk.END, "\n"+tmp)

      for line in self.ap_Keys:
        i = 0
        buffer = ''
        while i < self.num_of_aps:
          ap_name = 'ap_' + str(i+1)
          ap_form_input = False
              
          for form_field in self.output_Buffer[ap_name]:      #boolean to check if any of the form fields are filled
            if self.output_Buffer[ap_name][form_field] != '':
              ap_form_input = True
                  
          if ap_form_input:                                   #Lists the name of the AP and its associated cable identifier if any form is filled for the AP.
            buffer += "\nAP-"+str(i+1) + " "
            buffer += self.variables[ap_name]['cable'].get().strip()
                

          buffer+= self.output_Buffer[ap_name]['port'] + " "
          buffer+= self.output_Buffer[ap_name]['mac'] 
          i+= 1
        self.textboxes['output'].insert(tk.END, buffer)
        break     #break from the for loop created before the assertion.
    
    format_Buffer(ap_key)
    output_Buffer()
    
  def clear_All_Fields(self):
    def clear_Widgets():
      variables = self.variables
      for var in variables:
        try:
          assert not isinstance(variables[var], dict)
          if var == 'core_Check':
            variables[var].set(0)
          elif var == 'core_Room':
            variables[var].set("IDF")
          else:
            variables[var].set('')
          
        except AssertionError:      #checks for the AP's, as they're assigned as a dict
          i = 0
          while i < self.num_of_aps:
            ap_name = "ap_" + str(i+1)
            for field in variables[ap_name]:
              if not field == 'cable':
                if field == 'check':
                  variables[ap_name][field].set(0)
                else: 
                  variables[ap_name][field].set('')
                
            i+= 1
    def clear_Buffer():
      buffer = self.output_Buffer
      for line in buffer:
        try:
          assert not isinstance(buffer[line], dict)
          if line == 'core_Room':
            buffer[line] = 'IDF'
          else:
            buffer[line] = ''
        except AssertionError:
          i = 0
          while i < self.num_of_aps:
            ap_name = "ap_" + str(i+1)
            for field in buffer[ap_name]:
              buffer[ap_name][field] = ''
            i+= 1
      self.output_Buffer = buffer
    def clear_Textboxes():
      for textbox in self.textboxes:
        self.textboxes[textbox].delete('1.0', tk.END)
        
    clear_Widgets()
    clear_Buffer()
    clear_Textboxes()
    
  def log_Buffer(self):
    """
    First checks if either of the textboxes are occupied; if any are, it begins creating their respective text buffers.
    If only one is occupied, the rest are given a blank statement to print to the log.
    
    """
    
    note_Buffer = 'Notes:'
    call_Buffer = 'Call Info:'
    log_Ext = self.data.return_Specified_Setting('User')['file_Ext']
    def write_File(note_Buffer, call_Buffer):
      buffer = strftime("@%I:%M:%S %p:",localtime())
      if not os.path.exists('logs'):
        os.mkdir('logs')
      
      path = "logs\\" + strftime("20%y", localtime())
      if not os.path.exists(path):
        os.mkdir(path)
      timestamp = strftime("20%y-%m-%d." + log_Ext, localtime())
      path+= "\\"+timestamp
       
      with open(path, 'a+') as f:
        buffer += "\n# " + call_Buffer + "\n# " + note_Buffer + "\n\n"
        f.write(buffer)
        
    def check_Output():
      #Checks if any of the entry fields are filled with text.
      textbox_is_occupied = False
      for textbox in self.textboxes:
        if len(self.textboxes[textbox].get('1.0',tk.END)) > 1:
          textbox_is_occupied = True
      return textbox_is_occupied
      
    def parse_Notes(note_Buffer):
      if len(self.textboxes['notes'].get('1.0',tk.END)) > 1:
        buffer = self.textboxes['notes'].get('1.0',tk.END).strip().split("\n")
        for line in buffer:
          note_Buffer+= "\n\t" + line.strip()
      else:
        note_Buffer += "\n\tNo notes taken."
      return note_Buffer
    
    def parse_Call_Info(call_Buffer):
      if len(self.textboxes['output'].get('1.0',tk.END)) > 1:
        buffer = self.textboxes['output'].get('1.0',tk.END).strip().split("\n")
        for line in buffer:
          call_Buffer+= "\n\t" + line.strip()
      else:
        call_Buffer += "\n\tNo caller info taken."
      return call_Buffer

    if check_Output():
      note_Buffer = parse_Notes(note_Buffer)
      call_Buffer = parse_Call_Info(call_Buffer)
      write_File(note_Buffer, call_Buffer)
    
    
  def clear_And_Log(self):
    self.log_Buffer()
    self.clear_All_Fields()
  def copy_Release(self):
    code = self.variables['release'].get()
    if len(code) > 0:
      copy(code)
  def assign_Widget_From_SES_Logger(self, key, widget, ap_key = ""):
    if key == 'core_Room':
      widget.config(textvariable = self.variables[key])
      self.variables[key].trace('w', lambda *args: self.combobox_Update(widget, *args))
    elif ap_key == "":
      widget.config(textvariable = self.variables[key])
    
      self.variables[key].trace('w', lambda *args: self.update_Output_Textbox(key, widget, "", *args))
    else:
      #widget.config(textvariable = self.variables[ap_key][key])
      tmp = {ap_key:{key: widget}}
      self.widgets.update(tmp) 
      
      if key == 'cable':  #Don't auto update right away, it's easier this way :s
        pass
      else:
        self.variables[ap_key][key].trace('w', lambda *args: self.update_Output_Textbox(key, widget, ap_key, *args))
  
  def assign_TextBox_From_SES_Logger(self, key, textbox):
    tmp = {key: textbox}
    self.textboxes.update(tmp)
  def combobox_Update(self, widget, *args):
    
    network_Room = widget.get()
    cable_Suffix = ''
    if network_Room == 'IDF':
      cable_Suffix = '2d93'
    elif network_Room == 'MDF':
      cable_Suffix = '1d93'
    
    def updateCableVariables():
      
      i = 0
      while i < self.num_of_aps:
        ap = 'ap_'
        ap += str(i+1)
        self.variables[ap]['cable'].set(cable_Suffix + str(i+1))
        
        i+=1
    updateCableVariables()
  def debug(self):
    
    
    pass
    
    
    
    
    
    
    
    
    