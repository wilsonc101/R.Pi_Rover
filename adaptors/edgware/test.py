flist = []

for i in xrange(3):
    def func(x, i=i): # the *value* of i is copied in func() environment
        print "i = " + str(i)
        return x * i
    flist.append(func)

for f in flist:
    print f(2, 1)
