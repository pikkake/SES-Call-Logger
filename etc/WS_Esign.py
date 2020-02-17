
class WS_Esign:

  def __init__(self):
    user = {
      "Name":"",
      "Initials":"",
      "Emp_Num": 0    
    }
    null = {
        "Null_Value":"Nothing"
        }
    self.master = {
     'User':user,
     'NULL': null
     }
  def returnMaster(self):
    return self.master
  