# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import scrolledtext
from MenuBar import MenuBar
from time import localtime, strftime
from pyperclip import copy
import os

#https://likegeeks.com/python-gui-examples-tkinter-tutorial/
#https://effbot.org/tkinterbook/tkinter-application-windows.htm
#https://www.python-course.eu/tkinter_layout_management.php
#http://epydoc.sourceforge.net/stdlib/Tkinter.Variable-class.html
def nothing():
  pass

"""
Store: XXXX
Patch Panel Switch X
Core Port:XX MAC: XXXXXXXXXXXX
Patch Panel Switch X
Access Point 1: 2d931 Port: XX MAC: XXXXXXXXXXXX
Access Point 2: 2d932 Port: XX MAC: XXXXXXXXXXXX

Access Point 3: 2d933 Port: XX MAC: XXXXXXXXXXXX
Access Point 4: 2d934 Port: XX MAC: XXXXXXXXXXXX

Tech: XXX-XXX-XXXX

Check-out Code: 10123XXXX

"""
class SES_Logger:
  ##############################################################
  APP_TITLE = "SES-Call-Logger v.1"
  MIN_APP_WIDTH = 600
  MIN_APP_HEIGHT = 400  #420 for footer inclusion
  BANNER_SEPARATOR = 70

  employee_code = ""
  employee_initials = ""
  
  ##############################################################

  output_string = []
  
  def __init__(self, root):
    i = 0
    while i < 15:
      self.output_string.append("")
      i += 1
    
    self.root = root
    root.resizable(width = tk.FALSE, height = tk.FALSE)
    
    self.menu = MenuBar(root)

    self.dim = "{}x{}".format(self.MIN_APP_WIDTH, self.MIN_APP_HEIGHT)
    self.root.geometry(self.dim)
    self.root.title(self.APP_TITLE)
    self.root.wm_attributes("-topmost",1)
    
    try:
      self.initializeTheme()
      self.initializeTextVariables()
      self.create_Banner(root)
      self.create_CenterFrame(root)
      
    except Exception as e:
      """
      Check for any errors, mostly the TclError given when a color is nonexistent.
      """
      self.initializeTheme(True)
      self.create_Banner(root, 0, 0)
      self.create_CenterFrame(root)

      print(e)
      
  def initializeTheme(self, reset = False):
    try:
      assert reset == False
      theme = self.menu.return_Settings()['Theme']
      self.banner_color = theme['banner_color']
      self.bg_theme = theme['bg_theme']
      self.fg_theme = theme['fg_theme']
      self.button_bg = theme['button_bg']
      self.button_fg = theme['button_fg']
      self.button_active_bg = theme['button_active_bg']
      self.button_active_fg = theme['button_active_fg']
    except AssertionError:
      self.banner_color = '#3B4483'
      self.bg_theme = '#E1E1E1'
      self.fg_theme = 'black'
      self.button_bg = '#dedede'
      self.button_fg = 'black'
      self.button_active_bg = '#c9c9c9'
      self.button_active_fg = 'black'
      
    self.root.config(bg= self.bg_theme)
  def initializeTextVariables(self):
    self.var = {}
    
    store = tk.StringVar()
    name = tk.StringVar()
    phone = tk.StringVar()
    
    self.var = {
        'store':store,
        'name':name,
        'phone':phone
        
        }
    
  def create_Banner(self, root, col=0, row=0):
    """
    Creates the banner for the program.  Has various buttons, including clear and CP.
    """
      
    banner_Bar = tk.Frame(root, width = self.MIN_APP_WIDTH, height = 31, bg=self.banner_color)
    banner_Bar.grid_propagate(False)
    banner_Bar.grid(column= col, row= row, sticky= 'nsew')
    
    KDS_TS_Btn = tk.Button(banner_Bar, text="KDS Timestamp", command = self.KDS_Changer_TS, bg = self.button_bg, fg = self.button_fg, activebackground=self.button_active_bg, activeforeground=self.button_active_fg)
    KDS_TS_Btn.grid(column=0, row=0, padx=10)
    Comment_TS_Btn = tk.Button(banner_Bar, text = "Comment Timestamp", command = self.comment_TS, bg = self.button_bg, fg = self.button_fg, activebackground=self.button_active_bg, activeforeground=self.button_active_fg)
    Comment_TS_Btn.grid(column=1, row=0)
    seperator = tk.Frame(banner_Bar, width = 10)
    seperator.grid_propagate(False)
    seperator.grid(column = 2, padx=self.BANNER_SEPARATOR)
    
    clear_Button_Frame = tk.Frame(banner_Bar, bg = self.banner_color)
    clear_Button_Frame.grid(column=3, row = 0, padx=15, sticky='nsew')
    
    clear_only = tk.Button(clear_Button_Frame, text="Clear Only", command = nothing, bg='#ebdb34', fg='#0d0d0c', activebackground='#ccbe2d', activeforeground='#0d0d0c')
    clear_only.grid(column=0, row = 0, padx=18, sticky='E')
    clear_all = tk.Button(clear_Button_Frame, text="Clear & Log", command = nothing, bg='#C1392B', fg='#F8F8F8', activebackground='#a3382a', activeforeground='#F8F8F8')
    clear_all.grid(column=1, row = 0, padx=2, pady=3, sticky='E')
  def create_CenterFrame(self, root, col= 0, row= 1):
    center_Frame = tk.Frame(root, bg = self.bg_theme)
    center_Frame.grid(column= 0, row= row, sticky='nsew', padx= 3, pady= 5)
    
    self.create_SES_Form(center_Frame)
    
  def create_SES_Form(self, centerFrame):
    form_Master_Frame = tk.Frame(centerFrame, bg = self.bg_theme)
    form_Master_Frame.grid(column= 0, row= 0)
    
    caller_info = tk.Frame(form_Master_Frame, bg= self.bg_theme)
    core_and_panel= tk.Frame(form_Master_Frame)
    ap_1 = tk.Frame(form_Master_Frame)
    ap_2 = tk.Frame(form_Master_Frame)
    ap_3 = tk.Frame(form_Master_Frame)
    ap_4 = tk.Frame(form_Master_Frame)
    ap_5 = tk.Frame(form_Master_Frame)
    ap_6 = tk.Frame(form_Master_Frame)
    
    #List of frames for the AP section of the form.
    ap_List = [
        ap_1,
        ap_2,
        ap_3,
        ap_4,
        ap_5,
        ap_6,
        ]
    #List of every Frame & includes the ap_List.
    frame_List = [
        caller_info,
        core_and_panel,
        ap_List
        ]
    
    #Places each frame EXCEPT ap_List on the grid.  
    #ap_List needs to be iterated since it's essentially repeating itself.
    i= 0
    for frame in frame_List:
      if i < 2:
        frame.config(bg= self.bg_theme)
        frame.grid(column= 0, row= i, sticky= 'nsew')
      i+= 1
    
    
    #caller_info Frame#################################
    store_Label = tk.Label(caller_info, text= 'Store:')
    name_Label = tk.Label(caller_info, text= 'Name:')
    phone_Label = tk.Label(caller_info, text= 'Phone:')
    
    store = tk.Entry(caller_info, width=5, textvariable= self.var['store'])
    name = tk.Entry(caller_info, width=20, textvariable= self.var['name'])
    phone = tk.Entry(caller_info, width=16, textvariable= self.var['phone'])
    
    i= 0
    for label, entry in zip([store_Label, name_Label, phone_Label],[store, name, phone]):
      label.config(bg= self.bg_theme)
      label.grid(column=0, row= i, sticky= 'nw')
      
      #Editing colors for later
      #entry.config(bg= self.bg_theme)
      entry.grid(column=1, row= i, sticky= 'nw')
      i+= 1
    ####################################################
    
    

  def KDS_Changer_TS(self):
    #msg = "KDS Timestamp copied to clipboard"
    initials = self.menu.return_Settings()['User']['Initials']
    clipboard = initials + " " + strftime("%I:%M%p", localtime())
    copy(clipboard)
    
    #self.alterFooter(msg)
  def comment_TS(self):
    initials = self.menu.return_Settings()['User']['Initials']
    clipboard = strftime("%m/%d @%I:%M%p ("+initials+") ", localtime())
    copy(clipboard)    
if __name__ == "__main__":
  
  root = tk.Tk()
  ws_gui = SES_Logger(root)
  
  root.mainloop()