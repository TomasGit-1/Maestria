imgSegmentada = imread('Resultados/ISIC_0024308_Result_segmentacion.png');
objectivo = imread("Resultados/ISIC_0024308_segmentation.png");

% Convertir a escala de grises si es necesario
if size(imgSegmentada, 3) == 3
    imgSegmentada = rgb2gray(imgSegmentada);
end
if size(objectivo, 3) == 3
    objectivo = rgb2gray(objectivo);
end

% Calcular el error SAD
[SAD_total, tasa_error] = calcularErrorSAD(imgSegmentada, objectivo);

% Mostrar resultados
disp(['Suma de Diferencias Absolutas (SAD): ', num2str(SAD_total)]);
disp(['Tasa de Error Promedio: ', num2str(tasa_error)]);