function [h,H] = Histograma(imgGray)
    h = zeros(256, 1);
    for row = 1:size(imgGray, 1)
        for col = 1:size(imgGray, 2)
            intensidad_pixel = imgGray(row, col);
            h(intensidad_pixel + 1) = h(intensidad_pixel + 1) + 1;
        end
    end

    H = zeros(256, 1);
    H(1) = h(1);
    for j=2:size(h)
        H(j) = H(j-1) + h(j);
    end

end

