import random
from binarytree import Node,build
from math import *

def generar_expresion_aleatoria(niveles):
    operadores = ['+', '-', '*', '/']
    expresion = ''
    def generar_expresion_recursiva(nivel):
        nonlocal expresion
        if nivel == 0:
            expresion += str(random.randint(1, 10))
        else:
            expresion += '('
            generar_expresion_recursiva(nivel - 1)
            expresion += random.choice(operadores)
            generar_expresion_recursiva(nivel - 1)
            expresion += ')'
    generar_expresion_recursiva(niveles)
    return expresion

def evaluar_expresion(expresion):
    try:
        resultado = eval(expresion)
        return resultado
    except ZeroDivisionError:
        return "Error: División por cero"
    except:
        return "Error: Expresión inválida"

expresion = generar_expresion_aleatoria(3)
print("Expresión aleatoria generada:", expresion)
arbol = build(expresion)
print("Árbol binario:", arbol)
resultado = evaluar_expresion(expresion)
print("Resultado de la expresión:", resultado)
