"""
    Funcion de la esfera
    Donde x es un vector en un espacion n-dimensional
    xcentro es el valor del centro de la esfera
    El objetivo de la optimización es encontrar el valor de xx que minimiza esta función.
    f(x) = sumatoria de i hasta n (xi - xcentro)**2
"""

import numpy as np

def generateVectorRandom(n):
    S = np.random.rand(n) * 100
    S = np.round(S).astype(int)
    return S

def esferaF():
    try:
        x = generateVectorRandom(100)
        xcentro = np.random.randint(0, 100)
        return np.sum((x - xcentro) ** 2)
    except Exception as e:
        print(str(e))

def determineMasa(n, S):
    try:
        """ 
            Center of mass:
            Determine the center of mass of the n best points
        """
        return (sum( S[x] for x in range(len(S)-1)))/n
    except Exception as e:
        print(str(e))

def reflection(m, Sn , reflection):
    try:
        """Reflection: reflect the worst point over"""
        return m + reflection * (m - Sn)
    except Exception as e:
        print(str(e))

def main(n:int, S,reflection,expansion,contraction,shrink):
    f = esferaF()
    try:
        while True:
            S.sort()
            m = determineMasa(n = n , S = S)
            r = reflection(m, S[n], reflection=reflection)
            break
    except Exception as e:
        print(str(e))

    
if __name__ == '__main__':
    reflection = 0.5
    expansion = 0.2
    contraction = 1
    shrink = 0.5
    n = 3
    S = generateVectorRandom(n+1)
    main(
            n=n, S= S, 
            reflection = reflection, 
            expansion= expansion, 
            contraction = contraction , 
            shrink = shrink
        )



def mainV2():
    li, ls = -10, 10
    dim = 2
    S = []
    for _ in range(dim):
        p1 = [0]
        for _ in range(dim):
            p1.append(li + random() * (ls - li))
        p1[0] = sphere(p1[1:])
        S.append(p1)
    print("\n".join(str(s) for s in S))
