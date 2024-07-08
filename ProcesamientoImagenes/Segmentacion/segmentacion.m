function mascara_region_mas_grande = segmentacion(img)
    img = imgaussfilt(img, 5);
    imgInver = imcomplement(img-0.5);
    imgBinary = imbinarize(imgInver);
    se = strel('disk', 5);  
    morphology = imopen(imgBinary, se);
    morphology = imdilate(morphology, se);
    morphology = imopen(morphology, se);
    morphology = imdilate(morphology, se);
    %morphology = imgBinary;
    cc = bwconncomp(morphology);
    props = regionprops(cc, 'Area', 'BoundingBox', 'Centroid');
    [max_area, idx] = max([props.Area]);
    mascara_region_mas_grande = false(size(morphology));
    mascara_region_mas_grande(cc.PixelIdxList{idx}) = true;

end