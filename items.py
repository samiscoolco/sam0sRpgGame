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
        if self.type == "con":
            print self.parentContain.index(self)
            self.parent.food-=self.consumeVal


class Apple(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.name="app"
        self.type = "con"
        self.consumeVal = 25
        self.weight = 1
        self.stack=1
        self.imgnum=0

class Hat(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.name="hat"
        self.type="apr"
        self.consumeVal=0
        self.weight=1
        self.stack=1

class Knfe(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.name="kni"
        self.type="wep"
        self.consumeVal=0
        self.weight=1
