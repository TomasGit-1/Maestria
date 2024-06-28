img = imread("imagenes proyecto\ISIC_0024306.jpg");
canalRojo = img(:, :, 1);
grayImage = rgb2gray(img);


if size(img, 3) == 3
    img = rgb2gray(img);
end

% Crear un elemento estructurante
se = strel('disk', 5);

imgDilatada = imdilate(img, se);
imgErosionada = imerode(img, se);

bordes = edge(img, 'Canny');

%Sobel
Hsx = [-1 0 1; -2 0 2; -1 0 1];
Hsy = [-1 -2 -1; 0 0 0; 1 2 1];
% 1 es 3x3
% 2 es 5x5
nneighbors = 1;
derivateX = convolucion2D(imgDilatada,nneighbors,Hsx);
derivateX = abs(derivateX);
derivateY = convolucion2D(imgDilatada,nneighbors,Hsy);
derivateY = abs(derivateY);

gradient_magnitude = sqrt( derivateX .^ 2 + derivateY .^ 2);
gradient_magnitude = (gradient_magnitude * 255) /max(max(gradient_magnitude));
