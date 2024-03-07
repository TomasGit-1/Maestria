
%imwrite(imagen3D, 'nueva_imagen.png');

filas = 5;
columnas = 3;

subplot(filas, columnas, 1); % Subplot de 1 fila y 3 columnas, primer gráfico
imshow(subBayer, []); % Mostrar bayerImage
title('Imagen original');

subplot(filas, columnas, 2);
imshow(bayer_normalizado, []);
title('Imagen normalizada negro');

subplot(filas, columnas, 3);
imshow(bayer_balance_blancos, []); 
title('Imagen normalizada blanco');

subplot(filas, columnas, 4);
imshow(canalR, []);
title('Mosaico R');

subplot(filas, columnas, 5); 
imshow(canalV, []); 
title('Mosaico GG');

subplot(filas, columnas, 6); 
imshow(canalA, []);
title('Mosaico A');

subplot(filas, columnas, 7);
imshow(bayer_rojo_completo, []);
title('Mosaico Completo R');

subplot(filas, columnas, 8); 
imshow(bayer_verde1_completo, []); 
title('Mosaico Completo GG');

subplot(filas, columnas, 9); 
imshow(bayer_azul_completo, []);
title('Mosaico Completo A');


subplot(filas, columnas, 10);
imshow(ColorR, []);
title('Color R');

subplot(filas, columnas, 11); 
imshow(ColorV, []); 
title('Color GG');

subplot(filas, columnas, 12); 
imshow(ColorA, []);
title('Color A');


subplot(filas, columnas, 13);
imshow(Tempimagen3D, []);
title('Imagen Temp');


subplot(filas, columnas, 14);
imshow(imagen3D, []);
title('Imagen Final');

%{
subplot(filas, columnas, 10);
imshow(imagen_rojo_corregido, []);
title('Mosaico R 3d');

subplot(filas, columnas, 11); 
imshow(imagen_verde_corregido, []); 
title('Mosaico GG 3d');

subplot(filas, columnas, 12); 
imshow(imagen_azul_corregido, []);
title('Mosaico A 3d');


subplot(filas, columnas, 14); 
imshow(imagen3D_normalizada, []);
title('Imagen Normalizacion');
%}

