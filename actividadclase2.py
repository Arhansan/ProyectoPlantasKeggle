import math

class Complex:
    def __init__(self, re=0, im=0):
        self.re = re
        self.im = im
        
    def neg(self):
        return Complex(-self.re, -self.im)
    
    def sum(self, other):
        return Complex(self.re+other.re, self.im+other.im)
    
    def sub(self, other):
        return Complex(self.re-other.re, self.im-other.im)
    
    def mul(self, other):
        return Complex(self.re*other.re - self.im*other.im,
                       self.re*other.im + self.im*other.re)
        
    def abs(self):
        return math.sqrt(math.pow(self.re, 2)+math.pow(self.im,2))
    
    def toString(self):
        return 'Complex(%r, %r)' % (self.re, self.im)
    
c=Complex(3,5)
print(c.toString())
print('Neg of {} = {}'.format(c.toString(),c.neg().toString()))
print('Moduel of {} = {}'.format(c.toString(),c.abs()))


other=Complex(2,1)
print('{}+{}= {}'.format(c.toString(),other.toString(),c.sum(other).toString()))  
print('{}-{}= {}'.format(c.toString(),other.toString(),c.sub(other).toString()))  
print('{}*{} = {}'.format(c.toString(),other.toString(),c.mul(other).toString()))
    
    
    