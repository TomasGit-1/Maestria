img = double(imread("lena_gray_256.tif"));
%img = double(img(1:11,1:11));

[width, height] = size(img);
[h,H] = Histograma(img);

%MedianFilter
imgMedianF = uint8(MedianFilter(img));
[hMF,HMF]  = Histograma(imgMedianF);

%MidPointFilter
imgMidPointF = uint8(MidpointFilter(img));
[hMPF,HMPF]  = Histograma(imgMidPointF);

%Alpha-Trimmed Mean Filter
imgATMFilter  = uint8(ATMFilter(img,4));
[hATMF,HATMF] = Histograma(imgATMFilter);


%Weighted Median Filter
W = [1 2 1; 2 3 2; 1 2 1];
imgWMF  = uint8(WMF(img,W));
[hWMF,HWMF] = Histograma(imgWMF);


img = uint8(img);

figure()
    subplot(3,3,1);
    imshow(imgWMF);  
    title("Weighted Median Filter");

    subplot(3,3,2);
    bar(1:256, hWMF);
    title('Histograma h');
    xlabel('Intensidad de Píxeles');
    ylabel('Frecuencia');

    subplot(3,3,3);
    bar(1:256, HWMF);
    title('Histograma Acumulativos H');
    xlabel('Intensidad de Píxeles');
    ylabel('Frecuencia');



