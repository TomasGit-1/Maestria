function [SAD_total, tasa_error] = calcularErrorSAD(imgSegmentada, objectivo)
    assert(isequal(size(imgSegmentada), size(objectivo)), 'Las dimensiones de las imágenes deben ser iguales.');
  
    % Calcular la suma de diferencias absolutas (SAD)
    diferencias_absolutas = abs(double(imgSegmentada) - double(objectivo));
    SAD_total = sum(diferencias_absolutas(:));

    % Calcular el número total de píxeles
    num_pixeles = numel(imgSegmentada);

    % Calcular la tasa de error promedio
    tasa_error = SAD_total / num_pixeles;
end
