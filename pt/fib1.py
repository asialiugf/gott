from collections import Iterable

class kkk(object):
    def __init__(self):
      self.a = 1
    def __iter__(self):
        return self
    def __next__(self):
        self.a = self.a + 1
        if self.a > 20: # 退出循环的条件
            raise StopIteration();
        return self.a
    def next(self):
        return self.a + 1000

class Fib(object):
#class Fib(Iterable):
    def __init__(self,m,n):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b
        self.m = m
        self.n = n
        self.K = kkk() #kkk也是一个可迭代类，同时，也是一个迭代器类

    #根据需要，你可以返回不同的迭代器对象。
    def __iter__(self):
        if self.m ==5:
            return self.K
        else:
            return self
        #return self # 实例本身就是迭代对象，故返回自己

    def next(self): # next()在python3中，已经不具有其它含义，只是普通的一个方法。
        return self.a + 5555

    def addd(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100: # 退出循环的条件
            raise StopIteration();
        return self.a # 返回下一个值

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100: # 退出循环的条件
            raise StopIteration();
        return self.a # 返回下一个值

if __name__ == '__main__':
    x = Fib(5,6)
    print(x.__next__())
    print(x.__next__())
    print(x.__next__())
    print(x.__next__())

    print(x.next())
    print(x.next())
    print(x.next())
    print(x.next())

    print( "---------------------------------")
    print(x.addd())
    print(x.addd())
    print(x.addd())
    print(x.addd())
    print( "------in Fib(5,4)---------------------------")
    for n in Fib(5,4):
        print (n)
    print( "------in Fib(3,4)---------------------------")
    for n in Fib(3,4):
        print (n)

    print( "-------------in m --5,4------------------")
    m = Fib(5,4)
    for n in m:
        print(n)

    print( "-------------in m --3,4------------------")
    m = Fib(4,4)
    """
    print("-----m.next() is:",m.next() )
    print("-----m.next() is:",m.next() )
    print("-----m.next() is:",m.next() )
    """
    for n in m:
        print(n)

    print( "-------------in iter(m) --5,4------------------")
    m = Fib(5,4)
    x = iter(m)  #请问，iter是谁的内置函数
    print("-----iter(m).next() is:",x.next() )
    print("-----iter(m).next() is:",x.next() )
    print("-----iter(m).next() is:",x.next() )

    for n in x:
        print(n)

    print( "-------------in iter(m) --3,4------------------")
    m = Fib(3,4)
    x = iter(m)
    print("-----iter(m).next() is:",x.next() )
    print("-----iter(m).next() is:",x.next() )
    print("-----iter(m).next() is:",x.next() )

    print("-----iter(m).next() is:",x.__next__() )
    print("-----iter(m).next() is:",x.__next__() )
    print("-----iter(m).next() is:",x.__next__() )
    print("-----iter(m).next() is:",x.__next__() )
    print("-----iter(m).next() is:",x.__next__() )
    for n in x:
        print(n)

    print( "-----------------in iter(m) again---------------")

    y = iter(m) #每次调用 iter()会产生一个新的迭代器对象，从头开始。
    for n in y:
        print(n)

    print( "--------------end-------------------")
    #Fib.__next__()



    L = [1,3,2,5,6,7,9,6]
    for n in iter(L):
        print("L:",n)

    for n in iter(L):
        print("L:",n)

    print(dir("__builtins__"))
    print(dir("__class__"))

