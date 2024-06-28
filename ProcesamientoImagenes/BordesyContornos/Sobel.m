imgGray = double(imread("lena_gray_256.tif"));
imgGray = rgb2gray(imgGray);
%Sobel
Hsx = [-1 0 1; -2 0 2; -1 0 1];
Hsy = [-1 -2 -1; 0 0 0; 1 2 1];
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
subplot(1, 4, 2), imshow(derivateX, []), title('Sobel X');
subplot(1, 4, 3), imshow(derivateY, []), title('Sobel Y');
subplot(1, 4, 4), imshow(uint8(gradient_magnitude), []), title('E(u,v)');



%imgGray = rgb2gray(img);
%gradient_direction = atan2(derivateY, derivateX);
%Dx_normalized = (derivateX - min(derivateX(:))) / (max(derivateX(:)) - min(derivateX(:))) * 255;
%Dy_normalized = (derivateY - min(derivateY(:))) / (max(derivateY(:)) - min(derivateY(:))) * 255;
%combined_image =  Dx_normalized + Dy_normalized;

