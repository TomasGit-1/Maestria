%Validamos primera y ultima
if all(bayer_rojo_completo(end,:) == 0)
   bayer_rojo_completo(end, :) = bayer_rojo_completo(end - 1, :);
end
if all(bayer_rojo_completo(:, end) == 0)
    bayer_rojo_completo(:, end) = bayer_rojo_completo(:, end - 1);
end

filas = bayer_rojo_completo([1, end], :);
columnas = bayer_rojo_completo(:, [1, end]);

bayer_rojo_completo = interpolarasignar(bayer_rojo_completo,filas);
bayer_rojo_completo = interpolarasignar_columnas(bayer_rojo_completo,columnas);


%Aplicando interpoleacion Lineal a los borde
filas = bayer_rojo_completo([1, end], :);
columnas = bayer_rojo_completo(:, [1, end]);
filas_no_cero = filas(any(filas ~= 0, 2), :);

[pos_filas_ceros, pos_columnas_ceros] = find(bayer_rojo_completo == 0);
posiciones_pares = [pos_filas_ceros(mod(pos_filas_ceros, 2) == 0), pos_columnas_ceros(mod(pos_columnas_ceros, 2) == 0)];
bayer_rojo_completo = interpolacion_bilineal(bayer_rojo_completo, posiciones_pares);

[pos_filas_ceros, pos_columnas_ceros] = find(bayer_rojo_completo == 0);
posiciones_impares = [pos_filas_ceros(mod(pos_filas_ceros, 2) ~= 0), pos_columnas_ceros(mod(pos_columnas_ceros, 2) ~= 0)];
bayer_rojo_completo = interpolacion_bilineal(bayer_rojo_completo, posiciones_impares);

[pos_filas_ceros, pos_columnas_ceros] = find(bayer_rojo_completo == 0);
posiciones_impares_pares = [pos_filas_ceros(mod(pos_filas_ceros, 2) ~= 0), pos_columnas_ceros(mod(pos_columnas_ceros, 2) == 0)];
bayer_rojo_completo = interpolacion_bilinealCruz(bayer_rojo_completo, posiciones_impares_pares);

[pos_filas_ceros, pos_columnas_ceros] = find(bayer_rojo_completo == 0);
bayer_rojo_completo = interpolacion_bilinealCruz(bayer_rojo_completo, [pos_filas_ceros, pos_columnas_ceros] );



%codifo 
disp("Funciones");

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




