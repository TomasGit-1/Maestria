img = imread("imagenes proyecto\ISIC_0024310.jpg");
imagenHsv = img;
if size(img, 3) == 3
    imGray = rgb2gray(img);
end



imgBinary = imbinarize(imGray);
se = strel('disk', 5);
imgDilatada = imdilate(imgBinary, se);
%imgDilatada = imclose(imgBinary, se);



%bordesD = edge(imgDilatada, 'Canny');
