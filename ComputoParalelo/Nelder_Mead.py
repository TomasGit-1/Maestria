from random import random

def sphere(x):
    return sum(item**2 for item in x)

def createPop(dim,puntos):
    try:
        li, ls = -10, 10
        S = []
        for _ in range(puntos):
            p1 = [0]
            #Coordenadas
            p1.extend([ li + random() * (ls - li) for _ in range(dim)])
            #contiene el valor de la función de esfera
            p1[0] = sphere(p1[1:])
            S.append(p1)
        return S
    except Exception as e:
        raise Exception(f'Error en createPop : {str(e)}')
    
def sortPop(S):
    try:
        S.sort(key=lambda x: x[0])
        return S
    except Exception as e:
        raise Exception(f'Error en sortPop : {str(e)}')
    
def determineMass(S):
    try:
        #Solo se ocupan las coordenadas
        mass = ([sum(col) / len(S) for i, col in enumerate(zip(*S)) if i > 0])
        # mass = [ sum(col)/len(S) for col in  list(zip(*S))]
        return mass
    except Exception as e:
        print(str(e))

def reflection(m, reflection, peor):
    try:
        ref = [ item[0] + (reflection * (item[0] - item [1] )) for item in  zip(m , peor)]
        return ref
    except Exception as e:
        raise Exception(f"Error en reflection {str(e)}")

def main():
    try:
        # print("\n".join(str(s) for s in S))
        n = 2
        Reflection = 1
        Expansion =2
        Contraction = 0.5
        Shrink = 0.5
        #Creando el Simplex 
        S = createPop(n, n+1)
        while True:
            #Ordenamos
            S = sortPop(S)
            #print("\n".join(str(s) for s in S))
            #Calculamos el centro de masa quitamos el pero punto
            M = determineMass(S[:len(S)-1])
            #print("\n".join(str(m) for m in M))
            #Reflection: reflect the worst point over m
            R = reflection(M, Reflection, S[-1][1:])
            sphere(S[0])
            sphere(R)
            sphere(S[-1])
            if sphere(S[0]) < sphere(R) < sphere(S[-1]):
                pass
            break
    except Exception as e:
        print(f"Error en main : {str(e)}")

    
if __name__ == "__main__":
    main()
