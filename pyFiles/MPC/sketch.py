# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:57:37 2019

@author: axkar1
"""

class parent:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def getName(self):
        return self.name
    def getAge(self):
        return self.age
    
class child(parent):
    def __init__(self, name, age, id):
        super().__init__(name, age)
        self.id = id
        
    def getID(self):
        return self.id

c = child('Lul', 1, 1)
print(c.getName())
print(c.getAge())
print(c.getID())