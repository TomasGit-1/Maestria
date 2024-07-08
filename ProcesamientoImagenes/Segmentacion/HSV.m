path = 'imagenes proyecto/';
files = dir(fullfile(path, '*.jpg'));

for k = 1:length(files)
    filename = fullfile(path, files(k).name);
    disp(['Procesando imagen: ', filename]);
    img = imread(filename);
    
    % Convertir a escala HSV si es necesario
    imagenHsv = img;
    if size(img, 3) == 3
        imagenHsv = rgb2hsv(img);
    end
    
    % Procesamiento de la imagen según tu rutina
    H = imagenHsv(:, :, 1);  % Matiz
    S = imagenHsv(:, :, 2);  % Saturación
    V = imagenHsv(:, :, 3);  % Valor
    
    imgInver = imcomplement(V);
    imgBinary = imbinarize(imgInver);
    se = strel('disk', 5);
    imgDilatada = imdilate(imgBinary, se);
    imgDilatada = imdilate(imgDilatada, se);
    imgDilatada = imdilate(imgDilatada, se);
    imgDilatada = imdilate(imgDilatada, se);
    cc = bwconncomp(imgDilatada);
    props = regionprops(cc, 'Area', 'BoundingBox', 'Centroid');
    
    [max_area, idx] = max([props.Area]);
    mascara_region_mas_grande = false(size(imgDilatada));
    mascara_region_mas_grande(cc.PixelIdxList{idx}) = true;
    
    % Superponer la máscara en la imagen original
    img_resaltada = img;
    %{
    for i = 1:size(img, 3)
        canal = img(:,:,i);
        canal(~mascara_region_mas_grande) = 0;
        img_resaltada(:,:,i) = canal;
    end
    %}
    
    % Guardar resultados
    pathSave = 'Resultados/';
    [~, name, ext] = fileparts(filename);
    result1_name = fullfile(pathSave, ['Result1_', name, ext]);
    result2_name = fullfile(pathSave, ['Result2_', name, '.png']);  % Guardar máscara como PNG
    
    imwrite(img_resaltada, result1_name);
    imwrite(mascara_region_mas_grande, result2_name);
    
    disp(['Resultados guardados en: ', pathSave]);
end
