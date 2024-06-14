from binarytree import Node,build
from itertools import combinations
from TreeC import TreeC
import numpy as np
import random
import copy
import math
class PGenetica:

    def __init__(self,X_true,y_true):
        print("Programacion Genetica")
        self.operators = ["+", "-", "*", "/"]
        self.variables = ["X"]
        self.functions = ["sin", "cos", "tan"]
        self.constants = [str(random.randint(1, 10)) for _ in range(10)]
        self.X_true = X_true
        self.y_true = y_true
        self.objTree = TreeC()


    def generatePoblacionAleatoria(self, poblacionSize = 4):
        poblacion = []
        for i in range(poblacionSize):
            Tree = self.objTree.build(3)
            expresion,y_predict,mse =self.generateInfo(Tree)
            poblacion.append({"tree":Tree, "expresion":expresion,"y_predict":y_predict,"mse":mse})
        poblacion = sorted(poblacion, key=lambda x: x['mse'])
        return poblacion
    
    def generateInfo(self, Tree):
        expresion,y_predict,mse = None,None,None
        try:
            expresion =  self.objTree.generateExpressionV2(Tree)
            # print(Tree)
            # print(expresion)
            if expresion == None:
                return None, None,None
            y_predict = [self.evaluar_expresion(expresion, x) for x in self.X_true]
            mse = self.calcular_ecm(self.y_true, y_predict)
            return expresion,y_predict,mse
        except Exception as e:
            print(f"Error generatingInfo {e}")
            return expresion,y_predict,mse  

    def ListBuilld(self,individuo):
        return build(individuo)

    def generate_random_expression(self):
        # # return [ random.choice(self.operators + self.variables  + self.constants + self.operators +self.functions) for _ in range(size)]
        order = ['operator', 
                 'operator','operator', 
                 'operator', 'operator',
                 'operator' ,'operator',
                 'constant', 'variable' ,
                 'constant', 'constant' ,
                 'constant','variable',
                 'constant','variable']
        expression = []
        for item in order:
            if item == 'operator':
                expression.append(random.choice(self.operators))
            elif item == 'variable':
                expression.append(random.choice(self.variables))
            elif item == 'constant':
                expression.append(random.choice(self.constants))
            elif item == 'function':
                expression.append(random.choice(self.functions))
            else:
                expression.append(None)
        return expression
    
    def calcular_ecm(expresion, y_true,y_pred):
        return  np.mean((y_true - y_pred) ** 2)
    
    def MSE(y, y_):
        m = y.shape[0]
        mse = 0
        for i in range(m):
            mse += (y[i] - y_[i]) ** 2
        return round(mse / m, 2)
    
    def generateGeneration(self,poblacion):
        newGeneracion = []
        try:
            #Obtenemos los padres.... Revisar como realizar ruleta u otro metodo
            #Generamos permuitacion
            pos = list(range(len(poblacion)))
            combinacion = list(combinations(pos, 2))
            isTypeEquals = True
            node1 = None
            node2 = None
            for i in range(len(poblacion)):

                posiblePadres = [j for j in combinacion if i not in j]
                padres = posiblePadres[0]

                #Realizando la cruza
                p1 = poblacion[padres[0]]
                p2 = poblacion[padres[1]]
                
                #Aqui valido si la cruza se realiza sobre los mismos tipos de nodods
                while isTypeEquals:
                    node1 = self.seleccionNode(p1["tree"])
                    node2 = self.seleccionNode(p2["tree"])
                    isTypeEquals = self.validarTipo(node1[1].value,node2[1].value)

                hijo1 = copy.deepcopy(p1["tree"])
                hijo2 = copy.deepcopy(p2["tree"])
                """Realizando la cruza"""
           
                hijo1[node1[0]] = node2[1]
                hijo2[node2[0]] = node1[1]
           
                """Falta validar la profundidad"""
                expresion,y_predict,mse =self.generateInfo(hijo1)
                expresion2,y_predict2,mse2 =self.generateInfo(hijo2)

                elMejor = copy.deepcopy(hijo1)
                if mse2 ==  None and mse != None :
                    newGeneracion.append({"tree":elMejor, "expresion":expresion,"y_predict":y_predict,"mse":mse})
                    continue

                if mse2 !=  None and mse == None :
                    elMejor = copy.deepcopy(hijo2)
                    newGeneracion.append({"tree":elMejor, "expresion":expresion2,"y_predict":y_predict2,"mse":mse2})
                    continue
                    
                if mse2 ==  None and mse == None :
                    newGeneracion.append(p1)
                    continue

                if mse2<mse:
                    elMejor = copy.deepcopy(hijo2)
                    expresion = expresion2
                    y_predict = y_predict2
                    mse = mse2
                """Realizando la Muta"""
                elMejor =self.generateMuta(elMejor)   
                newGeneracion.append({"tree":elMejor, "expresion":expresion,"y_predict":y_predict,"mse":mse})
            return newGeneracion
        except Exception as e:
            print("Error: " + str(e))
            return newGeneracion

    def seleccionNode(self,Tree):
        opciones =  [ (indice, elemento) for indice, elemento in enumerate(Tree) if elemento is not None and indice != 0] 
        return random.choice(opciones)
    

    def generateMuta(self,Tree):
        try:
            print("Iniciamos la Muta Este es el mejor")
            # mutaTree = copy.deepcopy(Tree)
            mutaTree = Tree
            node = self.seleccionNode(mutaTree)
            value = node[1].value
            temp = None        
            #Verficamos si esl valor es un numero un operador o una funcion
            if value.isdigit():
                temp = [str(numero) for numero in range(10) if str(numero) != value]
            elif value in self.operators:
                temp = self.operators
            elif value in self.functions:
                temp = self.functions
            else:
                print("El value no encontraod")
            if value != "X":
                posibles = [temp[i] for i in range(len(temp)) if temp[i] != value]
                nuevoValue = random.choice(posibles)
                for i, node in enumerate(mutaTree):
                    print(f"Índice {i}: {node.value}")
                    if i == node[0]:
                        node.value = nuevoValue 
                # mutaTree[node[0]].value = nuevoValue
                # list(Tree)[node[0]].value = nuevoValue
            return mutaTree
        except Exception as e:
            print("Error en generar muta: " + str(e))
            return mutaTree
    
    def validarTipo(self, valueN1, valueN2):
        # print(valueN1,valueN2)
        if valueN1.isdigit() and valueN2.isdigit() or  valueN1 == "X" and valueN2.isdigit()  or   valueN1.isdigit() and valueN2 == "X"  :
            return False
        if  valueN1 in self.operators and  valueN2 in self.operators:
            return False
        if valueN1 in self.functions and valueN2 in self.functions:
            return False
        return True
    
    
    def evaluar_expresion(self, expresion,X):
        try:
            return eval(expresion, {'sin': math.sin, 'cos': math.cos, 'tan': math.tan,"X": X})
        except ZeroDivisionError:
            return -1
        except:
            return "Error: Expresión inválida"
