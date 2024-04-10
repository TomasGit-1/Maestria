img = imread("lenaColor.png");
imgGray = rgb2gray(img);
[rows, cols] = size(imgGray);
h = histograma(imgGray);
H = HistogramA(h);

%Auto Contraste ----------
aLow = 15;
aHigh = 200;
imgAjuste = AutoContrast(imgGray , aHigh , aLow);
hAjuste = histograma(imgAjuste);
HAjuste = HistogramA(hAjuste);
%Auto Contraste ----------


%Modified Auto Contraste ----------
aMin = 0;
aMax = 255;

sLow = 0.05;
sHigh = 0.05;

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
        imagen_transformada(i, j) = uint8(max(min(new_pixel_value, 255), 0));
    end
end
imagen_transformada = uint8(imagen_transformada);
hAModified = histograma(imagen_transformada);
HAModified = HistogramA(hAModified);
%Modified Auto Contraste ----------





subplot(3,3,1); imshow(imgGray); title('Imagen Gris');
subplot(3,3,2); bar(1:256, h);  title('Histograma h');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,3); bar(1:256, H);  title('Histograma H');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');

subplot(3,3,4); imshow(imgAjuste); title('Ajuste contraste ajustado automaticamente ');
subplot(3,3,5); bar(1:256, hAjuste);  title('Histograma h');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,6); bar(1:256, HAjuste);  title('Histograma H');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');


subplot(3,3,7); imshow(imagen_transformada); title('Ajuste contraste ajustado automaticamente Modificado ');
subplot(3,3,8); bar(1:256, hAModified);  title('Histograma h');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,9); bar(1:256, HAModified);  title('Histograma H');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');



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

function h = histograma2(imgGray)
    histograma = histcounts(imgGray(:), 0:256);
    h = histograma';
end

