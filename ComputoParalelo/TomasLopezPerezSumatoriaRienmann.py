def f(x:float):
    return x**3 +2*x -1

def main():
    try:
        #Calculamos las  sumatoria de riemann
        #Se definen las entradas
        limInferior ,limSuperior, nRectangulos = -1, 3, 100
        #Se calcula delatax
        deltaX = ( limSuperior - limInferior ) / nRectangulos
        sumaRiemann = 0
        for i in range(nRectangulos):
            sumaRiemann = sumaRiemann + f( limInferior + i * deltaX ) * deltaX
        print(f"Valor del area sobre la curva es {str(sumaRiemann)} del intervalo [ {limInferior} :  {limSuperior} ]" )
    except Exception as e:
        print(f"Error al calcular las sumatoria de riemann: {str(e)}")


if __name__ == '__main__':
    main()
