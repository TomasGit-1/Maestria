img = imread("lena_gray_256.tif");

%Aplicamos el procesos de convolucion
% 1 es 3x3
% 2 es 5x5
nneighbors = 2;
%Kernel

%Gaussiano
kernel = double([1 4 7 4 1; 4 16 25 16 4; 7 26 41 26 7;4 16 26 16 4;1 4 7 4 1]) / 273;

imgConvolucionada = uint8(convolucion2D(img,nneighbors,kernel));