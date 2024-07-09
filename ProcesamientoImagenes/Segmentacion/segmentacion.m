function mascara_region_mas_grande = segmentacion(img)
    img = imgaussfilt(img, 5);
    imgInver = imcomplement(img-0.5);
    imgBinary = imbinarize(imgInver);
    se = strel('disk', 5);  
    morphology = imdilate(imgBinary, se);
    morphology = imopen(morphology, se);
    morphology = imdilate(morphology, se);
    morphology = imdilate(morphology, se);
    morphology = imdilate(morphology, se);
    cc = bwconncomp(morphology);
    props = regionprops(cc, 'Area', 'BoundingBox', 'Centroid');
    [max_area, idx] = max([props.Area]);
    mascara_region_mas_grande = false(size(morphology));
    mascara_region_mas_grande(cc.PixelIdxList{idx}) = true;
    mascara_region_mas_grande = imfill(mascara_region_mas_grande, 'holes');
    
    se = strel('diamond', 10); 
    mascara_region_mas_grande = imopen(mascara_region_mas_grande, se);
    mascara_region_mas_grande = imdilate(mascara_region_mas_grande, se);
    mascara_region_mas_grande = imfill(mascara_region_mas_grande, 'holes');
end
