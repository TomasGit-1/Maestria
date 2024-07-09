path = 'imagenes proyecto/';
files = dir(fullfile(path, '*.jpg'));
isHsV = false;
for k = 1:length(files)
    filename = fullfile(path, files(k).name);
    disp(['Procesando imagen: ', filename]);
    img = imread(filename);
    if isHsV
        disp(['HSV']);
        imagenHsv = img;
        if size(img, 3) == 3
            imagenHsv = rgb2hsv(img);
        end
        H = imagenHsv(:, :, 1);  % Matiz
        S = imagenHsv(:, :, 2);  % Saturación
        V = imagenHsv(:, :, 3);  % Valor
        procesar = V;
    else
        disp(['GRAY']);
        imgGRAY = img;
        if size(img, 3) == 3
            imgGRAY = rgb2gray(img);
        end
        procesar = imgGRAY;
    end
    %valueMask = procesar >= 100;
    mascara_region_mas_grande = segmentacion(procesar);
     
    % Guardar resultados
    pathSave = 'Resultados/';
    [~, name, ext] = fileparts(filename);
    pathResult = fullfile(pathSave, [name,'_Result','_segmentacion', '.png']);
    imwrite(mascara_region_mas_grande, pathResult);

    objectivo = imread(sprintf('Resultados/%s_segmentation.png', name));
    imgSegmentada = imread(pathResult);

    if size(imgSegmentada, 3) == 3
        imgSegmentada = rgb2gray(imgSegmentada);
    end
    if size(objectivo, 3) == 3
        objectivo = rgb2gray(objectivo);
    end
    [SAD_total, tasa_error] = calcularErrorSAD(imgSegmentada, objectivo);
    disp(["Imagen : ",name]);
    disp(['Suma de Diferencias Absolutas (SAD): ', num2str(SAD_total)]);
    disp(['Tasa de Error Promedio: ', num2str(tasa_error)]);
    disp(["#############################"]);
end
