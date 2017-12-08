class A(object):
 a = "--a"
 def __init__(self):
   self.aa = "aa"
   print("enter A")
   print("leave A")

class B(object):
 def __init__(self):
   self.bb = "bb"
   print("enter B")
   print("leave B")

class C(A):
 def __init__(self):
   self.cc = "cc"
   print("enter C")
   super(C, self).__init__()
   print("leave C")

class D(A):
 def __init__(self):
   self.dd = "dd"
   print("enter D")
   super(D, self).__init__()
   print("leave D")

class E(B, C):
 a = "--e"
 def __init__(self):
   self.ee = "ee"
   print("??",self.ff)
   self.ff = "e.ff"
   print("enter E")
   B.__init__(self)
   C.__init__(self)
   print("leave E")

class F(E, D):
 def __init__(self):
   self.ff = "f.ff"
   print("enter F")
   E.__init__(self)
   D.__init__(self)
   print("leave F")

f=F()
print(f.ff)
#print(f.dd)
#print(f.aa)
print(f.a)
print(F().ff)
print(F().a)
#print(F().aa)
print ("MRO:", [x.__name__ for x in E.__mro__] )
