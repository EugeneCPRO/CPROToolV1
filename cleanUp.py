
# class for cleaning up strings


import re
import ast


class cleanUp(object):
        def __init__(self, price, balance, value):
            self.price = price
            self.balance = balance
            self.value = value

# clear terminal
def wipe():
    print("\033c",end="")



        

