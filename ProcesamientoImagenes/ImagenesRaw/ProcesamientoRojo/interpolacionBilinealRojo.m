%{
function bayer_completo_temp = interpolacion_bilineal(bayer_completo_temp, posiciones)
    % Coordenadas para la interpolación
    x1 = 1;
    x = 2;
    x2 = 3;
    % Iterar sobre las posiciones pares
    for i = 1:size(posiciones, 1)
        row = posiciones(i, 1);
        col = posiciones(i, 2);
       
        % Interpolación lineal en la fila superior
        y1 = bayer_completo_temp(row-1, col-1);
        y2 = bayer_completo_temp(row-1, col+1);
        y_first = y1 + (x - x1) * (y2 - y1) / (x2 - x1);
        
        % Interpolación lineal en la fila inferior
        y1 = bayer_completo_temp(row+1, col-1);
        y2 = bayer_completo_temp(row+1, col+1);
        y_second = y1 + (x - x1) * (y2 - y1) / (x2 - x1);
        % Interpolación bilineal
        y_second = y_first + (x - x1) * (y_second - y_first) / (x2 - x1);
        % Asignar el valor interpolado a la posición actual en la matriz
        bayer_completo_temp(row, col) = y_second;
    end
end

function bayer_completo_temp = interpolacion_bilinealCruz(bayer_completo_temp, posiciones) 
    % Coordenadas para la interpolación
    x1 = 1;
    x = 2;
    x2 = 3;
    % Iterar sobre las posiciones pares
    for i = 1:size(posiciones, 1)
        row = posiciones(i, 1);
        col = posiciones(i, 2);
        % Interpolación lineal en la fila superior
        y1 = bayer_completo_temp(row, col-1);
        y2 = bayer_completo_temp(row-1, col);
        y_first = y1 + (x - x1) * (y2 - y1) / (x2 - x1);
        % Interpolación lineal en la fila inferior
        y1 = bayer_completo_temp(row+1, col);
        y2 = bayer_completo_temp(row, col+1);
        y_second = y1 + (x - x1) * (y2 - y1) / (x2 - x1);
        % Interpolación bilineal
        y_second = y_first + (x - x1) * (y_second - y_first) / (x2 - x1);
        % Asignar el valor interpolado a la posición actual en la matriz
        bayer_completo_temp(row, col) = y_second;
    end
end

%}