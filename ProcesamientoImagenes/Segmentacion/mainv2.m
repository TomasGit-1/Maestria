img = imread("imagenes proyecto\ISIC_0024310.jpg");
imGray = img;
if size(img, 3) == 3
    imGray = rgb2gray(img);
end


% Crear un elemento estructurante
se = strel('disk', 5);
imgDilatada = imdilate(imGray, se);
%imgErosionada = imerode(imGray, se);


%Normalizamos de 0 a 1 
min_val = min(imgDilatada(:));
max_val = max(imgDilatada(:));
imgN_Dilatada= (imgDilatada - min_val) / (max_val - min_val);

bordesD = edge(imgN_Dilatada, 'Canny');
