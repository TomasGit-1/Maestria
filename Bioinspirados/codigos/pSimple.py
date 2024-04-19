import numpy as np

class Perceptron:
    def __init__(self, num_inputs, learning_rate=0.01):
        self.weights = np.random.randn(num_inputs)
        self.bias = np.random.randn()
        self.learning_rate = learning_rate

    def activation_function(self, x):
        # Función escalón (puedes probar con otras funciones de activación)
        return 1 if x >= 0 else 0

    def predict(self, inputs):
        # Suma ponderada de las entradas y los pesos, más el término de sesgo
        z = np.dot(inputs, self.weights) + self.bias
        # Aplicación de la función de activación
        return self.activation_function(z)

    def train(self, training_inputs, labels, num_epochs):
        for epoch in range(num_epochs):
            for inputs, label in zip(training_inputs, labels):
                prediction = self.predict(inputs)
                # Actualización de los pesos y el sesgo basado en el error
                self.weights += self.learning_rate * (label - prediction) * inputs
                self.bias += self.learning_rate * (label - prediction)
            print(f"Epoch {epoch + 1}/{num_epochs} - Error: {np.mean(np.abs(labels - self.predict(training_inputs)))}")

# Ejemplo de uso
training_inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
labels = np.array([0, 0, 0, 1])

perceptron = Perceptron(num_inputs=2)
print("Pesos iniciales:", perceptron.weights)
print("Sesgo inicial:", perceptron.bias)

print("\nEntrenamiento del perceptrón:")
perceptron.train(training_inputs, labels, num_epochs=10)

print("\nPesos finales:", perceptron.weights)
print("Sesgo final:", perceptron.bias)

# Probando el perceptrón entrenado
print("\nProbando el perceptrón entrenado:")
for inputs in training_inputs:
    prediction = perceptron.predict(inputs)
    print(f"Entradas: {inputs}, Predicción: {prediction}")
