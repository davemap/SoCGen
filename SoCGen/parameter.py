from enum import Enum, auto

class Parameter:
    def __init__(self,name,default_value):
        self.name = name
        self.description = ""
        self.default_value =  default_value
        self.value = self.default_value