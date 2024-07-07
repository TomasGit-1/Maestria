from TreeNode import TreeNode
import random

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


# "network":[["hiddenNeurons"], ["outputNeurons"]],
struct ={
    "hiddenNeurons":[["hiddenNeuron"], ["hiddenNeuron","_","hiddenNeurons"]],
    "hiddenNeuron":[["func", "weight", "@i0",",","inputs","#","outputs"],["func", "weight", "@i0",",","inputs","#","outputs"]],
    "func":[["LS"], ["HT"],["SN"],["GS"],["LN"],["HL"],["LR"]],
    "inputs":[["input"], ["input",",","inputs"]],
    "outputs":[["output"], ["output",",","outputs"]],
    "input":[["weight", "@", "inputID"],["weight", "@", "inputID"]],#sOLO TENGO 0 O 1 mODIFICAMOS AQUI  
    "output":[["weight", "@" ,"outputID"],["weight", "@" ,"outputID"]],#sOLO TENGO 0 O 1
    "inputID":[["i1|..|iN"],["i1|..|iN"]],
    "outputID":[["o1|..|oM"],["o1|..|oM"]],
    "weight":[["sign","digitList",".","digitList"],["sign","digitList",".","digitList"]],
    "sign":[["+"], ["-"]],
    "digitList":[["digit"], ["digit","digitList"]],
    "digit":[["0"],["1"],["2"],["3"],["4"],["5"],["6"],["7"],["8"],["9"]] #Tener cuidado generarlo manualemnte
}

chromosome = [2,1,7,9,3,15,23,1,11,4,6,13,1232,2132,3344,5,56,6,56,4,6,13,1232,2132,3344,5,56,6,56,2,1,7,9,3,15,23,1,11,4,6,13,1232,2132,3344,5,56,6,56,4,6,13,1232,2132,3344,5,56,6,56]     
hojas=["0","1","2","3","4","5","6","7","8","9", "+","-","@i0","#","@",".","i1|..|iN","o1|..|oM",",","LS","HT","SN","GS","LN","HL","LR"] 
nodos=["hiddenNeuron","func","inputs","outputs","input","output","inputID","outputID","weight","sing","digitList","digit"]


#Creamos la raiz de nuestro arbol
keyTemp = "hiddenNeurons"
raiz = TreeNode(keyTemp)
actual = raiz

for i in range(len(chromosome)):
    #Obtenemos el modulo
    mod = chromosome[i]%2
    nivelOpciones = struct[keyTemp]
    newChild = nivelOpciones[mod]
    keyTemp = newChild[0]
    #Insertamos el nodo actual
    if actual.data =="digit":
        newChild[0] = str( random.randint(0, 9))
    
    nodoTemp = TreeNode(newChild[0])
    actual.add_child(nodoTemp)
    restante = newChild[1:]
    if len(restante)>0:
        for j in range(len(restante)):
            # if restante[j] =="@i0":
            #     restante[j] = round(random.random(),2)
            nodo = TreeNode(restante[j])
            actual.add_child(nodo)
    print(f"Arbol  actual cromosama {i} de {len(chromosome)}")
    print(raiz)
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










    

