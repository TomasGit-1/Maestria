if all(bayer_azul_completo(1,:) == 0)
   bayer_azul_completo(1, :) = bayer_azul_completo(2, :);
end
if all(bayer_azul_completo(:, 1) == 0)
    bayer_azul_completo(:, 1) = bayer_azul_completo(:, 2);
end

if all(bayer_azul_completo(end,:) == 0)
   bayer_azul_completo(end, :) = bayer_azul_completo(end - 1, :);
end
if all(bayer_azul_completo(:, end) == 0)
    bayer_azul_completo(:, end) = bayer_azul_completo(:, end - 1);
end

filas = bayer_azul_completo([1, end], :);
columnas = bayer_azul_completo(:, [1, end]);

bayer_azul_completo = interpolarasignar(bayer_azul_completo,filas);
bayer_azul_completo = interpolarasignar_columnas(bayer_azul_completo,columnas);

[pos_filas_ceros, pos_columnas_ceros] = find(bayer_azul_completo == 0);
posiciones_impares = [pos_filas_ceros(mod(pos_filas_ceros, 2) ~= 0), pos_columnas_ceros(mod(pos_columnas_ceros, 2) ~= 0)];
bayer_azul_completo = interpolacion_bilineal(bayer_azul_completo, posiciones_impares);

[pos_filas_ceros, pos_columnas_ceros] = find(bayer_azul_completo == 0);
posiciones_impares_pares = [pos_filas_ceros(mod(pos_filas_ceros, 2) ~= 0), pos_columnas_ceros(mod(pos_columnas_ceros, 2) == 0)];
bayer_azul_completo = interpolacion_bilinealCruz(bayer_azul_completo, posiciones_impares_pares);

[pos_filas_ceros, pos_columnas_ceros] = find(bayer_azul_completo == 0);
bayer_azul_completo = interpolacion_bilinealCruz(bayer_azul_completo, [pos_filas_ceros, pos_columnas_ceros] );

function bayer_completo = interpolarasignar(bayer_completo,filas)
    % Iterar sobre las filas de la matriz
    for i = 1:size(filas, 1)
        x = filas(i,:);
        indices_ceros = find(x == 0);
        indices_no_ceros = find(x ~= 0);
        x_interp = interp1(indices_no_ceros, x(indices_no_ceros), indices_ceros, 'linear');
        x_interp(isnan(x_interp)) = 0;
        x(indices_ceros) = x_interp;
        if i == 2
            bayer_completo(end, :) = x;
        else
            bayer_completo(i, :) = x;
        end
    end
end

function bayer_completo = interpolarasignar_columnas(bayer_completo,columnas)
    % Iterar sobre las columnas de la matriz
    for i = 1:size(columnas, 2)
        x = columnas(:, i);
        indices_ceros = find(x == 0);
        indices_no_ceros = find(x ~= 0);
        x_interp = interp1(indices_no_ceros, x(indices_no_ceros), indices_ceros, 'linear');
        x_interp(isnan(x_interp)) = 0;
        x(indices_ceros) = x_interp;
        if i == 2
            bayer_completo(:, end) = x;
        else
            bayer_completo(:, i) = x; 
        end
    end
end

function bayer_completo_temp = interpolacion_bilineal(bayer_completo_temp, posiciones)
    x1 = 1;
    x = 2;
    x2 = 3;
    % Extraer las coordenadas de las posiciones
    rows = posiciones(:, 1);
    cols = posiciones(:, 2);
    
    % Calcular los índices de los elementos en las posiciones superiores e inferiores
    top_left_indices = sub2ind(size(bayer_completo_temp), rows-1, cols-1);
    top_right_indices = sub2ind(size(bayer_completo_temp), rows-1, cols+1);
    bottom_left_indices = sub2ind(size(bayer_completo_temp), rows+1, cols-1);
    bottom_right_indices = sub2ind(size(bayer_completo_temp), rows+1, cols+1);
    
    % Obtener los valores en las posiciones superiores e inferiores
    y1_top_left = bayer_completo_temp(top_left_indices);
    y2_top_right = bayer_completo_temp(top_right_indices);
    y1_bottom_left = bayer_completo_temp(bottom_left_indices);
    y2_bottom_right = bayer_completo_temp(bottom_right_indices);
    
    % Interpolación lineal en las posiciones superiores e inferiores
    y_first = y1_top_left + (x - x1) * (y2_top_right - y1_top_left) / (x2 - x1);
    y_second = y1_bottom_left + (x - x1) * (y2_bottom_right - y1_bottom_left) / (x2 - x1);
    
    % Interpolación bilineal
    y_second = y_first + (x - x1) * (y_second - y_first) / (x2 - x1);
    
    % Asignar los valores interpolados a las posiciones actuales en la matriz
    bayer_completo_temp(sub2ind(size(bayer_completo_temp), rows, cols)) = y_second;

    %{
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
    %}
end

function bayer_completo_temp = interpolacion_bilinealCruz(bayer_completo_temp, posiciones) 
    % Obtener las coordenadas para la interpolación
    x1 = 1;
    x = 2;
    x2 = 3;
    
    % Extraer las coordenadas de las posiciones
    rows = posiciones(:, 1);
    cols = posiciones(:, 2);
    
    % Interpolación lineal en la fila superior
    y1 = bayer_completo_temp(sub2ind(size(bayer_completo_temp), rows, cols-1));
    y2 = bayer_completo_temp(sub2ind(size(bayer_completo_temp), rows-1, cols));
    y_first = y1 + (x - x1) * (y2 - y1) / (x2 - x1);
    
    % Interpolación lineal en la fila inferior
    y1 = bayer_completo_temp(sub2ind(size(bayer_completo_temp), rows+1, cols));
    y2 = bayer_completo_temp(sub2ind(size(bayer_completo_temp), rows, cols+1));
    y_second = y1 + (x - x1) * (y2 - y1) / (x2 - x1);
    
    % Interpolación bilineal
    y_second = y_first + (x - x1) * (y_second - y_first) / (x2 - x1);
    
    % Asignar los valores interpolados a las posiciones actuales en la matriz
    bayer_completo_temp(sub2ind(size(bayer_completo_temp), rows, cols)) = y_second;
    %{
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
    %}
end




