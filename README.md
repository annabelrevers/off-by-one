# Off By One

OffByOne is a number object for doing arbitrary precision calculations. Python already has a library for this, called Decimal, which has some caveats:

```
from decimal import *
getcontext().prec = 6 # Set the precision to 6 decimal digits (pretty low, 28 is the default)
getcontext().rounding=ROUND_CEILING # round towards infinity
Decimal(1)/Decimal(3)-10**10+10**10 # will yield 10000 (not 1 / 3)
getcontext().rounding=ROUND_FLOOR # round towards zero
Decimal(1)/Decimal(3)-10**10+10**10 # will yield -0
```

The right answer is in between ROUND_FLOOR and ROUND_CEILING, but neither of these is even close to the right answer 0.333333. 

OffByOne is mutable in implementation on the inside, but immutable in how it exposes itself to the outside world. Every numerical answer calculated using the object is always within 1 of the correct answer because upper bound and lower bounds are consistently computed throughout the calculation.

Example: try ```(OffByOne(‘3’) + OffByOne(‘0.25’) – OffByOne(‘10000000000’) + OffByOne(‘10000000000’)) * OffByOne(‘3’)```

You will see how the answer is far more precise than if you used Python’s Decimal class.

