imgGray = double(imread("lena_gray_256.tif"));
%imgGray = rgb2gray(imgGray);

%Prewitt
Hsy = [-1 0 1; -1 0 1; -1 0 1];
Hsx = [-1 -1 -1; 0 0 0; 1 1 1];
% 1 es 3x3
% 2 es 5x5
nneighbors = 1;
derivateX = convolucion2D(imgGray,nneighbors,Hsx);
derivateX = abs(derivateX);

derivateY = convolucion2D(imgGray,nneighbors,Hsy);
derivateY = abs(derivateY);

gradient_magnitude = sqrt( derivateX .^ 2 + derivateY .^ 2);
gradient_magnitude = (gradient_magnitude * 255) /max(max(gradient_magnitude));

subplot(1, 4, 1), imshow(uint8(imgGray)), title('Original Image');
subplot(1, 4, 2), imshow(uint8(derivateX), []), title('Prewitt X');
subplot(1, 4, 3), imshow(uint8(derivateY), []), title('Prewitt Y');
subplot(1, 4, 4), imshow(uint8(gradient_magnitude), []), title('E(u,v)');

