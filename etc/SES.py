
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
    null = {
        "Null_Value":"Nothing"
        }
    self.master = {
     'User':user,
     'NULL': null,
     'Theme':theme
     }
  def returnMaster(self):
    return self.master
  