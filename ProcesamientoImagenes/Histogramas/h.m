img = imread("lena.jpg");

imgGray = rgb2gray(img);

h = histograma(imgGray);
H = HistogramA(h);

figure;
    bar(1:256, h);
    title('Histograma h');
    xlabel('Intensidad de Píxeles');
    ylabel('Frecuencia');
 
figure;
    bar(1:256, H);
    title('Histograma Acumulativos H');
    xlabel('Intensidad de Píxeles');
    ylabel('Frecuencia');
 

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

function h = histograma2(imgGray)
    histograma = histcounts(imgGray(:), 0:256);
    h = histograma';
end

