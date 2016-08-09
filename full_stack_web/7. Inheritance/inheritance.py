class Parent():
    def __init__(self, lastname, eyecolor):
        self.lastname = lastname
        self.eyecolor = eyecolor

class Child(Parent):
    def __init__(self, lastname, eyecolor, ntoys):
        Parent.__init__(self, lastname, eyecolor)
        self.ntoys = ntoys

p = Parent("Mudgal", "blue")

c = Child("Mudgal", "green", 5)

print c.eyecolor
