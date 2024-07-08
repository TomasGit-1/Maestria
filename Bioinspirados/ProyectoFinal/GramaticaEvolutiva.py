from TreeNode import TreeNode
import random
import numpy as np
import copy


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

def ordenar(vector):
    return  sorted(vector, key= lambda x: x.fitness , reverse=True)

def mutate(vector, mutation_rate=0.01):
    # Iterar sobre cada gen en el vector
    for i in range(len(vector)):
        # Mutar con cierta probabilidad
        if random.random() < mutation_rate:
            # Generar un nuevo valor aleatorio para el gen
            vector[i] = random.randint(0, 255)
    return vector

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1.vector) - 1)
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)
    # child1.fitness = float("inf")
    # child2.fitness = float("inf")
    child1.vector  = np.concatenate([parent1.vector[:point], parent2.vector[point:]])
    child2.vector  = np.concatenate([parent2.vector[:point], parent1.vector[point:]])
    return child1, child2

def generateGeneration(population):
    # half_size = len(population) // 2
    # padres  = population[:half_size]
    new_population = []
    while len(new_population) < len(population):
        parent1, parent2 = random.choices(population, k=2)
        child1, child2 = crossover(parent1, parent2)
        child1.vector = mutate(child1.vector)
        child2.vector = mutate(child2.vector)
        new_population.append(child1)
        new_population.append(child2)
    return new_population

def obtenerConfig(vector):
    #Primer poso recorremos hasta encontrar le #
    hiidenNeuronsTemp ="".join(vector).split("hiddenNeurons")
    for i in range(len(hiidenNeuronsTemp)):
        hiidenNeuronsTemp[i] = hiidenNeuronsTemp[i].split("#")
    pass




def GenotipoaFenotipo(nameRaiz, genotipo,hojas,nodos,struct,numeroNeuronas=0):
    try:
        #Creamos la raiz de nuestro arbol
        keyTemp = nameRaiz
        raiz = TreeNode(keyTemp)
        actual = raiz
        neuronsCont = 0 
        for i in range(len(genotipo)):
            
            #Obtenemos el modulo
            mod = genotipo[i]%2
            nivelOpciones = struct[keyTemp]
            newChild = nivelOpciones[mod]
            keyTemp = newChild[0]
            #Insertamos el nodo actual
            if actual.data =="digit":
                newChild[0] = str( random.randint(0, 9))

            # if actual.data =="inputID":
            #     newChild[0] = str(neuronsCont)
            #     neuronsCont =+1
            
            nodoTemp = TreeNode(newChild[0])
            actual.add_child(nodoTemp)
            restante = newChild[1:]
            if len(restante)>0:
                for j in range(len(restante)):
                    nodo = TreeNode(restante[j])
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
                            print("Moiendo a otro nodo")
                            index =  [i for i, child in enumerate(temp.children) if len(child.children) == 0 and  child.data not in hojas]
                            if len(index)>0:
                                temp = temp.get_child(index[0])
                                keyTemp = temp.data
                                nodoTemp = temp
                                break
                            else:
                                print("No se encontro vacios no movemos un niovel ams")
                    else:
                        nodoTemp = raiz  
                        break
                    nodoTemp = temp
            keyTemp = nodoTemp.data
            actual = nodoTemp
        result = inorder_traversal(raiz)
        print("\nRecorrido inorder:")
        print(result)
        obtenerConfig(result)
        return result
    except Exception as e:
        print(f"Error en generar fenotipo {str(e)}")


def hiidenNeurons():
    struct ={
        "hiddenNeurons":[["hiddenNeuron"], ["hiddenNeuron","_","hiddenNeurons"]],
        "hiddenNeuron":[["func", "weight", "@i0",",","inputs","#","outputs"],["func", "weight", "@i0",",","inputs","#","outputs"]],
        "func":[["LS"], ["HT"],["SN"],["GS"],["LN"],["HL"],["LR"]],
        "inputs":[["input"], ["input",",","inputs"]],
        "outputs":[["output"], ["output",",","outputs"]],
        "input":[["weight", "@", "inputID"],["weight", "@", "inputID"]],#sOLO TENGO 0 O 1 mODIFICAMOS AQUI  
        "output":[["weight", "@" ,"outputID"],["weight", "@" ,"outputID"]],#sOLO TENGO 0 O 1
        "inputID":[["iN"],["iN"]],
        "outputID":[["oM"],["oM"]],
        "weight":[["sign","digitList",".","digitList"],["sign","digitList",".","digitList"]],
        "sign":[["+"], ["-"]],
        "digitList":[["digit"], ["digit","digitList"]],
        "digit":[["0"],["1"],["2"],["3"],["4"],["5"],["6"],["7"],["8"],["9"]] #Tener cuidado generarlo manualemnte
    }
    hojas=["0","1","2","3","4","5","6","7","8","9", "+","-","@i0","#","@",".","iN","oM",",","LS","HT","SN","GS","LN","HL","LR"] 
    nodos=["hiddenNeuron","func","inputs","outputs","input","output","outputID","inputID","weight","sing","digitList","digit"]
    return struct,hojas,nodos

def outputNeurons():
    struct ={
        # "hiddenNeurons":[["hiddenNeuron"], ["hiddenNeuron","_","hiddenNeurons"]],
        "outputNeurons":[["func", "weight", "@i0"],["outputNeurons"]],
        # "outputNeurons":[["func", "weight", "@i0","_.._","func", "weight", "@i0"]],
        "func":[["LS"], ["HT"],["SN"],["GS"],["LN"],["HL"],["LR"]],
        "weight":[["sign","digitList",".","digitList"],["sign","digitList",".","digitList"]],
        "sign":[["+"], ["-"]],
        "digitList":[["digit"], ["digit","digitList"]],
        "digit":[["0"],["1"],["2"],["3"],["4"],["5"],["6"],["7"],["8"],["9"]] #Tener cuidado generarlo manualemnte
    }
    hojas=["0","1","2","3","4","5","6","7","8","9", "+","-","@i0","#","@",".","i1|..|iN","o1|..|oM",",","LS","HT","SN","GS","LN","HL","LR"] 
    nodos=["hiddenNeuron","func","inputs","outputs","input","output","inputID","outputID","weight","sing","digitList","digit"]
    return struct,hojas,nodos

def performMappingProcess(population):

    struct,hojas,nodos = hiidenNeurons()
    for individuo in population:
        genotipo = individuo.vector
        hnConfg = GenotipoaFenotipo(nameRaiz = "hiddenNeurons",
                                    genotipo = genotipo, 
                                    hojas = hojas,
                                    nodos = nodos, 
                                    struct = struct)
        print(hnConfg)
    # struct,hojas,nodos = outputNeurons()
    # onConfig = GenotipoaFenotipo(nameRaiz = "outputNeurons",genotipo = genotipo, hojas = hojas,nodos = nodos, struct = struct, numeroNeuronas = M)
    
    # network = [hnConfg, onConfig]
    pass
                

