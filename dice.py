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

def operate(var2: str, operator: str, var1: str, dList):
    outputVar = 0.0
    if operator == "+":
        outputVar = float(var1)+float(var2)
    elif operator == "-":
        outputVar = float(var1)-float(var2)
    elif operator == "*":
        outputVar = float(var1)*float(var2)
    elif operator == "/":
        outputVar = float(var1)/float(var2)
    elif operator == "d":
        return dice_parse(int(var1), int(var2), dList)
    if outputVar.is_integer(): return int(outputVar)
    return outputVar

def calculate(expression, dList):
    expression = expression.replace('["(",', "")
    expression = expression.replace(',")"]', "")
    expression = expression.replace('"', "")
    expression = expression.replace(",", "")

    data = []
    digitStack = []
    for e in expression:
        if e.isdigit():
            digitStack.append(e)
        elif e == "]":
            if len(digitStack)>0:
                num: str = ""
                for f in digitStack:
                    num = num + f
                data.append(num)
                digitStack = []
            
            new_data = operate(data.pop(), data.pop(), data.pop(), dList)
            data.pop()
            data.append(str(new_data))
        else:
            if len(digitStack)>0:
                num: str = ""
                for f in digitStack:
                    num = num + f
                data.append(num)
                digitStack = []
            data.append(e)
    return data[0]

def dice_parse(x:int, y:int, dList: list[list[int]]) -> int:
    s = []
    sum = 0
    for _ in range(x):
        currVal = random.randint(1, y)
        s.append(currVal)
        sum += currVal
    dList.append(s)
    return sum