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


class wsRefresh:
  ##############################################################
  APP_TITLE = "SES-Call-Logger v.1"
  MIN_APP_WIDTH = 600
  MIN_APP_HEIGHT = 400  #420 for footer inclusion
  banner_color = '#3B4483 '
  bg_theme = '#E1E1E1'
  fg_theme = 'black'
  button_bg = '#dedede'
  button_fg = 'black'
  button_active_bg = '#c9c9c9'
  button_active_fg = 'black'
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
    self.config = self.menu.return_Settings()
    self.employee_initials = self.config['User']['Initials']
    self.employee_code = self.config['User']['Emp_Num']
    
    root.resizable(width = tk.FALSE, height = tk.FALSE)

    



    self.dim = "{}x{}".format(self.MIN_APP_WIDTH, self.MIN_APP_HEIGHT)
    self.root.geometry(self.dim)
    self.root.title(self.APP_TITLE)
    self.root.wm_attributes("-topmost",1)
    
    self.WS_refresh_buttonBar = Frame(root, width = 600, height = 31, bg=self.banner_color)
    #Allows the frame to expand to the set width and height
    self.WS_refresh_buttonBar.grid_propagate(False)
    
    self.WS_Center = Frame(root, bg = self.bg_theme)
    self.WS_refresh_buttonBar.grid(sticky=E+W)
    self.WS_Center.grid(row=1, sticky='nsew')
    
    self.WS_refresh_form = Frame(self.WS_Center, bg = self.bg_theme)
    self.WS_refresh_textarea = Frame(self.WS_Center, bg = self.bg_theme)
    self.WS_refresh_form.grid(column=0, row=0,padx = 5, pady = 10, sticky ='NW')
    self.WS_refresh_textarea.grid(column=1, row = 0, padx=15, pady=10, sticky='NW')
  
    self.KDS_TS_Btn = Button(self.WS_refresh_buttonBar, text="KDS Timestamp", command = nothing, bg = self.button_bg, fg = self.button_fg, activebackground=self.button_active_bg, activeforeground=self.button_active_fg)
    self.KDS_TS_Btn.grid(column=0, row=0, padx=10)
    self.Comment_TS_Btn = Button(self.WS_refresh_buttonBar, text = "Comment Timestamp", command = nothing, bg = self.button_bg, fg = self.button_fg, activebackground=self.button_active_bg, activeforeground=self.button_active_fg)
    self.Comment_TS_Btn.grid(column=1, row=0)
    seperator = Frame(self.WS_refresh_buttonBar, width = 10)
    seperator.grid_propagate(False)
    seperator.grid(column = 2, padx=23)
    
    self.clearFrame = Frame(self.WS_refresh_buttonBar, bg = self.banner_color)
    self.clearFrame.grid(column=3, row = 0, padx=15, sticky='nsew')
    
    self.clear_all = Button(self.clearFrame, text="Clear Only", command = nothing, bg='#ebdb34', fg='#0d0d0c', activebackground='#ccbe2d', activeforeground='#0d0d0c')
    self.clear_all.grid(column=0, row = 0, padx=18, sticky='E')
    self.clear_all = Button(self.clearFrame, text="Clear & Log", command = nothing, bg='#C1392B', fg='#F8F8F8', activebackground='#a3382a', activeforeground='#F8F8F8')
    self.clear_all.grid(column=1, row = 0, padx=2, pady=3, sticky='E')
    


if __name__ == "__main__":
  
  root = Tk()
  ws_gui = wsRefresh(root)
  
  root.mainloop()