from binarytree import Node
import random
import math

class TreeC:

    def construir(self,profundidad_maxima):
        if profundidad_maxima == 0:
            return Node(str(random.randint(1, 10)))
        else:
            raiz = Node(random.choice(['+', '-', '*', '/','sin','cos','tan']))
            raiz.left = self.construir(profundidad_maxima - 1)
            raiz.right = self.construir(profundidad_maxima - 1)
            return raiz
    
    def generar_expresion(self,tree):
        if tree is None:
            return ''
        if tree.left is None and tree.right is None:
            return tree.value
        
        expresion_izquierda = self.generar_expresion(tree.left)
        expresion_derecha = self.generar_expresion(tree.right)

        if tree.value in ('+', '-', '*', '/'):
            expresion_actual = '(' + expresion_izquierda + tree.value + expresion_derecha + ')'
        elif tree.value.lower() in ('sin', 'cos', 'tan'):
            expresion_actual = tree.value.lower() + '(' + expresion_izquierda + ')'
        else:
            raise ValueError("Operador no válido: {}".format(tree.value))
        return expresion_actual

objTree = TreeC()
tree = objTree.construir(3)
expresion = objTree.generar_expresion(tree)
resultado = eval(expresion, {'sin': math.sin, 'cos': math.cos, 'tan': math.tan})
print(tree)
print("Expresión generada:", expresion)



