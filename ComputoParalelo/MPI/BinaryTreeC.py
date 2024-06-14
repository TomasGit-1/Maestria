import random
from binarytree import Node,build

# class Node:
#     def __init__(self, value):
#         self.value = value
#         self.left = None
#         self.right = None

class TreeC:
    def build(self, profundidad_maxima):
        if profundidad_maxima == 0:
            # Cuando llegamos a la profundidad máxima, creamos una hoja con un número aleatorio
            return Node(random.choice([str(random.randint(1, 10)), 'X']))
        else:
            # En niveles internos, seleccionamos un operador o función trigonométrica
            raiz = Node(random.choice(['+', '-', '*', '/', 'sin', 'cos']))
            if raiz.value in ['sin', 'cos', 'tan']:
                raiz.left = None
                raiz.right = self.build(profundidad_maxima - 1)
            else:
                raiz.left = self.build(profundidad_maxima - 1)
                raiz.right = self.build(profundidad_maxima - 1)
            return raiz
    def imprimir_arbol(self, raiz, nivel=0):
        if raiz is not None:
            if isinstance(raiz.value, int) or raiz.value == 'X':
                print("    " * nivel + str(raiz.value))
            else:
                print("    " * nivel + raiz.value)
            self.imprimir_arbol(raiz.left, nivel + 1)
            self.imprimir_arbol(raiz.right, nivel + 1)
        

objTree = TreeC()
Tree = objTree.build(3)
print(Tree)
for i, node in enumerate(Tree):
    print(f"Índice {i}: {node.value}")
    if i == 3:
        # print(node.value)
        node.value = 330303    
# nodo_en_posicion_3 = Tree[3]
print(Tree)
# print("Árbol generado aleatoriamente:")
# objTree.imprimir_arbol(Tree)
# print(Tree)