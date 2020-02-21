# -*- coding: utf-8 -*-
import tkinter as tk
import etc.setting_Data as sd
#from pyperclip import copy
#from time import strftime, localtime

class MenuBar:
  
  """
  Requires a main window with dimensions 500x400px.  
  IF changing dimensions, edit the 'size_of_menu' parameter
  
  """
  ###############################################  
  SETTINGS_HEIGHT = 400       #Height of the settings window
  SETTINGS_WIDTH = 350        #Width of the settings window
  
  size_of_menu_separator = 172  #Space that pushes the settings button to the right
  settings_menu_x_offset = 115  #Offset from the top left corner of the main window
  settings_menu_y_offset = 25
  
  settings_State = False        #Boolean handling if Settings is open
  
  list_Of_Setting_Frames = {}
  
  ###############################################
  
  def __init__(self, root):
    self.root = root
    
    self.config = sd.setting_Data()
        
    root.bind('<Motion>', self.motion)
    self.menuBar = tk.Menu(self.root)
    self.createMenuBar()  
  
  def createMenuBar(self):
    settingSpacing = ''
    i = 0
    
    while i < self.size_of_menu_separator:
      settingSpacing+=" "
      i+=1
      
    self.menuBar.add_command(label=settingSpacing, state = "disabled")
    
    #Settings button runs the openSettings function
    self.menuBar.add_command(label="Settings", command=self.openSettings)
    
    
    #Add menu to root/the main window
    self.root.config(menu=self.menuBar)
  
  def createSettingsMenu(self, root):
    """
    Creates the actual settings window.  Requires the toplevel frame, called as 'root'
    """
    ############
    listbox_coordinates = (0,0) #column/row
    form_coordinates = (1,0)
    panel_options = []
    
    #Pulls data from the config file to create a list of settings.
    tmp = self.config.return_Raw_Settings()
    for setting in tmp:
      panel_options.append(setting)
    ############
    

    central_Frame = tk.Frame(root, width = self.SETTINGS_WIDTH-50)
    central_Frame.grid(column = 0, row = 0, padx = 5, sticky = 'w')
    #central_Frame.grid_propagate(False)
    
    bottom_Frame = tk.Frame(root, width = self.SETTINGS_WIDTH, height = 100)
    bottom_Frame.grid(column = 0, row = 1, padx = 5)
    bottom_Frame.grid_propagate(False)

    self.createListOfOptions(central_Frame, listbox_coordinates, panel_options)
    self.createSelectedForm(central_Frame, form_coordinates) 
    self.createButtonFrame(bottom_Frame)
    
    #Initialized what to load when Settings is created.
    self.settings_panel.select_set(0)
    self.list_Of_Setting_Frames['User'].mountFrame()
    
  def createListOfOptions(self, central_frame_of_settings_menu, panel_cords, panel_options):
    """
    Creates the list of setting options and places it on the left most column of the given frame.
    """
    
    root = central_frame_of_settings_menu
    
    settings_panel_frame = tk.LabelFrame(root, text = "Setting Options")
    settings_panel_frame.grid(column = panel_cords[0], row=panel_cords[1], sticky="w")
    
    self.settings_panel = tk.Listbox(settings_panel_frame, selectmode = "SINGLE",
                                font = 10, height = 16, width = 10, exportselection = False)
    
    for item in panel_options:
      self.settings_panel.insert(tk.END, item)
    self.settings_panel.grid(column=0, row=0)
    
    self.settings_panel.bind('<<ListboxSelect>>', self.listboxSelect)
    
    
  def createSelectedForm(self, central_frame_of_settings_menu, form_cords) :
    """
    Creates the area which the forms are changed.
    Takes the central frame of the settings windows and assigned it locally as 'root,'
    Uses coordinates passed from the createSettingsMenu to place it in the frame.
    
    """
    root = central_frame_of_settings_menu
    
    self.form_frame = tk.Frame(root)
    self.form_frame.grid(column = form_cords[0], row=form_cords[1], sticky="nsew")
    
    self.createIndividual_Setting_Frames(self.form_frame)
    
    
  def createIndividual_Setting_Frames(self, root):
    """
    Creates an object 'grouped_Settings' and stores within this class.  This object is used to handle
    necessary setting Objects within a dict.  
    
    list_Of_Setting_Frames stores the dict returned by grouped_Settings.
    """
    
    master = self.settings_Window #master window of the Settings object.
    
    self.grouped_Settings = all_Settings(master, root, self.config)
    self.list_Of_Setting_Frames = self.grouped_Settings.return_Settings_Dict()
    
  def createButtonFrame(self, root):
    button_Frame = tk.Frame(root, width=self.SETTINGS_WIDTH/2)
    button_Frame.grid(column=1, row=0)
    separator = tk.Frame(root, width = 180)
    separator.grid(column=0, row = 0)
    save = tk.Button(button_Frame, text = 'Save', command= self.closeAndSave)
    apply = tk.Button(button_Frame, text="Apply", command= self.grouped_Settings.save_All)
    close = tk.Button(button_Frame, text = 'Close', command = self.closeSettings)
    
    
    save.grid(column = 0, row = 0, sticky = 'nsew', padx = 7)
    apply.grid(column = 1, row = 0, sticky = 'nsew', padx = 7)
    close.grid(column = 2, row = 0, sticky = 'nsew', padx = 7)
    
  def openSettings(self):
    """
    Creates a settings menu and places it on the screen using the winfo of self.root & an offset.
    
    """
    
    #######################
    
    x_offset = self.settings_menu_x_offset
    y_offset = self.settings_menu_y_offset
    
    #######################
    if not self.settings_State:  #if settings_State is False/ Window isn't opened
      self.settings_Window = tk.Toplevel(self.root)
      self.settings_Window.protocol("WM_DELETE_WINDOW", self.closeSettings)
      self.settings_Window.resizable(width = tk.FALSE, height = tk.FALSE)
      
      
      x_offset += self.root.winfo_x()
      y_offset += self.root.winfo_y()
      
      settings_dim = "{}x{}+{}+{}".format(self.SETTINGS_WIDTH, self.SETTINGS_HEIGHT, x_offset, y_offset)
      self.settings_Window.geometry(settings_dim)
      self.settings_Window.wm_attributes("-topmost",2)
      
      self.createSettingsMenu(self.settings_Window)
      
      self.setActive(self.settings_Window)
      
  def closeSettings(self):
    self.settings_Window.destroy()
    self.settings_State = False
  def closeAndSave(self):
    self.grouped_Settings.save_All()
    self.closeSettings()
  def setActive(self, root):
    root.lift()
    root.grab_set()
    root.focus_set()
    self.settings_State = True
  def return_Settings(self):
    return self.config.return_Raw_Settings()
  def listboxSelect(self, event):
    item = event.widget
    try:
      index = (int(item.curselection()[0]))
      value = item.get(index)
      
      for setting_frame in self.list_Of_Setting_Frames:
        if setting_frame == value:
          self.list_Of_Setting_Frames[setting_frame].mountFrame()
        else:
          self.list_Of_Setting_Frames[setting_frame].unmountFrame()
    except:
      print("Frame '"+value+"' was not found!")
    
  def motion(self, event):
    global x_cord
    global y_cord
    x_cord, y_cord = event.x, event.y
    

class all_Settings:
  def __init__(self, master, root, configuration_File):
    """
    all_Settings stores all setting Objects within itself.  Used to call the list of setting Objects and
    write to each object.  Essentially handles the load of object handling away from the main settings Class.
    
    To create a setting, must do the following:
      1) Create the 'setting.py' module to be created in setting_Data.py.
      2) Create the setting object below, using base_settings as the parent class.
        a) Declare self.setting_Attribute THE SAME AS THE SETTING LISTED IN setting.py FILE!
        b) Call self.setting_data = self.config.return_Specified_Setting(self.setting_Attribute)
        c) Create a dict using self.create_Dict_Of_Widgets(LIST OF WIDGETS)
      3) Call an instance of the setting object
      4) Place setting object in 'list_of_Settings' IN THE SAME ORDER APPEARING IN THE setting.py FILE!
      5) After all this, it should properly assign the frame of the created setting to the listbox for selection.
    
    """
    self.master = master
    #Settings are created and stored in local variables.  Class initializations are handled below.
    user_Frame = user_Settings(root, configuration_File)
    null_Frame = null_Settings_TEST(root, configuration_File)
    theme_Frame = theme_Settings(root, configuration_File)
    
    list_of_Settings = [
        user_Frame,
        theme_Frame,
        null_Frame
        
        ]
    #Configuration data pulled from a JSON file is stored within this object.
    self.config = configuration_File
    
    #A dict containing each setting Object is stored within this object.
    
    self.dict_Of_Setting_Frames = {}
    #keys = self.config.return_List_Of_Keys
    i = 0
    
    #Cycles through the list of settings created by the Setting_Data module.
    #Creates a tmp dict and saves the result within the object.
    #IMPORTANT:
    #Settings listed within list_of_Settings MUST MATCH the list of returned keys perfectly.
    
    for setting_Label in self.config.return_List_Of_Keys():
      try:
        tmp = {setting_Label: list_of_Settings[i]}
        self.dict_Of_Setting_Frames.update(tmp)        
      except IndexError as e:
        print("Too many keys returned from 'self.config.return_List_Of_Keys()'\n" +setting_Label+" not created." )
      finally:
        i+=1

  def return_Settings_Dict(self):
    """
    Returns the dict containing every setting Object.
    """
    return self.dict_Of_Setting_Frames
  def save_All(self): #TO DO
    """
    Creates a JSON dict from the self.config object.
    Pulls a dict of Widgets created by each setting object.
    Cycles through each setting Object's config files, matches the name of the specified setting with
    the name of the widget.  Saves that specific setting to the final JSON dict.
    Dict is saves via write_All_Settings()
    """
    final = self.config.return_Raw_Settings()
    
    for setting in self.dict_Of_Setting_Frames:
      tmp = self.dict_Of_Setting_Frames[setting]
      widget_Dict = tmp.return_dict_Of_Widgets()
      setting_Data = tmp.setting_data
            
      for selected_Data in setting_Data:
        
        for widget in widget_Dict:
          if selected_Data == widget:
            final[setting][selected_Data] = widget_Dict[widget].get().strip()
      
      self.config.write_All_Settings(final)

    
    
    
    
    
  ##### Baseline functions for settings ######
class base_settings:
  def __init__(self, root, config):
    self.config = config
    self.setting_Attribute = ""
    self.setting_data = {}
    self.dict_Of_Widgets = {}
        
    self.master = tk.Frame(root)
    self.form = tk.Frame(self.master)
    self.form.grid(sticky = "nsew", padx = 8, pady=8)
    
  def unmountFrame(self):
    self.master.grid_forget()
  def mountFrame(self):
    self.master.grid()
  def create_Dict_Of_Widgets(self, args):
    """
    Takes widgets (Entry, etc.) in *args and assigns it to a dictionary based on the name of the widget.
    This will ONLY assign widgets if the widget name is == to the setting_Name.lower()
    
    """
    
    data = self.setting_data
    for setting_Name in data: 
      #print(setting_Name) #debugging
      for selected_Widget in args:
        tmp_Array = str(selected_Widget).split('.')
        tmp = tmp_Array[-1]
        if setting_Name.lower() == tmp:
          tmp_Dict = {setting_Name: selected_Widget}
          self.dict_Of_Widgets.update(tmp_Dict)  

  def return_dict_Of_Widgets(self):
    return self.dict_Of_Widgets
  def save_Settings(self):
    self.config.write_Specified_Setting(self.setting_Attribute, self.setting_data)
  #############################################
  
  ##### Setting Item: User ######
  
class user_Settings(base_settings):
  def __init__(self, root, config):
    super().__init__(root, config)
    ############################
    
    self.setting_Attribute = "User" #name of the setting
    self.setting_data = self.config.return_Specified_Setting(self.setting_Attribute)
    
    self.initials = tk.StringVar()
    self.employeeNum = tk.StringVar()
    self.name = tk.StringVar()
    ############################
    
    self.createForm()
    
    
  def createForm(self):
    initials_label = tk.Label(self.form, text = "Initials")
    self.initials_textbox = tk.Entry(self.form, width=5, textvariable= self.initials, name ="initials")
    emp_label = tk.Label(self.form, text = "Employee Number")
    self.emp_textbox = tk.Entry(self.form, width = 5, textvariable = self.employeeNum, name = 'emp_num')
    initials_label.grid(column=0, row=0, sticky = 'w')
    self.initials_textbox.grid(column=1, row=0, sticky = 'w')
    emp_label.grid(column=0, row=1, sticky = 'w')
    self.emp_textbox.grid(column=1,row=1, sticky = 'w')
    emp_label.grid(column=0, row=1, sticky = 'w')
    self.emp_textbox.grid(column=1,row=1, sticky = 'w')

    
    entry_List = [
        self.initials_textbox,
        self.emp_textbox,
        ]
    
    self.populateFields()
    self.create_Dict_Of_Widgets(entry_List)
  def populateFields(self):
    items = self.setting_data
    self.initials.set(items['Initials'])
    self.employeeNum.set(items['Emp_Num'])
    self.name.set(items['Name'])
  
  
class theme_Settings(base_settings):
  def __init__(self, root, config):
    super().__init__(root, config)
    
    self.setting_Attribute = "Theme" #name of the setting
    self.setting_data = self.config.return_Specified_Setting(self.setting_Attribute)
    
    self.createForm()
    
  def createTextVariables(self):
    """
    Initializes the textvariables that are stored within 
    """
    self.banner = tk.StringVar()
    self.background = tk.StringVar()
    self.foreground = tk.StringVar()
    self.button_BG = tk.StringVar()
    self.button_FG = tk.StringVar()
    self.button_Active_BG = tk.StringVar()
    self.button_Active_FG = tk.StringVar()    
    
  def createForm(self):

    label_Frame = tk.Frame(self.form)
    entry_Frame = tk.Frame(self.form)
    label_Frame.grid(column= 0, row = 0, sticky = 'nsew')
    entry_Frame.grid(column= 1, row = 0, sticky = 'nsew')
    
    self.createTextVariables()

    banner_Label = tk.Label(label_Frame, text = 'Banner')
    background_Label = tk.Label(label_Frame, text = 'BG')
    foreground_Label = tk.Label(label_Frame, text = 'FG')
    button_BG_label = tk.Label(label_Frame, text = 'Button BG')
    button_FG_label = tk.Label(label_Frame, text = 'Button FG')
    button_active_bg_Label = tk.Label(label_Frame, text = 'Active Button BG')
    button_active_fg_Label = tk.Label(label_Frame, text = 'Active Button FG')
    
    banner = tk.Entry(entry_Frame, width = 10, textvariable = self.banner, name='banner_color')
    background = tk.Entry(entry_Frame, width = 10, textvariable = self.background, name='bg_theme')
    foreground = tk.Entry(entry_Frame, width = 10, textvariable = self.foreground, name='fg_theme')
    button_BG = tk.Entry(entry_Frame, width = 10, textvariable = self.button_BG, name='button_bg')
    button_FG = tk.Entry(entry_Frame, width = 10, textvariable = self.button_FG, name='button_fg')
    button_Active_BG = tk.Entry(entry_Frame, width = 10, textvariable = self.button_Active_BG, name='button_active_bg')
    button_Active_FG = tk.Entry(entry_Frame, width = 10, textvariable = self.button_Active_FG, name='button_active_fg')
    
    label_List = [
      banner_Label,
      background_Label,
      foreground_Label,
      button_BG_label,
      button_FG_label, 
      button_active_bg_Label,
      button_active_fg_Label, 
        ]
    entry_List = [
      banner,
      background,
      foreground,
      button_BG,
      button_FG,
      button_Active_BG,
      button_Active_FG,
        ]
    i = 0
    for label, entry in zip(label_List, entry_List):
      label.grid(column = 0, row = i, sticky = 'nw')
      entry.grid(column = 1, row = i, sticky = 'nw', pady = 1, padx = 5)
      i+=1
      
    self.populateFields()
    self.create_Dict_Of_Widgets(entry_List)
    
  def populateFields(self):

    items = self.setting_data
    self.banner.set(items['banner_color'])
    self.background.set(items['bg_theme'])
    self.foreground.set(items['fg_theme'])
    self.button_BG.set(items['button_bg'])
    self.button_FG.set(items['button_fg'])
    self.button_Active_BG.set(items['button_active_bg'])
    self.button_Active_FG.set(items['button_active_fg'])
    
class null_Settings_TEST(base_settings):
  def __init__(self, root, config):
    super().__init__(root, config)    
    ############################
    
    self.setting_Attribute = "NULL" #name of the setting
    self.setting_data = self.config.return_Specified_Setting(self.setting_Attribute)
    
    ############################
    test = tk.Label(self.form, text = "Placeholder for debugging")
    test_box = tk.Entry(self.form, width = 10, name = 'null_value')
    
    test.grid()
    test_box.grid()
    entry_List = [
        test_box]
    self.create_Dict_Of_Widgets(entry_List)

    
    
  
  
  ###############################
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
