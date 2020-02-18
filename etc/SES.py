
class SES:

  def __init__(self):
    user = {
      "Name":"",
      "Initials":"",
      "Emp_Num": 0    
    }
    theme = {
        "window_bg" : ""
        }
    window = {
        'Window' : 'on-top'
        }
    null = {
        "Null_Value":"Nothing"
        }
    
    
    self.master = {
     'User':user,
     'NULL': null,
     'Theme':theme,
     'Window':window
     }
  def returnMaster(self):
    return self.master
  