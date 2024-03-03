%Separar los canales
%selecciona los elementos en las filas impares y columnas impares
bayer_rojo = bayer_balance_blancos(1:2:end, 1:2:end);
[filas, columnas] = size(bayer_rojo);
%Creamos la matriz de 0
bayer_rojo_completo = zeros(filas * 2, columnas * 2, 'like', bayer_rojo);
%En las posiciones anteriores 
bayer_rojo_completo(1:2:end, 1:2:end) = bayer_rojo;

% elecciona los elementos en las filas impares y columnas pares
bayer_verde1 = bayer_balance_blancos(1:2:end, 2:2:end); 
[filas, columnas] = size(bayer_verde1);
bayer_verde1_completo = zeros(filas * 2, columnas * 2, 'like', bayer_verde1);
bayer_verde1_completo(1:2:end, 2:2:end) = bayer_verde1;

%Selecciones Filas pares y Columnas impares

bayer_verde2 = bayer_balance_blancos(2:2:end, 1:2:end); 
[filas, columnas] = size(bayer_verde2);
bayer_verde2_completo = zeros(filas * 2, columnas * 2, 'like', bayer_verde2);
bayer_verde2_completo(2:2:end, 1:2:end) = bayer_verde2;
bayer_verde1_completo(2:2:end, 1:2:end) = bayer_verde2;

%Seleccionando Filas pares y Columnnas impares pero aumentando 2
bayer_azul = bayer_balance_blancos(2:2:end, 2:2:end); 
[filas, columnas] = size(bayer_azul);
bayer_azul_completo = zeros(filas * 2, columnas * 2, 'like', bayer_azul);
bayer_azul_completo(2:2:end, 2:2:end) = bayer_azul;