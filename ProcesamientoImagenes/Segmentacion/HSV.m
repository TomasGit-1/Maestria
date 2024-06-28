img = imread("imagenes proyecto\ISIC_0024310.jpg");
imagenHsv = img;
if size(img, 3) == 3
    imagenHsv = rgb2hsv(img);
end

H = imagenHsv(:, :, 1);  % Matiz
S = imagenHsv(:, :, 2);  % Saturación
V = imagenHsv(:, :, 3);  % Valor

%MedianFilter
%imgMedianF = uint8(MedianFilter(S));
imgMidPointF = uint8(MidpointFilter(S));

imgBinary = imbinarize(imgMidPointF);
se = strel('disk', 5);
imgDilatada = imdilate(imgBinary, se);
%imgDilatada = imclose(imgBinary, se);



%bordesD = edge(imgDilatada, 'Canny');
