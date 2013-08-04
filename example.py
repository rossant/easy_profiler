# @profile
def fun():
    for _ in (_ for _ in xrange(1000000)):
        pass
        
if __name__ == '__main__':
    fun()
        