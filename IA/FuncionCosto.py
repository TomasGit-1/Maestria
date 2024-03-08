import matplotlib.pyplot as plt
import random
def funcionCosto(w, train):
    try:
        m = len(train)
        y_temp = 0
        generate_puntos = []
        for i in range(m):
            y_predic = w * train[i][0]
            y_temp += pow((y_predic-train[i][1]),2)
            generate_puntos.append((train[i][0],y_predic))
        jw = round(((1/(2*m)) * y_temp),3)
        print("################################")
        print(f"El valor total de las distancia {jw}" , end="\n")
        print(f"Puntos generados: {''.join([str(p) for p in generate_puntos])}")
        print("################################")
        return generate_puntos, [jw,w ]
    except Exception as e:
        print(f"Error calculating {e}")

def graficar(puntos=[],valoresW=[]):
    try:
        for i in range(len(puntos)):
            x1, y1 = zip(*puntos[i][0])
            color = (random.random(), random.random(), random.random())  # Generar color aleatorio (R, G, B)
            plt.plot(x1, y1, 'o', color=color , label=f'W {puntos[i][1][1]} Distancia {puntos[i][1][0]}',  )
            plt.plot(x1, y1, color=color) 
        plt.xlabel('Coordenada x')
        plt.ylabel('Coordenada y')
        plt.title('Gráfico de múltiples conjuntos de puntos')
        plt.grid(True)
        plt.legend()
        plt.show()
    except Exception as e:
        print(f"Error graficando {e}")

if __name__ == '__main__':
    train,valoresW = [(1,1),(2,2),(3,3)],[-0.25,-0.5,0.5,0.8,1.25,1.5,2,3,0,-0.8]
    predicciones = []
    predicciones.append([train,[0,0]])
    for i in range(len(valoresW)):
        generate_puntos, distancia = funcionCosto(w=valoresW[i],train= train)
        predicciones.append([generate_puntos,distancia])
    graficar(predicciones)