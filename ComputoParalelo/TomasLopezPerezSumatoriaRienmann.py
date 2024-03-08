def f(x:float):
    return x**3+x**2-1
#Utilize la funcion de la clas

def main():
    try:
        #Calculamos las  sumatoria de riemann
        #Se definen las entradas
        limInferior ,limSuperior, nRectangulos = -1, 3, 1000000
        #Se calcula delatax
        deltaX = ( limSuperior - limInferior ) / nRectangulos
        sumaRiemann = 0
        #Modifique el incio en 1 ya que con el 0 hace una vuelta mas
        for i in range(1,nRectangulos):
            sumaRiemann = sumaRiemann + f( limInferior + i * deltaX ) * deltaX
        print(f"Valor del area sobre la curva es {str(sumaRiemann)} del intervalo [ {limInferior} :  {limSuperior} ]" )
    except Exception as e:
        print(f"Error al calcular las sumatoria de riemann: {str(e)}")
        
if __name__ == '__main__':
    main()
