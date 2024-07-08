function mascara_region_mas_grande = segmentacion(img)
    imgInver = imcomplement(img);
    imgBinary = imbinarize(imgInver);
    se = strel('disk', 5);
    imgDilatada = imdilate(imgBinary, se);

    cc = bwconncomp(imgDilatada);
    props = regionprops(cc, 'Area', 'BoundingBox', 'Centroid');
    [max_area, idx] = max([props.Area]);
    mascara_region_mas_grande = false(size(imgDilatada));
    mascara_region_mas_grande(cc.PixelIdxList{idx}) = true;
end
