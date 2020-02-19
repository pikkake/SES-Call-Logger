
class SES:

  def __init__(self):
    user = {
      "Name":"",
      "Initials":"",
      "Emp_Num": 0    
    }
    
    theme = {
      'banner_color' : '#3B4483',
      'bg_theme' : '#E1E1E1',
      'fg_theme' : 'black',
      'button_bg' : '#dedede',
      'button_fg' : 'black',
      'button_active_bg' : '#c9c9c9',
      'button_active_fg' : 'black'
        }

    null = {
        "Null_Value":"Nothing"
        }
    
    
    self.master = {
     'User':user,
     'Theme':theme,
     'NULL': null
     
     }
  def returnMaster(self):
    return self.master
  