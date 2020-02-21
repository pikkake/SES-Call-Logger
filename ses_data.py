# -*- coding: utf-8 -*-

import tkinter as tk


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
      
    def format_Buffer():
      widget_input = widget.get().strip()
      if ap_key != '':
        #Tests if the given input is from an AP frame.
        self.output_Buffer[key] = widget_input
        
      #iterates through every line of the output_Buffer to update the key-value.
      #It's easier to manage if in a loop
      for line in self.output_Buffer:
        try:
          assert not isinstance(self.output_Buffer[line], dict)    #Tests if the value from the given key is a dict.  Normally is false.
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
              buffer = 'Phone: ' + format_Phone(widget_input)
            elif key == 'core_port':
              buffer = 'Core Port: ' + widget_input 
            elif key == 'core_mac':
              buffer = 'MAC: ' + formatMAC(widget_input) 
            
            self.output_Buffer[key] = buffer
          elif widget_input == '':          #If Entry widget is empty
            self.output_Buffer[key] = ''
            break
            
        except AssertionError:              #If the value is a dict, it must be the APs.
          if ap_key != "":
            buffer = ''
            for line in self.output_Buffer[ap_key]:
                print(line)
                print(ap_key)
              
              
            #print("AP")
            pass
        except RuntimeError as e:
          print(e)
        finally:
          #print(self.output_Buffer)
          pass
      
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
            pass
        
      
    format_Buffer()
    output_Buffer()
    
  def assign_Widget_From_SES_Logger(self, key, widget, ap_key = ""):
    if ap_key == "":
      widget.config(textvariable = self.variables[key])
      tmp = {key:widget}
      self.widgets.update(tmp)
    
      self.variables[key].trace('w', lambda *args: self.update_Output_Textbox(key, widget, *args))
    else:
      widget.config(textvariable = self.variables[ap_key][key])
      tmp = {ap_key:{key: widget}}
      self.widgets.update(tmp)
    
      self.variables[ap_key][key].trace('w', lambda *args: self.update_Output_Textbox(key, widget, ap_key, *args))
  
  def assign_TextBox_From_SES_Logger(self, key, textbox):
    tmp = {key: textbox}
    self.textboxes.update(tmp)
    
    
    
    """
Store: XXXX
Patch Panel Switch X
Core Port:XX MAC: XXXXXXXXXXXX

A1: 2d931 Port: XX MAC: XXXXXXXXXXXX
A2: 2d932 Port: XX MAC: XXXXXXXXXXXX

A3: 2d933 Port: XX MAC: XXXXXXXXXXXX
A4: 2d934 Port: XX MAC: XXXXXXXXXXXX

Tech: XXX-XXX-XXXX

Check-out Code: 10123XXXX

"""
    
    
    
    
    
    
    
    
    
    