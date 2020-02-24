# -*- coding: utf-8 -*-

import tkinter as tk
import os
from time import localtime, strftime
import etc.setting_Data as sd


class ses_data:
  
  data_Keys = [
      'store',
      'name',
      'phone',
      'core_port',
      'core_mac',
      ]
  ap_Keys = [
      'cable',
      'port',
      'mac',
      ]
  ###########
  widgets = {}          #Dict of widget pointers
  textboxes = {}        #Dict of text boxes pointers
  variables = {}        #Dict of StringVariables pointers
  output_Buffer = {}    #Buffer to store values/outputs to formatted textbox
  ###########
  
  num_of_aps = 0
  
  def __init__(self, root, num_of_aps):
    self.num_of_aps = num_of_aps
    
    self.data = sd.setting_Data()
    
    def create_Output_Buffer():
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
    self.reset_Variables()
    
  def create_Variables(self, root):
    pass
  def reset_Variables(self):
    self.variables = tmp = {}

    for key in self.data_Keys:
      var = tk.StringVar()
      
      if key == 'core_port':
        #var.set('183')
        tmp = {key: var}
      else:
        tmp = {key: var}
      
      self.variables.update(tmp)
    
    i= 0
    
    while i < self.num_of_aps:
      ap_name = 'ap_' + str(i+1)
      tmp = {}
      for key in self.ap_Keys:
        var = tk.StringVar()
        tmp_dict = {key:var}
        tmp.update(tmp_dict)
      
      tmp_dict = {ap_name: tmp}
      self.variables.update(tmp_dict)
      
      i+= 1
  
  def update_Output_Textbox(self, key, widget, ap_key = "",  *args):
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
      
    def format_Buffer(ap_key):
      widget_input = widget.get().strip()
      try:
        assert ap_key == ''    #Thows an AssertionError if the ap_key isn't empty (is created on an AP entry widget).
        #self.output_Buffer[key] = widget_input
        
        if widget_input != '':
            
          buffer = ''
          if key == 'store':
            buffer = 'S-' + widget_input
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
            
          self.output_Buffer[key] = buffer
        elif widget_input == '':          #If Entry widget is empty
          self.output_Buffer[key] = ''
          
            
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
      
    def output_Buffer():
      self.textboxes['output'].delete('1.0', tk.END)
      for line in self.output_Buffer:
        if self.output_Buffer[line] != '':
          try:
            assert not isinstance(self.output_Buffer[line], dict)
            tmp = self.output_Buffer[line]
            if line == 'store':
              self.textboxes['output'].insert(tk.END, tmp)
            elif line == 'core_mac':
              self.textboxes['output'].insert(tk.END, " "+tmp)
            else:
              self.textboxes['output'].insert(tk.END, "\n"+tmp)
          except AssertionError:
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
                
              for ap_value in self.output_Buffer[ap_name]:        #Adds to the buffer if any of the form fields are filled
                if self.output_Buffer[ap_name][ap_value] != '':                                        #Replace later with actual form input
                  if ap_value == 'port':
                    buffer+= self.output_Buffer[ap_name][ap_value]
                  elif ap_value == 'mac':
                    buffer+= self.output_Buffer[ap_name][ap_value]
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
          variables[var].set('')
        except AssertionError:      #checks for the AP's, as they're assigned as a dict
          i = 0
          while i < self.num_of_aps:
            ap_name = "ap_" + str(i+1)
            for field in variables[ap_name]:
              if not field == 'cable':
                variables[ap_name][field].set('')
            i+= 1
    def clear_Buffer():
      buffer = self.output_Buffer
      for line in buffer:
        try:
          assert not isinstance(buffer[line], dict)
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
  def assign_Widget_From_SES_Logger(self, key, widget, ap_key = ""):
    if ap_key == "":
      widget.config(textvariable = self.variables[key])
      tmp = {key:widget}      #not sure if this is needed, but it's nice ig.
      self.widgets.update(tmp)
    
      self.variables[key].trace('w', lambda *args: self.update_Output_Textbox(key, widget, "", *args))
    else:
      widget.config(textvariable = self.variables[ap_key][key])
      tmp = {ap_key:{key: widget}}
      self.widgets.update(tmp) 
    
      self.variables[ap_key][key].trace('w', lambda *args: self.update_Output_Textbox(key, widget, ap_key, *args))
  
  def assign_TextBox_From_SES_Logger(self, key, textbox):
    tmp = {key: textbox}
    self.textboxes.update(tmp)
    
    
    
    
    
    
    
    
    
    
    