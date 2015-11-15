#!/usr/bin/env python
"""
items. py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []

class Item:
    def __init__(self):
        self.stack=1
    def setContainer(self,setpc):
        self.parentContain=setpc
    def setName(self, name):
        self.name = name
    def destroy(self):
        test=self.parentContain
        print self.name

class Apple(Item):
    def __init__(self,setpc=None):
        self.parentContain=setpc
        self.name="app"
        self.type = "con"
        self.consumeVal = 25
        self.weight = 1
        

class Knfe(Item):
    def __init__(self,setpc=None):
        self.parentContain=setpc
        self.name="kni"
        self.type="wep"
        self.consumeVal=0
        self.weight=1
        self.stack=1
    
