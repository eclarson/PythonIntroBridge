from __future__ import print_function


class CalculatorError(ValueError):
    '''raise this when the user causes a mistake from the calculator'''

class Calculator:
    def __init__(self):
        
        import operator as oper
        # add dictionary of operations and function passing
        self.operations_list = {'+':oper.add,
                                '-':oper.sub,
                                '*':oper.mul,
                                '/':oper.truediv,
                                '^':oper.pow,
                                '%':oper.mod,
                               }
        self.eval_queue = []
       
    #==Queue Operations========
    def clear_queue(self):
        self.eval_queue = []
    
    def print_queue(self):
        print("Current Stack:", self.eval_queue)
        
    def addto_queue(self,value):
        tmp = self.convert_user_input(value)
        self.eval_queue.append( tmp )
    
        
        # evaluate operation if it was entered
        if self.isoperation(self.eval_queue[-1]):

            result = self.eval_queue.pop()
            
            if len(self.eval_queue)<2:
                # not enough elements to perform an operation
                raise CalculatorError('Not enough values to perform operation')
                
            v2 = self.eval_queue.pop()
            v1 = self.eval_queue.pop()

            result = calc.perform_operation(result,(v1,v2))
            self.eval_queue.append(result)
            
    def print_operations(self):
        # print supported operations
        print('Operations List:', end=' ')
        [print(x, end=', ') for x in self.operations_list.keys()]
        print('')
        
    #==check type Operations========
    def isoperation(self, value):
        if value in self.operations_list.keys():
            return True
        else:
            return False

    def isfloat(self, value):
        try:
            tmp = float(value)
            return True
        except ValueError:
            return False

    #===evalaute operations============
    def convert_user_input(self, value):
        if self.isfloat(value):
            return float(value)

        elif self.isoperation(value) :
            return value # leave as is and interpret operation later
        
        else:
            raise CalculatorError('Invalid entry. Entry must be number or supported operator.')

    def perform_operation(self, op,vals):
        if self.isoperation(op):
            return self.operations_list[op](vals[0],vals[1])
        return op


class Operator:
    def __init__(self, func, num_args=2):
        self.func = func
        self.num_args = num_args
    

    
class CustomCalculator(Calculator):
    def __init__(self):
        # THIS OVERWRITES THE INIT FUNCTION OF INHERITED CLASS
        import operator as oper
        # add dictionary of operations and function passing, include basic operations here
        self.operations_list = {'+':Operator(oper.add),
                                '-':Operator(oper.sub),
                                '*':Operator(oper.mul),
                                '/':Operator(oper.truediv),
                                '^':Operator(oper.pow),
                                '%':Operator(oper.mod),
                                'abs':Operator(oper.abs,num_args=1),
                               }
        self.eval_queue = []
        
    def add_custom_operations(self,filename):
        import json
        with open(filename) as file:
            data = json.loads(file.read()) # Grab file data

        import math
        for key,module in data.items():
            if hasattr(math, module):
                self.operations_list[key] = Operator(getattr(math, module), num_args = 1)
                
    def addto_queue(self,value):
        tmp = self.convert_user_input(value)
        self.eval_queue.append( tmp )
    
        
        # evaluate operation if it was entered
        if self.isoperation(self.eval_queue[-1]):

            result = self.eval_queue.pop()
            num_args = self.operations_list[result].num_args
            
            if len(self.eval_queue)<num_args:
                # not enough elements to perform an operation
                raise CalculatorError('Not enough values to perform operation')
                
            args = []
            for i in range(num_args):
                args.append(self.eval_queue.pop())

            result = self.perform_operation(result,args)
            self.eval_queue.append(result)
            
    def perform_operation(self, op, vals):
        if self.isoperation(op):
            return self.operations_list[op].func(*vals) # pass list as arguments
        return op
        
    