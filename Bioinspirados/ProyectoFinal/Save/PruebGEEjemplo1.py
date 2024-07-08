class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None 

    def add_child(self, child_node):
        child_node.parent = self  
        self.children.append(child_node)

    def get_child(self, index):
            return self.children[index]

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.data) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret
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

if __name__ == "__main__":
    chromosome = [2,12,7,9,3,15,23,1,11,4,6,13,2,7,8,3,35,19,2,6]        
    struct={
        "e":[["e","o", "e" ], ["v"]],
        "o":[["+"], ["-"]],
        "v":[["0.5"], ["5"]]
    }  
    hojas=["0.5","5", "+","-"] 
    nodos=["e","o"]

    #Creamos la raiz de nuestro arbol
    keyTemp = "e"
    raiz = TreeNode(keyTemp)
    actual = raiz

    for i in range(len(chromosome)):
        #Obtenemos el modulo
        mod = chromosome[i] %2
        nivelOpciones = struct[keyTemp]
        newChild = nivelOpciones[mod]
        keyTemp = newChild[0]
        #Insertamos el nodo actual
        nodoTemp = TreeNode(newChild[0])
        actual.add_child(nodoTemp)
        restante = newChild[1:]
        if len(restante)>0:
            for j in range(len(restante)):
                nodo = TreeNode(restante[j])
                actual.add_child(nodo)
        print(f"Arbol  actual cromosama {i} de {len(chromosome)}")
        print(raiz)
        if nodoTemp.data in hojas:
            #regresamos al sigueinte nodo libre
            while True:
                keyTemp = nodoTemp.data
                temp = nodoTemp.parent
                if nodoTemp.parent !=None:
                    if temp.data in nodos and len(temp.children)>1:
                        print("Moiendo a otro nodo")
                        index =  [i for i, child in enumerate(temp.children) if len(child.children) == 0 ]
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









