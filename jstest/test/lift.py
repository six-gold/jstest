#!/usr/bin/env python
# coding=utf-8
import gc


class Person:
    population = 0

    def __init__(self, name):
        self.name = name
        print("initializing %s" % self.name)
        Person.population += 1

    # def __del__(self):
    #     print("%s say bye" % self.name)
    #     Person.population -= 1
    #     if Person.population == 0:
    #         print ("I'm the last one")
    #     else:
    #         print ("There are still %d person left" % Person.population)

    def SayHi(self):
        print ("Hi,my name is %s" % self.name)

    def HowMany(self):
        if Person.population == 1:
            print("I am the only Person here")
        else:
            print ("We have %d person here" % Person.population)

    def Invoke(self):
        print("ok")

gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_LEAK)
a = Person("Swaroop")  # initializing Swaroop
a.SayHi()  # Hi,my name is Swaroop
a.HowMany()  # I am the only Person here

b = Person("Kalam")  # initializing Kalam
b.SayHi()  # Hi,my name is Kalam
b.HowMany()  # We have 2 person here

d = Person("Smithy")
d.SayHi()
d.HowMany()

c = Person("Jackson")
c.SayHi()
c.HowMany()