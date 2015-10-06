#!/usr/bin/env python
# -*- coding: utf-8 -*-
import types

AND = lambda a, b: bool(a) and bool(b)
OR = lambda a, b: bool(a) or bool(b)
NOT = lambda a: not bool(a)

class outlet:
    def __init__(self, owner, name):
        self.value = False
        self.owner = owner
        self.name = name
        self.connects = []  
        self.level = 0

    def connect(self, inputs):
        if type(inputs) != type([]):
            inputs = [inputs]
        
        for input in inputs:
            self.connects.append(input)

            input.set(self.value)
            input.owner.eval()

    def set(self, value):
        if self.value == value:
            return                   
        
        self.value = value
        
        self.update()

    
    def update(self):       
        for con in self.connects:
            con.set(self.value)
            
            if con.owner != self.owner:
                con.owner.eval()
            else:
                if self.level == 0:
                    self.level += 1
                    con.owner.eval()
                    
        
        self.level = 0

class PrimElement:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def eval(self):
        return
    
    def update(self):
        self.out.update()

class Not(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name, 'not')
        self.in1 = outlet(self, 'A')
        self.out = outlet(self, 'B')

    def eval(self):
        self.out.set(NOT(self.in1.value))

class And(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name, 'and')
        self.in1 = outlet(self, 'A')
        self.in2 = outlet(self, 'B')
        self.out = outlet(self, 'C')

    def eval(self):
        self.out.set(AND(self.in1.value, self.in2.value))

class Or(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name, 'or')
        self.in1 = outlet(self, 'A')
        self.in2 = outlet(self, 'B')
        self.out = outlet(self, 'C')

    def eval(self):
        self.out.set(OR(self.in1.value, self.in2.value))

class Switch(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name, 'switch')
        self.out = outlet(self, 'A')

    def eval(self):
        self.out.set(NOT(self.out.value))

class Bulb(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name, 'bulb')
        self.value = False
        self.in1 = outlet(self, 'A')

    def eval(self):
        self.value = self.in1.value


class Constant(PrimElement):
    def __init__(self, name, value):
        PrimElement.__init__(self, name, 'constant')
        self.value = value
        
        self.out = outlet(self, 'A')
        self.out.value = self.value
    
    def eval(self):
        self.out.update()


class Element(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name, name)
    
    def add(self, gate):
        setattr(self, gate.name, gate)
    
    def update(self):
        attr = []
        
        for i in dir(self):
            if type(getattr(self, i)) is types.InstanceType:
                attr.append(i)
        
        for i in attr:
            if getattr(self, i).type == 'switch':
                getattr(self, i).update()

El = Element('Xor')

El.add(Switch('s1'))
El.add(Switch('s2'))

N = Not('n')
B1 = Bulb('b2')

N.out.connect(N.in1)
N.out.connect(B1.in1)

print N.out.value, B1.value

N.update()

print N.out.value, B1.value
