name = "ISIC_0024307.jpg";

path = "imagenes proyecto\";
filename = path + name;
img = imread(filename);

imagenHsv = img;
if size(img, 3) == 3
    imagenHsv = rgb2hsv(img);
end

H = imagenHsv(:, :, 1);  % Matiz
S = imagenHsv(:, :, 2);  % Saturación
V = imagenHsv(:, :, 3);  % Valor
imgInver = imcomplement(V);
imgBinary = imbinarize(imgInver);
se = strel('disk', 5);
imgDilatada = imdilate(imgBinary, se);
imgDilatada = imdilate(imgDilatada, se);
imgDilatada = imdilate(imgDilatada, se);
imgDilatada = imdilate(imgDilatada, se);
cc = bwconncomp(imgDilatada);
props = regionprops(cc, 'Area', 'BoundingBox', 'Centroid');

[max_area, idx] = max([props.Area]);
mascara_region_mas_grande = false(size(imgDilatada));
mascara_region_mas_grande(cc.PixelIdxList{idx}) = true;

% Encontrar el índice de la región con el área más grande
[max_area, idx] = max([props.Area]);

% Crear una máscara para la región más grande
mascara_region_mas_grande = false(size(imgDilatada));
mascara_region_mas_grande(cc.PixelIdxList{idx}) = true;

% Superponer la máscara en la imagen original
img_resaltada = img;
for i = 1:size(img, 3)
    canal = img(:,:,i);
    canal(~mascara_region_mas_grande) = 0;
    img_resaltada(:,:,i) = canal;
end

pathSave = "Resultados/";
imwrite(img_resaltada, pathSave+"Result1_"+name);
imwrite(mascara_region_mas_grande, pathSave+"Result2_"+name);

