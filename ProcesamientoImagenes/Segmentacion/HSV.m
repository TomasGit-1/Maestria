img = imread("imagenes proyecto\ISIC_0024310.jpg");
imagenHsv = img;
if size(img, 3) == 3
    imagenHsv = rgb2hsv(img);
end

H = imagenHsv(:, :, 1);  % Matiz
S = imagenHsv(:, :, 2);  % Saturación
V = imagenHsv(:, :, 3);  % Valor

%APlicamos filtro gauss
kernel = double([1 4 7 4 1; 4 16 25 16 4; 7 26 41 26 7;4 16 26 16 4;1 4 7 4 1]) / 273;
nneighbors = 2;
imgGauss = convolucion2D(S,nneighbors,kernel);

%MedianFilter
imgMedianF = MedianFilter(imgGauss);
imgMidPointF = MidpointFilter(imgGauss);

%imgBinary = imbinarize(V);
%se = strel('disk', 5);
%imgDilatada = imdilate(imgBinary, se);
%imgDilatada = imclose(imgBinary, se);



%bordesD = edge(imgDilatada, 'Canny');
