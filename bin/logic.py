#!/usr/bin/env python
# -*- coding: utf-8 -*-

AND = lambda a, b: bool(a) and bool(b)
OR = lambda a, b: bool(a) or bool(b)
NOT = lambda a: not bool(a)

class outlet:
    def __init__(self, owner, name):
        self.value = False
        self.owner = owner
        self.name = name
        self.connects = []  

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
        
        for con in self.connects:
            con.set(value)
            con.owner.eval()

class PrimElement:
	def __init__(self, name):
		self.name = name

	def eval(self):
		return

class Not(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name)
        self.in1 = outlet(self, 'A')
        self.out = outlet(self, 'B')

    def eval(self):
        self.out.set(NOT(self.in1.value))

class And(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name)
        self.in1 = outlet(self, 'A')
        self.in2 = outlet(self, 'B')
        self.out = outlet(self, 'C')

    def eval(self):
        self.out.set(AND(self.in1.value, self.in2.value))

class Or(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name)
        self.in1 = outlet(self, 'A')
        self.in2 = outlet(self, 'B')
        self.out = outlet(self, 'C')

    def eval(self):
        self.out.set(OR(self.in1.value, self.in2.value))

class Switch(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name)
        self.out = outlet(self, 'A')

    def eval(self):
        self.out.set(NOT(self.out.value))

class Bulb(PrimElement):
    def __init__(self, name):
        PrimElement.__init__(self, name)
        self.value = False
        self.in1 = outlet(self, 'A')

    def eval(self):
        self.value = self.in1.value


class Constant(PrimElement):
    def __init__(self, name, value):
        PrimElement.__init__(self, name)
        self.value = value
        
        self.out = outlet(self, 'A')
        self.out.value = self.value


class Element(PrimElement):
	def __init__(self, name):
		PrimElement.__init__(self, name)
		self.schema = []

	def eval(self):
		return

S1 = Switch('s1')
S2 = Switch('s2')

N1 = Not('n1')
N2 = Not('n2')

A1 = And('a1')
A2 = And('a2')

O1 = Or('o1')

B = Bulb('b1')

S1.eval()
S2.eval()

S1.out.connect([N1.in1, A2.in1])

S2.out.connect([N2.in1, A1.in2])

N1.out.connect(A1.in1)
N2.out.connect(A2.in2)

A1.out.connect(O1.in1)
A2.out.connect(O1.in2)

O1.out.connect(B.in1)
print S1.out.value, S2.out.value, N1.out.value, N2.out.value, A1.out.value, A2.out.value, B.value
