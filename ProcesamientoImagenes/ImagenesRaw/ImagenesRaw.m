fileName = 'paisaje.ARW';
%fileName = 'anima1.NEF';

bayerImage = rawread(fileName);
%Definimos las matriz a utilizar
bayer_rggb = uint16([800,800;800,800]);

%Procesos para obtener verdadero black
%subBayer = bayerImage(500:2000, 500:3000);
%Se ve mas claro 
subBayer = bayerImage(1:10, 1:10);

%subBayer = bayerImage
%Creamos la funciona anonima que nos permite procesar 2 x 2
funcion_resta = @(block_struct) block_struct.data - bayer_rggb;
resultado = blockproc(subBayer, [2, 2], funcion_resta);
max_valor = max(resultado(:));
bayer_normalizado = double(resultado) / double(max_valor);
%bayer_normalizado

%Ajuste de balance de blancos
balance_blancos = [2.964,1; 1, 1.832]
funcion_ajuste_W = @(block_struct) block_struct.data * balance_blancos;
bayer_balance_blancos = blockproc(bayer_normalizado, [2, 2], funcion_ajuste_W);

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



%Interpolacion
%pixeles_a_interpolar = (bayer_rojo_completo == 0);
%indices_interpolar = find(pixeles_a_interpolar);
%matriz_interpolada(indices_interpolar) = imresize(bayer_rojo_completo(indices_interpolar), size(bayer_rojo_completo(indices_interpolar)), 'bilinear');

%valores_interpolar = bayer_rojo_completo(pixeles_a_interpolar);  % Obtener los valores a interpolar
%valores_interpolar_redimensionados = imresize(valores_interpolar, size(valores_interpolar), 'bilinear');  % Interpolar los valores
%matriz_interpolada(indices_interpolar) = valores_interpolar_redimensionados;  % Asignar los valores interpolados a matriz_interpolada

%matriz_interpoladatemp = imresize(bayer_rojo_completo, size(bayer_rojo_completo), 'bilinear');
%matriz_interpolada = matriz_interpoladatemp .* double(pixeles_a_interpolar) + bayer_rojo_completo;
%imshow(matriz_interpolada);


% Generar una máscara de los píxeles a interpolar
pixeles_a_interpolar = (bayer_rojo_completo == 0);
% Obtener los índices de los píxeles a interpolar
indices_interpolar = find(pixeles_a_interpolar);
% Interpolar solo en los píxeles a interpolar
valores_interpolar = bayer_rojo_completo(indices_interpolar);
valores_interpolar_redimensionados = imresize(valores_interpolar, size(valores_interpolar), 'bilinear');
% Crear una matriz temporal para almacenar los valores interpolados
matriz_interpolada_temp = bayer_rojo_completo;
matriz_interpolada_temp(indices_interpolar) = valores_interpolar_redimensionados;
% Combinar la matriz temporal con la matriz original para obtener la matriz interpolada final
matriz_interpolada = matriz_interpolada_temp;



subplot(2, 3, 1); % Subplot de 1 fila y 3 columnas, primer gráfico
imshow(subBayer, []); % Mostrar bayerImage
title('Imagen original');

subplot(2, 3, 2);
imshow(bayer_normalizado, []);
title('Imagen normalizada negro');

subplot(2, 3, 3);
imshow(bayer_balance_blancos, []); 
title('Imagen normalizada blanco');

subplot(2, 3, 4);
imshow(bayer_rojo_completo, []);
title('Mosaico R');

subplot(2, 3, 5); 
imshow(bayer_verde1_completo, []); 
title('Mosaico GG');

subplot(2, 3, 6); 
imshow(bayer_azul_completo, []);
title('Mosaico A');

