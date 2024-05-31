function HG = gaussianKernel(size, sigma)
    size = floor(size / 2);
    [x, y] = meshgrid(-size:1:size);
    normal = 1 / (2.0 * pi * sigma ^ 2);
    HG = exp( -( (x.^2 + y.^2) / (2.0 * sigma ^ 2))) * normal;
end
