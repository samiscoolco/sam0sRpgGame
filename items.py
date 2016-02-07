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
    def Use(self):
        if isinstance(self,Food):
            print self.parentContain.index(self)
            self.parent.food-=self.consumeVal

#TYPES
class Food(Item):
    def __init__(self,setp,name,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.name=name
        self.consumeVal = 25
        self.weight = 1
        self.stack=1
        self.imgnum=0
