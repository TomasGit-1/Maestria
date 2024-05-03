img = double(imread("lena_gray_256.tif"));
%img = double(img(110:150,110:150));
%Aplicamos el procesos de convolucion
% 1 es 3x3
% 2 es 5x5
nneighbors = 2;
%Kernel

%Gaussiano

kernel = double([1 4 7 4 1; 4 16 25 16 4; 7 26 41 26 7;4 16 26 16 4;1 4 7 4 1]) / 273;
imgGauss = uint8(convolucion2D(img,nneighbors,kernel));

%imgGauss2 = uint8(conv2(double(img), kernel, 'same'));

%laplace
kernel = double([0 0 -1 0 0; 0 -1 -2 -1 0; -1 -2 16 -2 -1; 0 -1 -2 -1 0;0 0 -1 0 0 ]);
imgLaplace = uint8(convolucion2D(img,nneighbors,kernel));
%imgLaplace2 = uint8(conv2(img, kernel, 'same'));


%Low pass Filter 
kernel = LowPassFilter();
nneighbors = 15;
imgLowPassFilter = uint8(convolucion2D(img,nneighbors,kernel));
%imgLowPassFilter2 = uint8(conv2(img, kernel, 'same'));

%Sharpening filter
kernel = sharpeningFilter();
nneighbors = 6;
imgsharpeningFilter = uint8(convolucion2D(img,nneighbors,kernel));
%imgsharpeningFilter2 = uint8(conv2(img, kernel, 'same'));


img = uint8(img);

figure()
    subplot(1,3,1);
    imshow(img);  
    title("Original");

    subplot(1,3,2);
    imshow(imgGauss);  
    title("Gauss");

    subplot(1,3,3);
    imshow(imgLaplace);  
    title("Laplace")


figure()
    subplot(1,3,1);
    imshow(img);  
    title("Original");
    
    subplot(1,3,2);
    imshow(imgLowPassFilter);  
    title("LowPassFilter");

    subplot(1,3,3);
    imshow(imgsharpeningFilter);  
    title("sharpeningFilter")
