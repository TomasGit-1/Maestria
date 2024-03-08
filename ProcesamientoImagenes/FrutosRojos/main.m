img = imread("frutos_rojos.png");
imgGris = (img(:,:,1) + img(:,:,2) + img(:,:,3))/3;

%Aplicando Ponderacion

imgGrisPon =(0.299 * img(:,:,1) + 0.687 * img(:,:,2) + 0.114 * img(:,:,3)); 


imgCanales = cat(2,img(:,:,1),img(:,:,2),img(:,:,3));

segR = img(:,:,1) > 200;
segV = img(:,:,2) < 140;
segB = img(:,:,3);

separacion = segR & segV & segB;
imgFinal = img .* uint8(separacion);


filas = 2;
columnas = 2;
subplot(filas, columnas, 1);
imshow(img,[]);
title("Imagen Original");

subplot(filas, columnas, 2);
imshow(imgFinal);
title("Imagen procesada");

subplot(filas, columnas,[3,4]);
imshow(imgCanales);
title("Imagene canales");

   