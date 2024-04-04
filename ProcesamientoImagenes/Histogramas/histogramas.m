img = imread("lenaColor.png");

imgGray = rgb2gray(img);

h = histograma(imgGray);
H = HistogramA(h);


aLow = 10;
aHigh = 220;
imgAjuste = AutoContrast(imgGray , aHigh , aLow);
hAjuste = histograma(imgAjuste);
HAjuste = HistogramA(hAjuste);

subplot(2,3,1); imshow(imgGray); title('Imagen Gris');
subplot(2,3,2); bar(1:256, h);  title('Histograma h');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(2,3,3); bar(1:256, H);  title('Histograma H');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');

subplot(2,3,4); imshow(imgAjuste); title('Ajuste contraste ajustado automaticamente ');
subplot(2,3,5); bar(1:256, hAjuste);  title('Histograma h');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(2,3,6); bar(1:256, HAjuste);  title('Histograma H');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');


 

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

function h = histograma2(imgGray)
    histograma = histcounts(imgGray(:), 0:256);
    h = histograma';
end

