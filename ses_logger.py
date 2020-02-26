# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import scrolledtext
import ses_data as ses
from MenuBar import MenuBar
from time import localtime, strftime
from pyperclip import copy

#https://likegeeks.com/python-gui-examples-tkinter-tutorial/
#https://effbot.org/tkinterbook/tkinter-application-windows.htm
#https://www.python-course.eu/tkinter_layout_management.php
#http://epydoc.sourceforge.net/stdlib/Tkinter.Variable-class.html
def nothing():
  pass

class SES_Logger:
  ##############################################################
  APP_TITLE = "SES Call Logger v0.7"
  MIN_APP_WIDTH = 600   #600
  MIN_APP_HEIGHT = 450  #450
  BANNER_SEPARATOR = 70
  NUM_OF_APS = 4
  
  VERTICAL_SCROLL_FRAME_HEIGHT = 340      #340

  
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
    self.vars = ses.ses_data(root, self.NUM_OF_APS)
    
    self.dim = "{}x{}".format(self.MIN_APP_WIDTH, self.MIN_APP_HEIGHT)
    self.root.geometry(self.dim)
    self.root.title(self.APP_TITLE)
    self.root.wm_attributes("-topmost",1)
    
    try:
      self.initializeFrames()
      
    except Exception as e:
      """
      Check for any errors, mostly the TclError given when a color is nonexistent.
      """
      self.initializeFrames(True)

      print(e)
      
  def initializeTheme(self, reset = False):
    
    try:
      assert reset == False
      theme = self.menu.return_Settings()['Theme']
      self.banner_color = theme['banner_color']
      self.bg_theme = theme['bg_theme']
      self.active_bg_theme = theme['bg_theme']
      self.fg_theme = theme['fg_theme']
      self.button_bg = theme['button_bg']
      self.button_fg = theme['button_fg']
      self.button_active_bg = theme['button_active_bg']
      self.button_active_fg = theme['button_active_fg']
    except AssertionError:
      self.banner_color = '#3B4483'
      self.bg_theme = '#E1E1E1'
      self.active_bg_theme = '#E1E1E1'
      self.fg_theme = 'black'
      self.button_bg = '#dedede'
      self.button_fg = 'black'
      self.button_active_bg = '#c9c9c9'
      self.button_active_fg = 'black'
      
    self.root.config(bg= self.bg_theme)
  def initializeTextVariables(self):
    pass
      
  def initializeFrames(self, reset= False):
    self.initializeTheme(reset)
    self.initializeTextVariables()
    self.create_Banner(root)
    self.create_CenterFrame(root)
    
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
    
    clear_only = tk.Button(clear_Button_Frame, text="Clear Only", command = self.vars.clear_All_Fields, bg='#ebdb34', fg='#0d0d0c', activebackground='#ccbe2d', activeforeground='#0d0d0c')
    clear_only.grid(column=0, row = 0, padx=18, sticky='E')
    clear_all = tk.Button(clear_Button_Frame, text="Clear & Log", command = self.vars.clear_And_Log, bg='#C1392B', fg='#F8F8F8', activebackground='#a3382a', activeforeground='#F8F8F8')
    clear_all.grid(column=1, row = 0, padx=2, pady=3, sticky='E')
  def create_CenterFrame(self, root, col= 0, row= 1):
    center_Frame = tk.Frame(root, bg = self.bg_theme)
    center_Frame.grid(column= 0, row= row, sticky='nsew', padx= 3, pady= 5)
    
    self.create_SES_Form(center_Frame, 0, 0)
    self.create_Textbox_Frames(center_Frame, 1, 0)
  def create_SES_Form(self, centerFrame, col, row):
    scrollBoxWidth = 160
    
    form_Master_Frame = tk.Frame(centerFrame, bg = self.bg_theme)
    form_Master_Frame.grid(column= col, row= row, sticky='nsew')
    
    caller_info = tk.Frame(form_Master_Frame, bg= self.bg_theme)
    core_and_panel= tk.Frame(form_Master_Frame)
    ap_Panel = tk.Frame(form_Master_Frame)

    
    #List of every Frame & includes the ap_List.
    frame_List = [
        caller_info,
        core_and_panel,
        ap_Panel,
        ]
    
    #Places each frame EXCEPT ap_List on the grid.  
    #ap_List needs to be iterated since it's essentially repeating itself.
    i= 0
    for frame in frame_List:
      frame.config(bg= self.bg_theme)
      frame.grid(column= 0, row= i, sticky= 'nsew')
      i+= 1
    
    
    #caller_info Frame#################################
    store_Label = tk.Label(caller_info, text= 'Store:')
    name_Label = tk.Label(caller_info, text= 'Name:')
    phone_Label = tk.Label(caller_info, text= 'Phone:')
    
    store = tk.Entry(caller_info, width=5, textvariable= self.vars.variables['store'])
    self.vars.assign_Widget_From_SES_Logger('store', store)
    ## THIS WORKS
    
    name = tk.Entry(caller_info, width=20, textvariable= self.vars.variables['name'])
    self.vars.assign_Widget_From_SES_Logger('name', name)
    phone = tk.Entry(caller_info, width=16, textvariable= self.vars.variables['phone'])
    self.vars.assign_Widget_From_SES_Logger('phone', phone)
    
    i= 0
    for label, entry in zip([store_Label, name_Label, phone_Label],[store, name, phone]):
      label.config(bg= self.bg_theme)
      label.grid(column=0, row= i, sticky= 'nw')
      
      #Editing colors for later
      #entry.config(bg= self.bg_theme)
      entry.grid(column=1, row= i, sticky= 'nw')
      i+= 1
    ####################################################
    
    # core_and_panel ###################################
    
    
    ####################################################
    
    
    # AP's #############################################
    ap_Frame = tk.LabelFrame(ap_Panel, bg= self.bg_theme)
    ap_Frame.grid(sticky= 'nw', pady= 2)
    
    self.scrollFrame= VerticalScrolledFrame(ap_Frame, self.VERTICAL_SCROLL_FRAME_HEIGHT)  #Scrollable frame

    ap_frame_list= []
    
    ### Core
    core_FrameLabel = tk.LabelFrame(self.scrollFrame.interior, text= 'Core:', bg = self.bg_theme)
    core_FrameLabel.grid()
    core_FrameInner = tk.Frame(core_FrameLabel, bg= self.bg_theme, width= scrollBoxWidth, height= 50)
    core_FrameInner.grid_propagate(False)
    core_FrameInner.grid()
    
    core_Port_Label = tk.Label(core_FrameInner, text= 'Port:') 
    core_MAC_Label = tk.Label(core_FrameInner, text = 'MAC:')
        
    core_Port = tk.Entry(core_FrameInner, width = 4, textvariable= self.vars.variables['core_port'])
    self.vars.assign_Widget_From_SES_Logger('core_port', core_Port)
    core_MAC = tk.Entry(core_FrameInner, width = 16, textvariable= self.vars.variables['core_mac'])
    self.vars.assign_Widget_From_SES_Logger('core_mac', core_MAC)
    
    ###
    
    i= 0
    for label, entry in zip([core_Port_Label, core_MAC_Label], [core_Port, core_MAC]):
      label.config(bg= self.bg_theme)
      label.grid(column= 0, sticky= 'w')
      
      entry.grid(column= 1, row= i, sticky= 'w')
      if i == 1:
        label.config(pady= 2)
      i+= 1
    
    ####################################################
    """
    Create i frames, i == number of APs designated on load.
    Creates a frame within the LabelFrame to control the inner padding/style.
    textvariables are assigned through self.vars.variables.
    
    """
    for i in range(self.NUM_OF_APS):
      #master frame, tmp frame is there to control spacing
      master = tk.LabelFrame(self.scrollFrame.interior, text= 'AP '+str(i+1), bg= self.bg_theme)
      #temp frame to hold created widgets during each iteration
      tmp = tk.Frame(master, bg= self.bg_theme, width= scrollBoxWidth, height= 70)
      tmp.grid_propagate(False)
      
      #places both the frames onto the grid
      master.grid()
      tmp.grid()
      
      ap = 'ap_' + str(i+1)       #name of the ap, thrown into the self.vars object
            
      cable_Label = tk.Entry(tmp, width= 6, textvariable = self.vars.variables[ap]['cable'])    #Cable entry box field
      self.vars.variables[ap]['cable'].set("2d93"+str(i+1))                                     #Assigns the variable of the cable entry field to a predetermined cable name
      
      
      port_Label = tk.Label(tmp, text= 'Port:')
      mac_Label = tk.Label(tmp, text= 'MAC:')
      
      port = tk.Entry(tmp, width= 4, textvariable = self.vars.variables[ap]['port'])
      mac = tk.Entry(tmp, width= 16, textvariable = self.vars.variables[ap]['mac'])

      check = tk.Checkbutton(tmp, text= "Complete", variable = self.vars.variables[ap]['check'])
        

      #For Loops that place the widgets into the grid
      j = 0
      for label in [cable_Label, port_Label, mac_Label]:
        label.config(bg= self.bg_theme)
        if j == 0: #not a label, entry field
          label.grid(column= 0, row= j, sticky= 'nw', padx= 2, pady= 2)
          self.vars.assign_Widget_From_SES_Logger('cable', label, "ap_"+str(i+1))
        else:
          label.grid(column= 0, row= j, sticky= 'nw')
        j+= 1
      j = 0
      for entry in [check, port, mac]: #Where to place check box   <<<<<<<<<<<<<<<<<<<<<<<<<<<<
        entry.grid(column=1, row= j, sticky= 'nw')
        if j == 0:
          entry.config(bg = self.bg_theme, activebackground = self.active_bg_theme)
          entry.grid(padx = 35)
          self.vars.assign_Widget_From_SES_Logger('check', entry, "ap_"+str(i+1))
        if j == 1:
          
          self.vars.assign_Widget_From_SES_Logger('port', entry, "ap_"+str(i+1))
        if j == 2:
          self.vars.assign_Widget_From_SES_Logger('mac', entry, "ap_"+str(i+1))
        j+= 1
      ap_frame_list.append(tmp)
      ap_frame_list[-1].grid()
 
    self.scrollFrame.grid()
    ####################################################
  def create_Textbox_Frames(self, centerFrame, col, row):
    txtBox_Master_Frame = tk.Frame(centerFrame, bg = self.bg_theme)
    txtBox_Master_Frame.grid(column= col, row= row, sticky='nsew', padx= 5)
    
    #Textbox Buttons
    button_Frame = tk.Frame(txtBox_Master_Frame, bg= self.bg_theme)
    self.create_Textbox_Buttons(button_Frame)
    
    #Notepad text area
    note_Frame = tk.LabelFrame(txtBox_Master_Frame, bg= self.bg_theme, text= 'Notes', borderwidth= 0)  
    notes = scrolledtext.ScrolledText(note_Frame, width= 47, height= 10, padx= 5, wrap=tk.WORD)
    notes.grid()
    self.vars.assign_TextBox_From_SES_Logger('notes', notes)      #Assign to instanced variable inside ses_data
    
    #Format (POTENTIAL) output text area
    formatted_Frame= tk.LabelFrame(txtBox_Master_Frame, bg= self.bg_theme, text= 'Call Info', borderwidth= 0, height= 150)
    formatted_Frame.grid_propagate(False)
    formatted_Output= scrolledtext.ScrolledText(formatted_Frame, width= 47, height= 8, padx= 5, wrap= tk.WORD)
    formatted_Output.grid()
    self.vars.assign_TextBox_From_SES_Logger('output', formatted_Output)      #Assign to instanced variable inside ses_data
    
    #place frames 
    button_Frame.grid(column= 0, row= 0, sticky='nsew')
    note_Frame.grid(column= 0, row= 1, sticky='nsew')
    formatted_Frame.grid(column= 0, row= 2, sticky= 'nsew')
    
    
  def create_Textbox_Buttons(self, button_Frame):
    
    release_Button = releaseCode_Button(button_Frame, self.menu.return_Settings()['Theme'], col= 0, row= 0 )
    
    pass
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
    
# ************************
# Scrollable Frame Class
# ************************
# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    focused = False
    def __init__(self, parent, canvasHeight, *args, **kw):
        
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set, height= canvasHeight)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)
        
        

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)
        
        def _on_leave(event):
          self.focused = False
        interior.bind('<Leave>', _on_leave)
        def _on_enter(event):
          self.focused = True
        interior.bind("<Enter>", _on_enter)
        def _on_mousewheel(event):
          if(self.focused):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.interior.bind_all("<MouseWheel>", _on_mousewheel)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
class releaseCode_Button(tk.Button):
  def __init__(self, root, theme, col= 0, row= 0, *args, **kw):
        
    tk.Button.__init__(self, root, *args, **kw)
    
    release_Button = tk.Button(root, text = 'Release Code')
    release_Button.grid(column= col, row= row, sticky= 'nsew')
    

    def config_Style(reset = False):
     
      def set_Style():
        #Creates a set of variables that is associated with the theme.
        try:
          assert reset == False
          self.button_bg = theme['button_bg']
          self.button_fg = theme['button_fg']
          self.button_active_bg = theme['button_active_bg']
          self.button_active_fg = theme['button_active_fg']
        except AssertionError:
          self.button_bg = '#dedede'
          self.button_fg = 'black'
          self.button_active_bg = '#c9c9c9'
          self.button_active_fg = 'black'
      
      #calls the function that sets the self variables of the theme
      set_Style()
      
      release_Button.config(activebackground= self.button_active_bg, activeforeground= self.button_active_fg)
      release_Button.config(bg= self.button_bg, fg= self.button_fg)
      
    try:
      config_Style()
    except:
      config_Style(True)
    
    
    
if __name__ == "__main__":
  
  root = tk.Tk()
  ws_gui = SES_Logger(root)
  
  root.mainloop()
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  