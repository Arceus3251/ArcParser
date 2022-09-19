import random
from math import sqrt

GRAMMAR = """
@@grammar::CALC
start = expression $ ;

expression
    =
    | left:expression op:('+'|'-') ~ right:term
    | term
    ;
    
term
    =
    | left:term op:('*'|'/') ~ right:exponent
    | exponent
    ;

exponent
    =
    | left:dice op:'^' ~ right:exponent
    | op:'sqrt' '(' mid:expression ')'
    | dice
    ;

dice
    =
    | left:dice op:/[d]+/ ~ right:uniary
    | uniary
    ;

uniary
    =
    | op:'-' '(' mid:expression ')'
    | factor
    ;
    
factor
    =
    | '(' ~ @:expression ')'
    | number
    ;
    
number = /\d+/;
"""

class DiceSemantics:
    def number(self, ast):
        return int(ast)

def operate(left: int, op: str, right: int, dice_list: list[list[int]]) -> int:
    if op == "+":
        return left + right
    elif op == "-":
        return left - right
    elif op =="*":
        return left * right
    elif op =="/":
        return left / right
    elif op =="d":
        return dice_parse(left, right, dice_list)
    elif op == "^":
        return left**right

def calculate(input: dict, dice_list: list[list[int]]) -> int:
    if 'right' not in input:
        if input.get('op') == 'sqrt':
            if type(input.get('mid')) == dict:
                input.update({'mid':calculate(input.get('mid'), dice_list)})
            return sqrt(input.get('mid'))
        if input.get('op') == '-':
            if type(input.get('mid')) == dict:
                input.update({'mid':calculate(input.get('mid'), dice_list)})
            return -1*(input.get('mid'))
        
    if type(input.get('left')) == dict:
        input.update({'left':calculate(input.get('left'), dice_list)})
    if type(input.get('right')) == dict:
        input.update({'right':calculate(input.get('right'), dice_list)})
    return operate(input.get('left'), input.get('op'), input.get('right'), dice_list)

def dice_parse(amount: int, sides: int, dice_list: list[list[int]]) -> int:
    s = []
    sum = 0
    for _ in range(amount):
        currVal = random.randint(1, sides)
        s.append(currVal)
        sum += currVal
    dice_list.append(s)
    return sum