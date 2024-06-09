from binarytree import Node,build
from TreeC import TreeC
import numpy as np
import random
import copy

class PGenetica:

    def __init__(self,X_true,y_true):
        print("Programacion Genetica")
        self.operators = ["+", "-", "*", "/"]
        self.variables = ["X"]
        self.functions = ["sin", "cos"]
        self.constants = [str(random.randint(1, 10)) for _ in range(10)]
        self.X_true = X_true
        self.y_true = y_true
        self.objTree = TreeC()


    def generatePoblacionAleatoria(self, poblacionSize = 4):
        poblacion = []
        for i in range(poblacionSize):
            nodes = self.generate_random_expression()
            Tree = self.ListBuilld(nodes)
            expresion,y_predict,mse =self.generateInfo(Tree)
            poblacion.append({"tree":Tree, "expresion":expresion,"y_predict":y_predict,"mse":mse})
        poblacion = sorted(poblacion, key=lambda x: x['mse'])
        return poblacion
    
    def generateInfo(self, Tree):
        expresion,y_predict,mse = None,None,None
        try:
            expresion = self.generateExpression(Tree)
            y_predict = [self.evaluar_expresion(expresion, x) for x in self.X_true]
            mse = self.calcular_ecm(self.y_true, y_predict)
            return expresion,y_predict,mse
        except Exception as e:
            print("Error generatingInfo")
            return expresion,y_predict,mse
    
    def generartePoblacionManual(self, poblacionSize = 4, data=None):   
        poblacion = []
        Trees = self.generateArboles()
        for i in range(4):
            expresion = self.generateExpression(Trees[i])
            poblacion.append({"tree":Trees[i], "expresion":expresion,"y":0})
            print(f"Arbol {Trees[i]} Expresion {expresion}")
            y_valores = [self.evaluar_expresion(expresion, 2) for x in data]
        return poblacion

    def generateExpression(self, Tree):
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
        #Obtenemos los padres.... Revisar como realizar ruleta u otro metodo
        padres = [(poblacion[i], poblacion[i+1]) for i in range(0, len(poblacion), 2)]
        poblacion = []
        for i in range(0, len(padres)):
            #Realizando la cruza
            p1 = padres[i][0]
            node1 = self.seleccionNode(p1["tree"])
            p2 = padres[i][1]
            node2 = self.seleccionNode(p2["tree"])

            hijo1 = copy.deepcopy(p1["tree"])
            hijo2 = copy.deepcopy(p2["tree"])
            #Cruza
            hijo1[node1[0]] = node2[1]
            hijo2[node2[0]] = node1[1]

            """Falta validar la profundidad"""

            #Muta
            hijo1 =self.generateMuta(hijo1)   
            expresion,y_predict,mse =self.generateInfo(hijo1)
            poblacion.append({"tree":hijo1, "expresion":expresion,"y_predict":y_predict,"mse":mse})   
            hijo2 =self.generateMuta(hijo2)
            expresion,y_predict,mse =self.generateInfo(hijo2)
            poblacion.append({"tree":hijo2, "expresion":expresion,"y_predict":y_predict,"mse":mse})

        return poblacion

    def seleccionNode(self,Tree):
        opciones =  [ (indice, elemento) for indice, elemento in enumerate(Tree) if elemento is not None and indice != 0] 
        return random.choice(opciones)
    
    def generateMuta(self,Tree):
        node = self.seleccionNode(Tree)
        value = node[1].value
        #Verficamos si esl valor es un numero un operador o una funcion
        temp = None
        
        if value.isdigit():
            temp = [str(numero) for numero in range(10)]
            value = int(value)
        elif value in self.operators:
            temp = self.operators
        elif value in self.functions:
            temp = self.functions
        else:
            print("El value no encontraod")
        if value != "X":
            posibles = [temp[i] for i in range(len(temp)) if temp[i] != value]
            nuevoValue = random.choice(posibles)
            Tree[node[0]].value = nuevoValue
        return Tree
    
    def evaluar_expresion(self, expresion,X):
        return eval(expresion)

