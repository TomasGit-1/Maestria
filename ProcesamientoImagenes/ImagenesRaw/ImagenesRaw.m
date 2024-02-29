fileName = 'paisaje.ARW';
fileName = 'anima1.NEF';

bayerImage = rawread(fileName);
%Definimos las matriz a utilizar
bayer_rggb = uint16([800,800;800,800]);

%Procesos para obtener verdadero black
%subBayer = bayerImage(500:2000, 500:3000);
subBayer = bayerImage
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




subplot(1, 3, 1); % Subplot de 1 fila y 3 columnas, primer gráfico
imshow(subBayer, []); % Mostrar bayerImage
title('Imagen original');

subplot(1, 3, 2); % Subplot de 1 fila y 2 columnas, segundo gráfico
imshow(bayer_normalizado, []); % Mostrar bayer_normalizado
title('Imagen normalizada negro');

subplot(1, 3, 3); % Subplot de 1 fila y 2 columnas, segundo gráfico
imshow(bayer_balance_blancos, []); % Mostrar bayer_normalizado
title('Imagen normalizada blanco');