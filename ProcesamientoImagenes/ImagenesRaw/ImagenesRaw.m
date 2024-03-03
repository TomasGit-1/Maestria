fileName = 'Imagenes/paisaje.ARW';
bayerImage = rawread(fileName);
bayerInfo = rawinfo(fileName)
cameraToRGB = bayerInfo.ColorInfo.CameraTosRGB
%Definimos las matriz a utilizar
bayer_rggb = uint16([800,800;800,800]);
%Procesos para obtener verdadero black
%subBayer = bayerImage(500:1800, 500:1800);
%subBayer = bayerImage(1:10, 1:10);
subBayer = bayerImage
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




