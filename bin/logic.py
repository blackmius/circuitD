#!/usr/bin/env python
# -*- coding: utf-8 -*-
import types
import copy

AND = lambda a, b: bool(a) and bool(b)
OR = lambda a, b: bool(a) or bool(b)
NOT = lambda a: not bool(a)

class outlet:
    def __init__(self, owner, name, out):
        self.value = False
        self.owner = owner
        
        self.name = name
        self.type = 'outlet'

        self.out = out
        
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

    def switch(self):
        self.set(not self.value)

class PrimElement:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def eval(self):
        return
    
    def update(self):
        self.out.update()

    def connect(self, out):
        self.out.connect(out)

class Not(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name, 'not')
        self.in1 = outlet(self, 'A', False)
        self.out = outlet(self, 'B', True)

    def eval(self):
        self.out.set(NOT(self.in1.value))

class And(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name, 'and')
        self.in1 = outlet(self, 'A', False)
        self.in2 = outlet(self, 'B', False)
        self.out = outlet(self, 'C', True)

    def eval(self):
        self.out.set(AND(self.in1.value, self.in2.value))

class Or(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name, 'or')
        self.in1 = outlet(self, 'A', False)
        self.in2 = outlet(self, 'B', False)
        self.out = outlet(self, 'C', True)

    def eval(self):
        self.out.set(OR(self.in1.value, self.in2.value))

class Switch(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name, 'switch')
        self.out = outlet(self, 'A', True)

    def eval(self):
        self.out.update()

    def switch(self):
        self.out.switch()

    def setValue(self, value):
        self.out.set(value)

class Bulb(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name, 'bulb')
        self.value = False
        self.in1 = outlet(self, 'A', False)

    def eval(self):
        self.value = self.in1.value


class Constant(PrimElement):
    def __init__(self, name, value):
        PrimElement.__init__(self, name, 'constant')
        self.value = value
        
        self.out = outlet(self, 'A', True)
        self.out.value = self.value
    
    def eval(self):
        self.out.update()


class Element(PrimElement):
    def __call__(self, name):
        prims = []

        for i in dir(self):
            if type(getattr(self, i)) is types.InstanceType:
                prims.append(copy.copy(getattr(self, i)))

        el = Element(name)

        el.add(prims)

        return el

    def __init__(self, name):
        PrimElement.__init__(self, name, name)

        self.inputs = []

        self.outputs = []
    
    def add(self, gate):
        if type(gate) is list:
            for i in gate:
                if i.type == 'bulb':
                    i.in1.name = i.name

                    setattr(self, i.name, i.in1)

                    self.outputs.append(i.name)

                elif i.type == 'switch':
                    i.out.name = i.name 

                    setattr(self, i.name, i.out)

                    self.inputs.append(i.name)

                elif i.type == 'outlet':
                    setattr(self, i.name, i)

                    if not i.out:
                        self.outputs.append(i.name)
                    
                    else:
                        self.inputs.append(i.name)

                else:
                    setattr(self, i.name, i)

        else:
            if i.type == 'bulb':
                setattr(self, i.name, i.in1)

                self.outputs.append(i.name)

            elif i.type == 'switch':
                setattr(self, i.name, i.out)
                
                self.inputs.append(i.name)

            else:
                setattr(self, gate.name, gate)
    
    def eval(self):       
        for i in self.inputs:
            getattr(self, i).update()

    def value(self):
        for o in self.outputs:
            print o, getattr(self, o).value

    def inValue(self):
        for i in self.inputs:
            print getattr(self, i).name, getattr(self, i).value

    def get(self, name):
        return getattr(self, name)

Xor = Element('Xor')

S1 = Switch('s1')
S2 = Switch('s2')
N1 = Not('n1')
N2 = Not('n2')
A1 = And('a1')
A2 = And('a2')
O1 = Or('o1')
B1 = Bulb('b1')

S1.connect([N1.in1, A2.in1])

S2.connect([N2.in1, A1.in1])

N1.connect(A1.in2)

N2.connect(A2.in2)

A2.connect(O1.in1)

A1.connect(O1.in2)

O1.connect(B1.in1)

Xor.add([S1, S2, N1, N2, A1, A2, O1, B1])

Xor.value()

elnel = Element('el in el')

d1 = Switch('s1')
d2 = Switch('s2')
d3 = Switch('s3')
d4 = Switch('s4')

X1 = Xor