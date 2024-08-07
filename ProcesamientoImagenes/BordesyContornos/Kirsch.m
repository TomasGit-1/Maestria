imgGray = double(imread("lena_gray_256.tif"));

Hk0 = [-1 0 1; -2 0 2; -1 0 1];
Hk1 = [-2 -1 0; -1 0 1; 0 1 2];
Hk2 = [-1 -2 -1; 0 0 0; 1 2 1];
Hk3 = [0 -1 -2; 1 0 -1; 2 1 0];

Hk4 = [1 0 -1; 2 0 -2; 1 0 -1];
Hk5 = [2 1 0; 1 0 -1; 0 -1 -2];
Hk6 = [1 2 1; 0 0 0; -1 -2 -1];
Hk7 = [0 1 2; -1 0 1; -2 -1 0];

nneighbors = 1;
HkFull = {Hk0, Hk1, Hk2, Hk3};
Derivate = cell(1, 8);
maginitud = cell(1 ,4);

for i = 1:4
    derivate = convolucion2D(imgGray,nneighbors,HkFull{i});
    Derivate{i} = derivate;
    Derivate{i+4} = -derivate;
end

[m, n] = size(imgGray);
gradient_magnitude = zeros(m, n);
for i = 1:8
    gradient_magnitude = max(gradient_magnitude, abs(Derivate{i}));
end
gradient_magnitude = (gradient_magnitude * 255) /max(max(gradient_magnitude));

figure;
    subplot(3, 4, 1);
    imshow(uint8(imgGray));
    title('Imagen Original');
    for i = 1:8
        subplot(3, 4, i+1);
        imshow(uint8(Derivate{i}));
        title(['D ', num2str(i)]);
    end
    subplot(3, 4, 10);
    imshow(uint8(gradient_magnitude));
    title('Imagen Original');


