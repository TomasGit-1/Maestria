path = 'imagenes proyecto/';
files = dir(fullfile(path, '*.jpg'));

for k = 1:length(files)
    filename = fullfile(path, files(k).name);
    disp(['Procesando imagen: ', filename]);
    img = imread(filename);
    imagenHsv = img;
    if size(img, 3) == 3
        imagenHsv = rgb2hsv(img);
    end
    H = imagenHsv(:, :, 1);  % Matiz
    S = imagenHsv(:, :, 2);  % Saturación
    V = imagenHsv(:, :, 3);  % Valor
    
    mascara_region_mas_grande = segmentacion(V);
     
    % Guardar resultados
    pathSave = 'Resultados/';
    [~, name, ext] = fileparts(filename);
    pathResult = fullfile(pathSave, ['Result2_', name, '.png']);
    imwrite(mascara_region_mas_grande, pathResult);
    %disp(['Resultados guardados en: ', pathSave]);
end
