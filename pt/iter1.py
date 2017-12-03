class counter:

    def __init__(self, _start, _end):
        self.start = _start
        self.end = _end

    def get_next(self):
        s = self.start
        if(self.start < self.end):
            self.start += 1
        else:
            raise StopIteration

        return s


c = counter(1, 15)
iterator = iter(c.get_next, 3)
print(dir(iterator))
print(type(iterator))
for i in iterator:
    print(i)

print(c.start)

print("--------")
print (c.get_next() )
print (c.get_next() )
print (c.get_next() )
print (c.get_next() )
print (c.get_next() )
print (c.get_next() )
print (c.get_next() )
