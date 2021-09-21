# Author: Annabel Revers
# Date:   August 2021

from decimal import *

class OffByOne(object):
    
    def __init__(self,i):
        self.__initial = i
        self._upper = Decimal(i)
        self._lower = Decimal(i)
        self._prec = 1
    
    def __add__(self,y):
        return MyAdd(self,y,True)
    
    def __sub__(self,y):
        return MyAdd(self,y,False)
    
    def __mul__(self,y):
        return MyMult(self,y)
    
    def __repr__(self):
        # keep calculating bounds with increasing precision until they are within one of each other
        while (self._upper - self._lower) > 1:
            self.bounds_with_precision(self._prec + 1)
            
        # return lower bound rounded up to nearest int
        getcontext().rounding = ROUND_CEILING
        while True:
            try:
                res = int(self._lower.quantize(Decimal(1)))
                break # break out of while True loop
            except InvalidOperation:    
                pass
            self.bounds_with_precision(self._prec+1)
        return res.__repr__()
    
    # returns the lower and upper-bound Decimal value
    def bounds_with_precision(self,prec):
        # update precision
        self._prec = prec
        return self._lower,self._upper

class MyAdd(OffByOne):
    def __init__(self,left,right,isadd):
        self.__left = left
        self.__right = right
        self.__isadd = isadd
        self._upper = None
        self._lower = None
        self._prec = None

    def __repr__(self):
        # initialize boundaries
        self.initialize()
        # return lower bound rounded up to nearest int
        getcontext().rounding = ROUND_CEILING
        while True:
            try:
                res = int(self._lower.quantize(Decimal(1)))
                break # break out of while True loop
            except InvalidOperation:    
                pass
            self.bounds_with_precision(self._prec+1)
        return res.__repr__()
    
    # returns the lower and upper-bound Decimal value
    def bounds_with_precision(self,prec):
        # recalculate left and right boundaries if we are using greater prec
        if self._prec != None and prec > self._prec:
            # recalculate left bounds 
            self.__left.bounds_with_precision(self._prec)
            # recalculate right bounds
            self.__right.bounds_with_precision(self._prec)
        # set precision
        self._prec = prec
        getcontext().prec = prec
        # calculate upper and lower bounds
        if self.__isadd: # addition
            getcontext().rounding = ROUND_CEILING
            self._upper = self.__left._upper + self.__right._upper
            getcontext().rounding = ROUND_FLOOR
            self._lower = self.__left._lower + self.__right._lower
        else: # subtraction
            getcontext().rounding = ROUND_CEILING
            self._upper = self.__left._upper - self.__right._upper
            getcontext().rounding = ROUND_FLOOR
            self._lower = self.__left._lower - self.__right._lower
   
    # initializes boundaries
    def initialize(self):
        # intialize left if it is none
        if (self.__left._upper == None):
            self.__left.initialize()
        # intialize right if it is
        if (self.__right._upper == None):
            self.__right.initialize()
        # set initial boundaires with prec of 1
        self.bounds_with_precision(1)
        # keep calculating bounds with increasing precision until they are within one of each other
        while (self._upper - self._lower) > 1:
            self.bounds_with_precision(self._prec + 1)   
    
class MyMult(OffByOne):
    def __init__(self,left,right):
        self.__left = left
        self.__right = right
        self._upper = None
        self._lower = None
        self._prec = None

    def __repr__(self):
        # initialize boundaries
        self.initialize()
        # return lower bound rounded up to nearest int
        getcontext().rounding = ROUND_CEILING
        while True:
            try:
                res = int(self._lower.quantize(Decimal(1)))
                break # break out of while True loop
            except InvalidOperation:    
                pass
            self.bounds_with_precision(self._prec+1)
        return res.__repr__()
        
    # returns the lower and upper-bound Decimal value
    def bounds_with_precision(self,prec):
        # recalculate left and right boundaries if we are using greater prec
        if self._prec != None and prec > self._prec:
            # recalculate left bounds 
            self.__left.bounds_with_precision(self._prec)
            # recalculate right bounds
            self.__right.bounds_with_precision(self._prec)
        # set precision
        self._prec = prec
        getcontext().prec = prec
        # calculate upper and lower bounds
        getcontext().rounding = ROUND_CEILING
        self._upper = min(self.__left._lower*self.__right._lower, self.__left._upper*self.__right._lower, 
            self.__left._lower*self.__right._upper, self.__left._upper*self.__right._upper)
        getcontext().rounding = ROUND_FLOOR
        self._lower = min(self.__left._lower*self.__right._lower, self.__left._upper*self.__right._lower, 
            self.__left._lower*self.__right._upper, self.__left._upper*self.__right._upper)

    # initializes boundaires
    def initialize(self):
        # intialize left if it is none
        if (self.__left._upper == None):
            self.__left.initialize()
        # initialize right if it is none
        if (self.__right._upper == None):
            self.__right.initialize()
        # initialize bounds with precision of 1
        self.bounds_with_precision(1)
        # keep calculating bounds with increasing precision until they are within one of each other
        while (self._upper - self._lower) > 1:
            self.bounds_with_precision(self._prec+1)

        
    


    
      
