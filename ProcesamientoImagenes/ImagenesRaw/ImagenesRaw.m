fileName = 'Imagenes/paisaje.ARW';
%fileName = 'anima1.NEF';

bayerImage = rawread(fileName);
%Definimos las matriz a utilizar
bayer_rggb = uint16([800,800;800,800]);
%Procesos para obtener verdadero black
%subBayer = bayerImage(500:2000, 500:3000);
%Se ve mas claro 
subBayer = bayerImage(1:8, 1:8);

%En impares agrega una columna mas y en pares no por la matriz de 2x2
%subBayer = bayerImage
%Creamos la funciona anonima que nos permite procesar 2 x 2
funcion_resta = @(block_struct) block_struct.data - bayer_rggb;
resultado = blockproc(subBayer, [2, 2], funcion_resta);
max_valor = max(resultado(:));
bayer_normalizado = double(resultado) / double(max_valor);
%bayer_normalizado

%Ajuste de balance de blancos
balance_blancos = [2.964,1; 1, 1.832];
funcion_ajuste_W = @(block_struct) block_struct.data * balance_blancos;
bayer_balance_blancos = blockproc(bayer_normalizado, [2, 2], funcion_ajuste_W);




