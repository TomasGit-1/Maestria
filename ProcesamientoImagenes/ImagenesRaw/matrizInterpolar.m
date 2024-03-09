

vec = [0.1870,0.18415,0.1800,0.18415;
       0.1871,    0,  0.1801,0.18415;
       0.1872,0.18415,0.1802,0.18415;
       0.1873,    0,  0.1803,0.18415;
       0.1874,0.18415,0.1804,0.18415]
%{

vec = [ 8,2,9,3,5,6;
        1,0,3,0,0,6;
        7,0,11,3,5,6;
        3,2,4,4,5,6];
%}

[pos_filas_ceros, pos_columnas_ceros] = find(vec == 0);
posiciones = [pos_filas_ceros, pos_columnas_ceros];
%rowcolP = posiciones(all(mod(vec, 2) == 0, 2), :);

vec = interpolacion_bilinealx(vec, posiciones);

function bayer = interpolacion_bilinealPrueba(bayer, posiciones)
  
    % Extraer las coordenadas de las posiciones
    rows = posiciones(:, 1);
    cols = posiciones(:, 2);
    
    % Calcular los índices de los elementos en las posiciones superiores e inferiores
    top_left_indices = sub2ind(size(bayer), rows-1, cols-1);
    top_right_indices = sub2ind(size(bayer), rows-1, cols+1);
    bottom_left_indices = sub2ind(size(bayer), rows+1, cols-1);
    bottom_right_indices = sub2ind(size(bayer), rows+1, cols+1);
    
    % Obtener los valores en las posiciones superiores e inferiores
    y1_top_left = bayer(top_left_indices);
    y2_top_right = bayer(top_right_indices);
    y1_bottom_left = bayer(bottom_left_indices);
    y2_bottom_right = bayer(bottom_right_indices);
    
    % Interpolación lineal en las posiciones superiores e inferiores
    x1 = cols-1;
    x2 = cols+1;
    x = cols;

    y_first = y1_top_left + (x - x1) .* (y2_top_right - y1_top_left) ./ (x2 - x1);
    y_second = y1_bottom_left + (x - x1) .* (y2_bottom_right - y1_bottom_left) ./ (x2 - x1);
    
    x = cols;
    % Interpolación bilineal
    y_second = y_first + (x - x1) .* (y_second - y_first) ./ (x2 - x1);
    % Asignar los valores interpolados a las posiciones actuales en la matriz
    bayer(sub2ind(size(bayer), rows, cols)) = y_second;
end


function bayer = interpolacion_bilineal(bayer, posiciones)
    x1 = 1;
    x = 2;
    x2 = 3;
    % Extraer las coordenadas de las posiciones
    rows = posiciones(:, 1);
    cols = posiciones(:, 2);
    
    % Calcular los índices de los elementos en las posiciones superiores e inferiores
    top_left_indices = sub2ind(size(bayer), rows-1, cols-1);
    top_right_indices = sub2ind(size(bayer), rows-1, cols+1);
    bottom_left_indices = sub2ind(size(bayer), rows+1, cols-1);
    bottom_right_indices = sub2ind(size(bayer), rows+1, cols+1);
    
    % Obtener los valores en las posiciones superiores e inferiores
    y1_top_left = bayer(top_left_indices);
    y2_top_right = bayer(top_right_indices);
    y1_bottom_left = bayer(bottom_left_indices);
    y2_bottom_right = bayer(bottom_right_indices);
    
    % Interpolación lineal en las posiciones superiores e inferiores
    y_first = y1_top_left + (x - x1) * (y2_top_right - y1_top_left) / (x2 - x1);
    y_second = y1_bottom_left + (x - x1) * (y2_bottom_right - y1_bottom_left) / (x2 - x1);
    
    % Interpolación bilineal
    y_second = y_first + (x - x1) * (y_second - y_first) / (x2 - x1);
    % Asignar los valores interpolados a las posiciones actuales en la matriz
    bayer(sub2ind(size(bayer), rows, cols)) = y_second;
end

function bayer = interpolacion_bilineal(bayer, posiciones)
    x1 = 1;
    x = 2;
    x2 = 3;
    % Extraer las coordenadas de las posiciones
    rows = posiciones(:, 1);
    cols = posiciones(:, 2);
    
    % Calcular los índices de los elementos en las posiciones superiores e inferiores
    top_left_indices = sub2ind(size(bayer), rows-1, cols-1);
    top_right_indices = sub2ind(size(bayer), rows-1, cols+1);
    bottom_left_indices = sub2ind(size(bayer), rows+1, cols-1);
    bottom_right_indices = sub2ind(size(bayer), rows+1, cols+1);
    
    % Obtener los valores en las posiciones superiores e inferiores
    y1_top_left = bayer(top_left_indices);
    y2_top_right = bayer(top_right_indices);
    y1_bottom_left = bayer(bottom_left_indices);
    y2_bottom_right = bayer(bottom_right_indices);
    
    % Interpolación lineal en las posiciones superiores e inferiores
    y_first = y1_top_left + (x - x1) * (y2_top_right - y1_top_left) / (x2 - x1);
    y_second = y1_bottom_left + (x - x1) * (y2_bottom_right - y1_bottom_left) / (x2 - x1);
    
    % Interpolación bilineal
    y_second = y_first + (x - x1) * (y_second - y_first) / (x2 - x1);
    % Asignar los valores interpolados a las posiciones actuales en la matriz
    bayer(sub2ind(size(bayer), rows, cols)) = y_second;
end