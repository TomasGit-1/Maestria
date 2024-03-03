
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
