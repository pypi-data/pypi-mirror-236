from dataclasses import dataclass
from turtle import right
from typing import Any
import tatsu

@dataclass
class __SpecialEvaluationValue:
    name: str 

ASK_INPUT = __SpecialEvaluationValue("ASK")

GRAMMAR = '''
    @@grammar::CALC


    start = expression $ ;


    expression
        =
        | left:expression op:'+' right:term
        | left:expression op:'-' right:term
        | left:term
        | left:special
        ;

    special = ask:'*' ;

    term
        =
        | left:term op:'*' right:factor
        | left:term op:'/' right:factor
        | left:factor
        ;


    factor
        =
        | '(' exp:expression ')'
        | num:number
        | identifier:identifier "(" args:expression_list ")"
        | identifier:identifier
        | string:string 
        ;

    expression_list = head:expression ["," tail:expression_list] ;

    number = /\d+\.?\d*/;
    identifier = /[a-zA-Z][a-zA-Z0-9]*/ ;
    string = /\"[^\"]*\"/ ;
'''


class Semantics:

    def __init__(self, identifiers, functions, instance=None) -> None:
        self.identifiers = identifiers
        self.functions = functions
        self.instance = instance

    def number(self, num):
        return float(num)
    def factor(self, ast):
        if ast.num is not None:
            return ast.num
        elif ast.identifier is not None:
            if ast.args is None:
                return ast.identifier 
            else:
                return ast.identifier(self, *ast.args)
        elif ast.string is not None:
            return ast.string
        else:
            return ast.exp 
    def term(self, ast):
        if ast.right is None:
            return ast.left 
        elif ast.op == "/":
            return float(ast.left) / float(ast.right)
        else:
            return float(ast.left) * float(ast.right)
    def expression(self, ast):
        if ast.right is None:
            return ast.left 
        elif ast.op == "+":
            return ast.left + ast.right 
        else:
            return ast.left - ast.right 
    def identifier(self, ast):
        return self.identifiers.get(ast, self.functions.get(ast, None))
    
    def expression_list(self, ast):
        if ast.tail is None:
            return [ast.head]
        return [ast.head] + ast.tail
    
    def string(self, ast):
        return ast[1:-1]
    
    def special(self, ast):
        if ast.ask is not None:
            return ASK_INPUT


def parse(input: str):
    return tatsu.parse(GRAMMAR, input)


FUNCTIONS = {}
def tpes_function(name=None):
    def wrap(f):
        FUNCTIONS[f.__name__ if name is None else name] = f
        return f 
    return wrap

tpes_function("sum")(lambda context, *l: sum(l))

@tpes_function()
def lineCount(context, path):
    count = 0
    for line in open(path):
        count += 1 
    return count

@tpes_function()
def document(context, name):
    return "%s/%s" % (context.instance.name, name)

@tpes_function("input")
def __input(context, name):
    return context.identifier(name)

def evaluate(input: str, semantics_class=Semantics, identifiers={"instance": 5}, instance=None):
    return tatsu.parse(GRAMMAR, input, semantics=semantics_class(identifiers, FUNCTIONS, instance))

class ExpressionEvaluator:
    def __init__(self, identifiers: dict[str, Any], instance = None) -> None:
        self.identifiers = identifiers
        self.instance = instance 
    
    def evaluate(self, input) -> Any:
        return evaluate(input, Semantics, self.identifiers, self.instance)