import numpy as np 
from TreeNode import TreeNode
import random
from itertools import chain

def formateList(data):
    formatted_list = []
    for el in data:
        formatted_list.append(el)
        formatted_list.append(["|"])
    if formatted_list:
        formatted_list.pop()
    return formatted_list
N= 4
M = 3

inputID = [[f"@i{n}"]  for n in range(1, N+1)]
outputID = [[f"o{m}"] for m in range(1, M+1)]
hojas=["0","1","2","3","4","5","6","7","8","9", "+","-","_",":","[]","@i0","#","@",".","iN","oM",",","LS","HT","SN","GS","LN","HL","LR"] 
hojas.extend(inputID)
hojas.extend(outputID)
hojas = [item[0] if isinstance(item, list) else item for item in hojas]

nodos=["<network>","<hiddenNeurons>","<outputNeurons>","<hiddenNeuron>","<func>","<inputs>","<outputs>","<input>","<output>","<outputID>","<inputID>","<weight>","<sign>","<digitList>","<digit>"]

inputID = formateList(inputID)
outputID = formateList(outputID)

outputNeuronsStruct = [["<func>",":", "<weight>","@i0","_"][:] for _ in range(M)]
outputNeuronsStruct = sum(outputNeuronsStruct, [])

struct ={
    "<network>":[["<hiddenNeurons>"],"[]",["<outputNeurons>"]],
    "<hiddenNeurons>":[["<hiddenNeuron>"],["|"],["<hiddenNeuron>","_","<hiddenNeurons>"]],
    "<hiddenNeuron>":["<func>",":", "<weight>", "@i0",",","<input>","#","<outputs>"],
    "<outputNeurons>":outputNeuronsStruct,
    # "<outputNeurons>":[["<func>: <weight> @i0_.._<func>: <weight> @i0"]],
    "<func>":[["LS"],["|"], ["HT"],["|"],["SN"],["|"],["GS"],["|"],["LN"],["|"],["HL"],["|"],["LR"]],
    "<inputs>":[["<input>"], ["<input>",",","<inputs>"]],
    "<outputs>":[["<output>"], ["<output>",",","<outputs>"]],
    "<input>":["<weight>","<inputID>"],
    "<output>":["<weight>","<outputID>"],
    "<inputID>":inputID,
    "<outputID>":outputID,
    "<weight>":["<sign>","<digitList>",".","<digitList>"],
    "<sign>":[["+"],["|"],["-"]],
    "<digitList>":[["<digit>"],["<digit>","<digitList>"]],
    "<digit>":[["0"],["|"],["1"],["|"],["2"],["|"],["3"],["|"],["4"],["|"],["5"],["|"],["6"],["|"],["7"],["|"],["8"],["|"],["9"]] #Tener cuidado generarlo manualemnte
}

def obtenerConfig(vector):
    #Primer poso recorremos hasta encontrar le #
    return "".join(vector).split("[]")
   


def inorder_traversal(node):
    result = []
    def traverse(node):
        if node is not None:
            # Recorrer todos los hijos
            for child in node.children:
                traverse(child)
            if not node.children:
                result.append(node.data)    
    traverse(node)
    return result

def GenotipoaFenotipo(nameRaiz, genotipo,N, M):
    try:
        #Creamos la raiz de nuestro arbol
        keyTemp = nameRaiz
        raiz = TreeNode(keyTemp)
        actual = raiz
        print(f"Arbol  actual ")
        print(raiz)
        posGenotipo =0
        for i in range(200):
            #Condicion para ocupar el codon
            sinOR = struct[keyTemp]
            newChild = sinOR
            if posGenotipo >len(genotipo):
                print("Se acabo los numeros")
                break
            if ["|"] in struct[keyTemp]:
                # print("Ocupamos un valor del genotipo")
                sinOR = [sublist for sublist in struct[keyTemp] if sublist != ['|']]
                newChild = sinOR
                mod = genotipo[posGenotipo]%len(sinOR)
                nivelOpciones = sinOR
                if len(sinOR) == 2:
                    #Esb imario
                    newChild = nivelOpciones[mod]
                    keyTemp = newChild[0]
                else:
                    eleccion = random.randint(0, len(sinOR)-1)
                    newChild = nivelOpciones[eleccion]
                    keyTemp = newChild[0]
                    pass
                
                posGenotipo =+1
            else:
                keyTemp = newChild[0]
            
            if isinstance(keyTemp, list):
                keyTemp = newChild[0][0]

            nodoTemp = TreeNode(keyTemp)
            actual.add_child(nodoTemp)
            restante = newChild[1:]
            if len(restante)>0:
                for j in range(len(restante)):
                    newNode = restante[j]
                    if isinstance(restante[j], list):
                        newNode = restante[j][0]
                    nodo = TreeNode(newNode)
                    actual.add_child(nodo)

            # print(f"Arbol  actual ")
            # print(raiz)
            if nodoTemp.data in hojas:
                #regresamos al sigueinte nodo libre
                while True:
                    keyTemp = nodoTemp.data
                    temp = nodoTemp.parent
                    if temp !=None:
                        if temp.data in nodos and len(temp.children)>1:
                            # print("Moiendo a otro nodo")
                            index =  [i for i, child in enumerate(temp.children) if len(child.children) == 0 and  child.data not in hojas]
                            if len(index)>0:
                                temp = temp.get_child(index[0])
                                keyTemp = temp.data
                                nodoTemp = temp
                                break
                            else:
                                pass
                                # print("No se encontro vacios no movemos un niovel ams")
                    else:
                        # index =  [i for i, child in enumerate(raiz.children) if len(child.children) == 0 and  child.data not in hojas]
                        nodoTemp = raiz  
                        break
                    nodoTemp = temp
            #Mantenemos en el nodo en el camnioo
            keyTemp = nodoTemp.data
            actual = nodoTemp
            if keyTemp == "<network>":
                #Nodos que aun no tienen hijos
                index =  [i for i, child in enumerate(actual.children) if len(child.children) == 0 and  child.data not in hojas]
                if index == []:
                    #Ya creamos      "<network>":[["<hiddenNeurons>"],"[]",["<outputNeurons>"]],
                    break
        result = inorder_traversal(raiz)
        print("\nConfiguracion:")
        config= obtenerConfig(result)
        print(config)
        return config
    except Exception as e:
        print(f"Error en generar fenotipo {str(e)}")



if __name__ == "__main__":
    genotipo = np.random.randint(low=1, high=55, size=100)
    hnConfg = GenotipoaFenotipo(nameRaiz = "<network>",
                                    genotipo = genotipo,N=2, M=3 )