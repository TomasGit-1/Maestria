img = imread("lenaColor.png");
imgGray = rgb2gray(img);
[rows, cols] = size(imgGray);
h = histograma(imgGray);
H = HistogramA(h);

%Auto Contraste ----------
aLow = 15;
aHigh = 200;
imgAjuste = AutoContrastLUT(imgGray , aHigh , aLow);
hAjuste = histograma(imgAjuste);
HAjuste = HistogramA(hAjuste);
%Auto Contraste ----------


%Modified Auto Contraste ----------
aMin = 0;
aMax = 255;
sLow = 0.05;
sHigh = 0.05;
imagen_transformada = ModifiedACLUT(aMin,aMax,sLow,sHigh,H,imgGray);
hAModified = histograma(imagen_transformada);
HAModified = HistogramA(hAModified);

%imagen_transformada2 = AutoContrastLUT(imgGray , aHigh , aLow);

%imagen_transformada2 = ModifiedACLUT(aMin,aMax,sLow,sHigh,H,imgGray);
%hAModified2 = histograma(imagen_transformada2);
%HAModified2 = HistogramA(hAModified);
%Modified Auto Contraste ----------




figure(1)
subplot(3,3,1); imshow(imgGray); title('Imagen Gris');
subplot(3,3,2); bar(1:256, h);  title('Histograma h');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,3); bar(1:256, H);  title('Histograma H');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');

subplot(3,3,4); imshow(imgAjuste); title('automático de contraste ');
subplot(3,3,5); bar(1:256, hAjuste);  title('Histograma h');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,6); bar(1:256, HAjuste);  title('Histograma H');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');

subplot(3,3,7); imshow(imagen_transformada); title('auto-contraste modificado');
subplot(3,3,8); bar(1:256, hAModified);  title('Histograma h');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,9); bar(1:256, HAModified);  title('Histograma H');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');

%subplot(4,3,10); imshow(imagen_transformada2); title('auto-contraste modificado LOOK Table');
%subplot(4,3,11); bar(1:256, hAModified2);  title('Histograma h');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
%subplot(4,3,12); bar(1:256, HAModified2);  title('Histograma H');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');

function h = histograma(imgGray)
    h = zeros(256, 1);
    for row = 1:size(imgGray, 1)
        for col = 1:size(imgGray, 2)
            intensidad_pixel = imgGray(row, col);
            h(intensidad_pixel + 1) = h(intensidad_pixel + 1) + 1;
        end
    end
end

function H = HistogramA(h)
    H = zeros(256, 1);
    H(1) = h(1);
    for j=2:size(h)
        H(j) = H(j-1) + h(j);
    end
end

function imgAdjusted = AutoContrast(imgGray, aHigh , aLow)
    imgAdjusted = (double(imgGray)- aLow) * 255 / aHigh - aLow;
    imgAdjusted = uint8(imgAdjusted);
end 

function newImage = LUTTable(image)
    for i = 1:256
        LUT(i) = i * 10
    end

    for r = 1:nRows
        for c = 1:nCols
            newImage(r,c) = LUT(image(r,c));
        end
    end
end

function imagen_transformada =ModifiedAutoContraste(aMin,aMax,sLow,sHigh,H,imgGray)
    [rows, cols] = size(imgGray);
    num_pixels = rows * cols;
    MNSlow = num_pixels * sLow;
    MNShigh = num_pixels * (1 - sHigh);
    aclow = find(H >= MNSlow,1, 'first');
    achigh = find(H <= MNShigh,1,'last');
    imagen_transformada = zeros(rows, cols);
     for i = 1:rows
        for j = 1:cols
            a = double(imgGray(i, j));
            new_pixel_value = (a - aclow) * 255 / (achigh - aclow);
            imagen_transformada(i, j) = uint8(max(min(new_pixel_value, aMax), aMin));
        end
    end
    imagen_transformada = uint8(imagen_transformada);
end


function imagen_transformada =ModifiedACLUT(aMin,aMax,sLow,sHigh,H,imgGray)
    [rows, cols] = size(imgGray);    
    num_pixels = rows * cols;
    MNSlow = num_pixels * sLow;
    MNShigh = num_pixels * (1 - sHigh);
    aclow = find(H >= MNSlow,1, 'first');
    achigh = find(H <= MNShigh,1,'last');
    imagen_transformada = zeros(rows, cols);
    LUT = zeros(rows, 1);

    for i = 1:aMax
        new_pixel_value = (i - aclow) * 255 / (achigh - aclow);
        LUT(i) = uint8(max(min(new_pixel_value, aMax), aMin));
    end
    
     for i = 1:rows
        for j = 1:cols
            imagen_transformada(i, j) = LUT(imgGray(i, j));
        end
     end

    imagen_transformada = uint8(imagen_transformada);
end

function imagen_transformada =AutoContrastLUT(imgGray, aHigh , aLow)
    [rows, cols] = size(imgGray);    
    imagen_transformada = zeros(rows, cols);
    LUT = zeros(rows, 1);
    for i = 1:256
        new_pixel_value = (i- aLow) * 255 / aHigh - aLow;
        LUT(i) = uint8(new_pixel_value);
    end
     for i = 1:rows
        for j = 1:cols
            imagen_transformada(i, j) = LUT(imgGray(i, j));
        end
     end

    imagen_transformada = uint8(imagen_transformada);
end

