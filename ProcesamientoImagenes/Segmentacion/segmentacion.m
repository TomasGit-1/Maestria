img = imread("imagenes proyecto\ISIC_0024307.jpg");
if size(img, 3) == 3
    img = rgb2gray(img);
end
img = imgaussfilt(img, 2);
imgInver = imcomplement(img);

se = strel('disk', 3);
imgBinary = imbinarize(imgInver);
imgDilatada = imdilate(imgBinary, se);
imgDilatada = imdilate(imgDilatada, se);

cc = bwconncomp(imgDilatada);
props = regionprops(cc, 'Area', 'BoundingBox', 'Centroid');
