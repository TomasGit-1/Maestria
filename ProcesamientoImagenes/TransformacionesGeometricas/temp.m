% Matriz original
matriz = [
    3 2 0 1 1 0 0;
    1 0 0 0 0 0 1;
    0 0 0 0 0 0 0;
    0 0 0 0 0 0 0;
    1 1 0 0 0 0 1;
    1 1 0 0 0 0 1;

];

[num_filas, num_columnas] = size(matriz);
for i=2:num_filas
   fila_actual = matriz(i,:);
   if all(fila_actual == 0)
      disp('Todos los elementos de la fila son cero');
      matriz(i,:) = matriz(i-1,:); 
   end
end

[num_filas, num_columnas] = size(matriz);
for i=2:num_columnas
   fila_actual = matriz(:,i);
   if all(fila_actual == 0)
      disp('Todos los elementos de la fila son cero');
      matriz(:,i) = matriz(:,i-1); 
   end
end






function matriz = AcompletarFilas(matriz)
    [num_filas, num_columnas] = size(matriz);
    for i=2:num_filas
       fila_actual = matriz(i,:);
       if all(fila_actual == 0)
          disp('Todos los elementos de la fila son cero');
          matriz(i,:) = matriz(i-1,:); 
       end
    end
    
    [num_filas, num_columnas] = size(matriz);
    for i=2:num_columnas
       fila_actual = matriz(:,i);
       if all(fila_actual == 0)
          disp('Todos los elementos de la fila son cero');
          matriz(:,i) = matriz(:,i-1); 
       end 
    end
end

function imagen_escala =  interpolacionBicubica(img)
   
    % Separar los canales de color de la imagen original
    canal_rojo = double(img(:,:,1));
    canal_verde = double(img(:,:,2));
    canal_azul = double(img(:,:,3));
    
    % Definir la cuadrícula de puntos de interpolación
    [x, y] = meshgrid(1:size(img, 2), 1:size(img, 1));
    
    % Calcular la interpolación bicúbica para cada canal de color
    nuevo_canal_rojo = interp2(x, y, canal_rojo, x, y, 'spline');
    nuevo_canal_verde = interp2(x, y, canal_verde, x, y, 'spline');
    nuevo_canal_azul = interp2(x, y, canal_azul, x, y, 'spline');
    
    % Combinar los canales interpolados en una nueva imagen a color
    imagen_suavizada = uint8(cat(3, nuevo_canal_rojo, nuevo_canal_verde, nuevo_canal_azul));
    
    % Mostrar la imagen suavizada
    imshow(imagen_suavizada);

end


function imagen_interpolada = interpolacionInter2(imagen_rgb)

    canal_rojo = imagen_rgb(:,:,1);
    canal_verde = imagen_rgb(:,:,2);
    canal_azul = imagen_rgb(:,:,3);
    
    canal_rojo = AcompletarFilas(canal_rojo);
    canal_verde = AcompletarFilas(canal_verde);
    canal_azul = AcompletarFilas(canal_verde);

    imagen_interpolada = cat(3, canal_rojo,canal_verde, canal_azul)

   
end

function imgInterpolada = interpolacionInterp1(img)
    imgInterpolada =uint8(zeros(size(img)));

    % Realizar interpolación lineal a lo largo de cada fila
    for i = 1:size(img, 1)
        fila = img(i, :);
        % Encontrar los índices de los valores que no son cero
        indices_no_ceros = find(fila ~= 0);
        valores_no_ceros = double(fila(indices_no_ceros));        
        % Encontrar los índices de los valores que son cero
        indices_ceros = find(fila == 0);
        tamCeros = size(indices_ceros);
        tamColor = size(fila)-10;
        if tamCeros(2) < tamColor(2)
            % Calcular la interpolación lineal usando interp1 con los mismos puntos de interpolación
            valores_interp = interp1(indices_no_ceros, valores_no_ceros, indices_ceros, 'spline');
            fila(indices_ceros) = uint8(valores_interp);   
            imgInterpolada(i, :) = fila;
        end
    end
end

function bayer = interpolacion_bilinealCruz(bayer, posiciones) 
    % Extraer las coordenadas de las posiciones
    rows = posiciones(:, 1);
    cols = posiciones(:, 2);
    % Calcular los índices de los elementos en las posiciones superiores e inferiores
    top_left_indices = sub2ind(size(bayer), rows, cols-1);
    top_right_indices = sub2ind(size(bayer), rows-1, cols);
    bottom_left_indices = sub2ind(size(bayer), rows+1, cols);
    bottom_right_indices = sub2ind(size(bayer), rows, cols+1);
    
     
    % Obtener los valores en las posiciones superiores e inferiores
    y1_top_left = bayer(top_left_indices);
    y2_top_right = bayer(top_right_indices);
    y1_bottom_left = bayer(bottom_left_indices);
    y2_bottom_right = bayer(bottom_right_indices);
    
    % Interpolación lineal en las posiciones superiores e inferiores
    x1 = cols-1;
    x2 = cols;
    x = cols;
    y_first = y1_top_left + (x - x1) .* (y2_top_right - y1_top_left) ./ (x2 - x1);
    x1 = cols;
    x2 = cols+1;
    y_second = y1_bottom_left + (x - x1) .* (y2_bottom_right - y1_bottom_left) ./ (x2 - x1);
    % Interpolación bilineal
    y_second = y_first + (x - x1) .* (y_second - y_first) ./ (x2 - x1);
    % Asignar los valores interpolados a las posiciones actuales en la matriz
    bayer(sub2ind(size(bayer), rows, cols)) = y_second;     
end

function bayer = interpolacion_bilineal(bayer, posiciones)
  
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









% 
    for i = 1:size(img, 1)
        fila = img(i, :);
        % Encontrar los índices de los valores que no son cero
        indices_no_ceros = find(fila ~= 0);
        valores_no_ceros = double(fila(indices_no_ceros));        
        % Encontrar los índices de los valores que son cero
        indices_ceros = find(fila == 0);
        tamCeros = size(indices_ceros);
        tamColor = size(fila)-10;
        if tamCeros(2) < tamColor(2)
            % Calcular la interpolación lineal usando interp1 con los mismos puntos de interpolación
            valores_interp = interp1(indices_no_ceros, valores_no_ceros, indices_ceros, 'linear');
            fila(indices_ceros) = uint8(valores_interp);   
            imgInterpolada(i, :) = fila;
        end
    end 
    }%
