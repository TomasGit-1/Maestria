import numpy as np
from ANN import ANN

# Ejemplo de entrenamiento y uso de la red neuronal
if __name__ == "__main__":
    # Datos de entrada y salida de ejemplo
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])
    
    y = np.array([[0],
                  [1],
                  [1],
                  [0]])
    
    # Crear una instancia de la red neuronal con 2 neuronas en la capa oculta
    nn = ANN(input_size=2, hidden_size=4, output_size=1)
    
    # Entrenar la red neuronal
    nn.train(X, y, epochs=10000, learning_rate=0.1)
    
    # Hacer predicciones
    predictions = nn.predict(X)
    
    # Mostrar resultados
    print("Predicciones:")
    for i in range(len(X)):
        print(f"Datos de entrada: {X[i]}, Predicción: {predictions[i]}")
