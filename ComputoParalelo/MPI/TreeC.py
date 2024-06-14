from binarytree import Node
import random
import math

class TreeC:
    def build(self, profundidad_maxima):
        if profundidad_maxima == 0:
            # Cuando llegamos a la profundidad máxima, creamos una hoja con un número aleatorio
            return Node(random.choice([str(random.randint(1, 10)), 'X']))
        else:
            # En niveles internos, seleccionamos un operador o función trigonométrica
            raiz = Node(random.choice(['+', '-', '*', '/', 'sin', 'cos']))
            if raiz.value in ['sin', 'cos', 'tan']:
                raiz.left = self.build(profundidad_maxima - 1)
                raiz.right = self.build(profundidad_maxima - 1)
            else:
                raiz.left = self.build(profundidad_maxima - 1)
                raiz.right = self.build(profundidad_maxima - 1)
            return raiz
    
    def generateExpressionV2(self,tree):
        try:
            if tree is None:
                return ''
            if tree.left is None and tree.right is None:
                return tree.value
            
            expresion_izquierda = self.generateExpressionV2(tree.left)
            if expresion_izquierda == None:
                expresion_izquierda ==""
            expresion_derecha = self.generateExpressionV2(tree.right)
            if expresion_derecha == None:
                expresion_derecha ==""
            if tree.value in ('+', '-', '*', '/'):
                expresion_actual = '(' + expresion_izquierda + tree.value + expresion_derecha + ')'
                return expresion_actual

            elif tree.value.lower() in ('sin', 'cos', 'tan'):
                expresion_actual = tree.value.lower() + '(' + expresion_izquierda + ')'
                return expresion_actual
            else:
                expresion_actual = None
            #     print("Operador no válido: {}".format(tree.value))
        except Exception as e:
            print("Error: {}".format(e))
            expresion_actual = ""
    
    def generateExpressionV1(self, Tree):
        expression = [ Tree.inorder[i].values[0] for i in range(len(Tree.inorder))]
        detectarC3 = 0
        expresionFull = ""
        for i in range(len(expression)):
            if detectarC3 == 0:
                expresionFull += "("
            if detectarC3 == 3:
                expresionFull += ")"
                expresionFull += expression[i] 
                detectarC3 = 0
            else:
                expresionFull += expression[i] 
                detectarC3 +=1
        return expresionFull+")"

    def cortar_Tree(self, Tree, profundidad_deseada, profundidad_actual=0):
        if Tree is None or profundidad_actual == profundidad_deseada:
            return None        
        Tree.izquierda = self.cortar_Tree(Tree.izquierda, profundidad_deseada, profundidad_actual + 1)
        Tree.derecha = self.cortar_Tree(Tree.derecha, profundidad_deseada, profundidad_actual + 1)
        return Tree

