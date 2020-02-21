# -*- coding: utf-8 -*-

import tkinter as tk
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
  widgets = {}
  variables = {}
  num_of_aps = 0
  
  def __init__(self, root, num_of_aps):
    self.num_of_aps = num_of_aps
    
    self.reset_Variables()  
    
    
    
  
  def create_Variables(self, root):
    pass
  def reset_Variables(self):
    self.variables = tmp = {}

    for key in self.data_Keys:
      var = tk.StringVar()
      
      if key == 'core_port':
        var.set('183')
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
  
  def _show_value(self, key, widget, *args):
    print(widget.get())

  def var_listen(self, *args):
    """
    Use the input of the above and below functions to control what happens next.  
    MUST bind them initially in ses_logger
    """
    print(args)
    self._show_value()
    pass
  def assign_Widget_From_SES_Logger(self, key, widget):
    widget.config(textvariable = self.variables[key])
    tmp = {'key':widget}
    self.widgets.update(tmp)
    
    self.variables[key].trace('w', lambda *args: self._show_value(key, widget, *args))

    pass
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    