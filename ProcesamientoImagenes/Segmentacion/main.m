img = imread("imagenes proyecto\ISIC_0024310.jpg");

if size(img, 3) == 3
    img = rgb2gray(img);
end
imgInver = imcomplement(img);

img = imgaussfilt(img, 2);
se = strel('disk', 5);
imgBinary = imbinarize(img);
imgDilatada = imdilate(imgBinary, se);
imgDilatada = imdilate(imgDilatada, se);
imgDilatada = imdilate(imgDilatada, se);
cc = bwconncomp(imgDilatada);
props = regionprops(cc, 'Area', 'BoundingBox', 'Centroid');

% Encontrar el índice de la región con el área más grande
[max_area, idx] = max([props.Area]);

% Obtener la información de la región más grande
area_mas_grande = props(idx).Area;
bounding_box_mas_grande = props(idx).BoundingBox;
centroid_mas_grande = props(idx).Centroid;

% Mostrar la información
disp(['Área más grande: ', num2str(area_mas_grande)]);
disp(['BoundingBox de la región más grande: ', mat2str(bounding_box_mas_grande)]);
disp(['Centroid de la región más grande: ', mat2str(centroid_mas_grande)]);


% Crear una máscara para la región más grande
mascara_region_mas_grande = false(size(imgBinary));
mascara_region_mas_grande(cc.PixelIdxList{idx}) = true;

% Superponer la máscara en la imagen original
imagen_resaltada = img; % Si img es en escala de grises
imagen_resaltada_color = cat(3, img, img, img); % Convertir a RGB si es necesario

% Resaltar la región más grande en rojo
imagen_resaltada_color(repmat(mascara_region_mas_grande, [1, 1, 3])) = 255;

% Mostrar la imagen original y la resaltada
figure;
subplot(1, 2, 1);
imshow(img);
title('Imagen Original en Escala de Grises');

subplot(1, 2, 2);
imshow(imagen_resaltada_color);
title('Región Más Grande Resaltada');
hold on;
rectangle('Position', bounding_box_mas_grande, 'EdgeColor', 'r', 'LineWidth', 2);
plot(centroid_mas_grande(1), centroid_mas_grande(2), 'b*', 'MarkerSize', 10);
hold off;