img = imread("imagenes proyecto\ISIC_0024306.jpg");

if size(img, 3) == 3
    img = rgb2gray(img);
end
imgInver = imcomplement(img);
img = imgaussfilt(img, 2);
se = strel('disk', 3);
imgBinary = imbinarize(img);
imgDilatada = imdilate(imgBinary, se);
imgDilatada = imdilate(imgDilatada, se);
imgDilatada = imdilate(imgDilatada, se);
imgEroded = imerode(imgDilatada, se);

cc = bwconncomp(imgEroded);
props = regionprops(cc, 'Area', 'BoundingBox', 'Centroid');

% Encontrar el índice de la región con el área más grande
[max_area, idx] = max([props.Area]);

% Obtener la información de la región más grande
area_mas_grande = props(idx).Area;
%bounding_box_mas_grande = props(idx).BoundingBox;
%centroid_mas_grande = props(idx).Centroid;

% Mostrar la información
%disp(['Área más grande: ', num2str(area_mas_grande)]);
%disp(['BoundingBox de la región más grande: ', mat2str(bounding_box_mas_grande)]);
%disp(['Centroid de la región más grande: ', mat2str(centroid_mas_grande)]);

% Crear una máscara para la región más grande
mascara_region_mas_grande = false(size(imgBinary));
mascara_region_mas_grande(cc.PixelIdxList{idx}) = true;
imgInver = imcomplement(mascara_region_mas_grande);


figure;
subplot(1, 2, 1);
imshow(img);
title('Imagen Original en Escala de Grises');

subplot(1, 2, 2);
imshow(imgInver);
title('Región Más Grande Resaltada');
