import random

GRAMMAR = """
@@grammar::CALC
start = expression $ ;

expression
    =
    | left:expression op:'+' ~ right:term
    | left:expression op:'-' ~ right:term
    | term
    ;
    
term
    =
    | left:term op:'*' ~ right:dice
    | left:term op:'/' ~ right:dice
    | dice
    ;

dice
    =
    | left:dice op:/[d]+/ ~ right:factor
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

def operate(left: int, op: str, right: int, dList: list[list[int]]) -> int:
    if op == "+":
        return left + right
    elif op == "-":
        return left - right
    elif op =="*":
        return left * right
    elif op =="/":
        return left / right
    elif op =="d":
        return dice_parse(left, right, dList)

def calculate(input: dict, dList: list[list[int]]) -> int:
    if type(input.get('left')) == dict:
        input.update('left', calculate(input.get('right')))
    if type(input.get('right')) == dict:
        input.update('right', calculate(input.get('right')))
    return operate(input.get('left'), input.get('op'), input.get('right'), dList)

def dice_parse(x:int, y:int, dList: list[list[int]]) -> int:
    s = []
    sum = 0
    for _ in range(x):
        currVal = random.randint(1, y)
        s.append(currVal)
        sum += currVal
    dList.append(s)
    return sum