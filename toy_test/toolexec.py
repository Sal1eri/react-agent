def add(a, b):
    return a + b
def subtract(a, b):
    '''
    it is a math tool that subtracts two numbers.
    '''
    res = {'description': 'Subtracts the second number from the first number.'
     }
    res.update({'result': a - b})
    return res

tools = [add, subtract]
print(tools[1].__doc__)  # Output: 8
print(tools[1](5, 3))  # Output: 2