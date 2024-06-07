imgGray = imread("lena_gray_256.tif");

% 1 es 3x3
% 2 es 5x5

%Prefilter
nneighbors = 2;
%Gaussiano
kernel = double([1 4 7 4 1; 4 16 25 16 4; 7 26 41 26 7;4 16 26 16 4;1 4 7 4 1]) / 273;
imgGauss = uint8(convolucion2D(imgGray,nneighbors,kernel));

%Horizontal and vertical  derivate
Hsx = [-1 0 1; -2 0 2; -1 0 1];
Hsy = [-1 -2 -1; 0 0 0; 1 2 1];
nneighbors = 1;
derivateX = convolucion2D(imgGray,nneighbors,Hsx);
derivateX = abs(derivateX);
derivateY = convolucion2D(imgGray,nneighbors,Hsy);
derivateY = abs(derivateY);