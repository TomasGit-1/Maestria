imgGray = imread("lena_gray_256.tif");

%Noise reduction
size = 5;
sigma = 1;
HG = gaussianKernel(size, sigma);
nneighbors = 2;
imgNR = convolucion2D(imgGray,nneighbors,HG);


%Gradient calculation
Hsx = [-1 0 1; -2 0 2; -1 0 1];
Hsy = [-1 -2 -1; 0 0 0; 1 2 1];

nneighbors = 1;
derivateX = convolucion2D(imgNR,nneighbors,Hsx);
derivateX = abs(derivateX);
derivateY = convolucion2D(imgNR,nneighbors,Hsy);
derivateY = abs(derivateY);

gradient_magnitude = sqrt( derivateX .^ 2 + derivateY .^ 2);
gradient_magnitude = uint8((gradient_magnitude * 255) /max(max(gradient_magnitude)));

theta = [-pi/4, pi/2; -pi, pi/3];
E2 = NMSuppression(gradient_magnitude,theta);