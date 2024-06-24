import numpy as np

class RedNeuronalModel():
    def __init__(self, input_size, hidden_size, output_size, connectivity, learning_rate=0.1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.connectivity = connectivity
        self.learning_rate = learning_rate
        self.W1, self.W2 = self.initialize_weights()
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def initialize_weights(self):
        np.random.seed(42)
        W1 = np.random.randn(self.input_size, self.hidden_size)
        mask = np.random.rand(self.input_size, self.hidden_size) < self.connectivity
        W1 *= mask   
        W2 = np.random.randn(self.hidden_size, self.output_size)
        return W1, W2
    
    def forward_propagation(self, X):
        self.Z1 = np.dot(X, self.W1)
        self.A1 = self.sigmoid(self.Z1)
        
        self.Z2 = np.dot(self.A1, self.W2)
        self.A2 = self.sigmoid(self.Z2)
        
        return self.A2
    
    def back_propagation(self, X, Y):
        output_error = Y - self.A2
        output_delta = output_error * self.sigmoid_derivative(self.A2)
        
        hidden_error = np.dot(output_delta, self.W2.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(self.A1)
        
        self.W2 += np.dot(self.A1.T, output_delta) * self.learning_rate
        self.W1 += np.dot(X.T, hidden_delta) * self.learning_rate
    
    def train(self, X, Y, epochs):
        for epoch in range(epochs):
            self.forward_propagation(X)
            self.back_propagation(X, Y)
            if epoch % 1000 == 0:
                loss = np.mean((Y - self.A2) ** 2)
                print(f"Epoch {epoch}, Loss: {loss}")
    
    def predict(self, X):
        return self.forward_propagation(X)