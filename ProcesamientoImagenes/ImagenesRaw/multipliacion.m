% Definir la matriz
A = [1.6342, -0.4373, -0.1969;
    -0.1839, 1.5024, -0.3185;
    0.0408, -0.4297, 1.3889];

% Definir el vector
x = [1.2956; 1.3726; 1.1070];

% Multiplicar la matriz por el vector para obtener otro vector
resultado = A * x;

% Mostrar el resultado
disp(resultado);