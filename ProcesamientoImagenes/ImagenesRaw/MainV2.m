fileName = 'paisaje.ARW';
bayerImage = rawread(fileName);
bayerInfo = rawinfo(fileName);
cameraToRGB = bayerInfo.ColorInfo.CameraTosRGB;
%Definimos las matriz a utilizar
%bayer_rggb = uint16([800,800;800,800]);
bayer_rggb = reshape(bayerInfo.ColorInfo.BlackLevel,2,2);
%balanceB = [2.964,1; 1, 1.832];
balanceB = reshape(bayerInfo.ColorInfo.CameraAsTakenWhiteBalance./ 1024, 2, 2);

subBayer = bayerImage(500:1800, 500:2000);
subBayer = bayerImage(1000:1006, 1000:1006);
subBayer = bayerImage(1:10, 1000:1010);
%subBayer = bayerImage;

bayerNomalizado = normalizate_bayer(subBayer,bayer_rggb);
%bayerNomalizado = max(0,bayerNomalizado);
bayerBalanceB = balance_blancos(bayerNomalizado,balanceB);

bayerRojo = separar_rojo(bayerBalanceB);
bayerVerde = separarVerde(bayerBalanceB);
bayerAzul = separarAzul(bayerBalanceB);

bayerRI = interpolacionRojo(bayerRojo);
bayerVI = interpolacionVerde(bayerVerde);
bayerAI = interpolacionAzul(bayerAzul);

bayerColorAG = espacionRGB(bayerRI, bayerVI, bayerAI, cameraToRGB );
bayerColor =generate_gamma(bayerColorAG);

figure()
    imshow(bayerImage, []);
    title('Imagen Original');

figure()
    imshow(bayerNomalizado, []);
    title('Imagen normalizada');
figure()
    imshow(bayerBalanceB, []);
    title('Balance de blancos');
figure()
    imshow(bayerRI);
    title("Canal Rojo");
figure()
    imshow(bayerVI);
    title("Canal Verde");
figure()
    imshow(bayerAI);
    title("Canal Azul");
figure()
    imshow(bayerColorAG);    
    title("Antes de Gamma");
figure()
    imshow(bayerColor);    
    title("Final");


%imnprimir(subBayer, bayerNomalizado, bayerBalanceB, bayerRojo, bayerVerde,bayerAzul, bayerRI,bayerVI,bayerAI,bayerColor);

function bayerNormalizate = normalizate_bayer(subBayer,bayer_rggbT)
    funcion_resta = @(block_struct) block_struct.data - bayer_rggbT;
    resultado =double( blockproc(subBayer, [2, 2], funcion_resta));
    max_valor = double(max(max(resultado)));
    bayerNormalizate = resultado ./ max_valor;
end

function bayer_balance_blancos = balance_blancos(bayer_normalizado,balanceB)
    funcion_ajuste_W = @(block_struct) block_struct.data .* balanceB;
    bayer_balance_blancos = double(blockproc(bayer_normalizado, [2, 2], funcion_ajuste_W));
end

function bayerRojo = separar_rojo(bayer)
    %selecciona los elementos en las filas impares y columnas impares
    rojo= bayer(1:2:end, 1:2:end);
    [filas, columnas] = size(rojo);
    bayerRojo = zeros(filas * 2, columnas * 2, 'like', rojo);
    bayerRojo(1:2:end, 1:2:end) = rojo;
end

function bayerVerde = separarVerde(bayer)
    %filas impares y columnas pares
    verde1 = bayer(1:2:end, 2:2:end); 
    [filas, columnas] = size(verde1);
    bayerVerde = zeros(filas * 2, columnas * 2, 'like', verde1);
    bayerVerde(1:2:end, 2:2:end) = verde1;
   
    %Filas pares y Columnas impares
    verde2 = bayer(2:2:end, 1:2:end); 
    bayerVerde(2:2:end, 1:2:end) = verde2;
    %bayerVerde(2:2:end, 1:2:end) = bayerVerde2C;
end

function bayerAzul = separarAzul(bayer)
    %Seleccionando Filas pares y Columnnas impares pero aumentando 2
    azul = bayer(2:2:end, 2:2:end); 
    [filas, columnas] = size(azul);
    bayerAzul= zeros(filas * 2, columnas * 2, 'like', azul);
    bayerAzul(2:2:end, 2:2:end) = azul;
end 

function bayerRI = interpolacionRojo(bayerRI)
    if all(bayerRI(end,:) == 0)
       bayerRI(end, :) = bayerRI(end - 1, :);
    end
    if all(bayerRI(:, end) == 0)
        bayerRI(:, end) = bayerRI(:, end - 1);
    end
    bayerRI = interpolar_bordes(bayerRI);
    
    [pos_filas_ceros, pos_columnas_ceros] = find(bayerRI == 0);
    posiciones = [pos_filas_ceros, pos_columnas_ceros];
    %Buscamos las pares
    rowcolP = posiciones(all(mod(posiciones, 2) == 0, 2), :);
    bayerRI = interpolacion_bilineal(bayerRI, rowcolP);
    %Pasamos el resto de posiciones
    [pos_filas_ceros, pos_columnas_ceros] = find(bayerRI == 0);
    bayerRI = interpolacion_bilinealCruz(bayerRI, [pos_filas_ceros, pos_columnas_ceros]);
end

function bayerVI =  interpolacionVerde(bayerVI)
    filas = bayerVI([1, end], :);
    columnas = bayerVI(:, [1, end]);
    bayerVI(1,1) =  bayerVI(1,2);
    bayerVI(end,end) =  bayerVI(end-1);
    %bayerVI = interpolar_bordes(bayerVI);
       
    
    for i=1:size(bayerVI)
        bayerVI(i,:) = interpolar16(bayerVI(i,:));    
    end 
    
    %[pos_filas_ceros, pos_columnas_ceros] = find(bayerVI == 0);
    %posiciones = [pos_filas_ceros, pos_columnas_ceros];
    %rowcolP = posiciones(all(mod(posiciones, 2) == 0, 2), :);
    %bayerVI = interpolacion_bilinealCruz(bayerVI, posiciones);
end 

function bayerAI = interpolacionAzul(bayerAI)
    if all(bayerAI(1,:) == 0)
       bayerAI(1, :) = bayerAI(2, :);
    end
    if all(bayerAI(:, 1) == 0)
        bayerAI(:, 1) = bayerAI(:, 2);
    end
    
    if all(bayerAI(end,:) == 0)
       bayerAI(end, :) = bayerAI(end - 1, :);
    end
    if all(bayerAI(:, end) == 0)
        bayerAI(:, end) = bayerAI(:, end - 1);
    end
    filas = bayerAI([1, end], :);
    columnas = bayerAI(:, [1, end]);
    bayerAI = interpolar_bordes(bayerAI); 
    % Obtener las posiciones de los elementos iguales a cero
    [pos_filas_ceros, pos_columnas_ceros] = find(bayerAI == 0);
    % Obtener las posiciones de las filas impares
    pos_filas_impares = pos_filas_ceros(mod(pos_filas_ceros, 2) == 1);
    % Obtener las posiciones de las columnas impares correspondientes a las filas impares
    pos_columnas_impares = pos_columnas_ceros(mod(pos_columnas_ceros, 2) == 1);
    posiciones_sin_repetir = unique([pos_filas_impares, pos_columnas_impares], 'rows');
    bayerAI = interpolacion_bilineal(bayerAI, posiciones_sin_repetir );

    [pos_filas_ceros, pos_columnas_ceros] = find(bayerAI == 0);
    bayerAI = interpolacion_bilinealCruz(bayerAI, [pos_filas_ceros, pos_columnas_ceros] );

end 

function bayer = interpolar_bordes(bayer)    
    % Interpolar en el borde superior
    bayer(1,:) = interpolar(bayer(1,:));
    % Interpolar en el borde inferior
    bayer(end, :) = interpolar(bayer(end,:));
    % Interpolar en el borde izquierdo
    bayer(:, 1) = interpolar(bayer(:,1));    
    % Interpolar en el borde derecho
    bayer(:, end) = interpolar(bayer(:,end));   
end

function valores = interpolar(valores)
    % Encontrar los índices de los valores que no son cero
    indices_no_ceros = find(valores ~= 0);
    valores_no_ceros = valores(indices_no_ceros);
    
    % Encontrar los índices de los valores que son cero
    indices_ceros = find(valores == 0);
    
    % Calcular la interpolación lineal usando interp1 con los mismos puntos de interpolación
    valores_interp = interp1(indices_no_ceros, valores_no_ceros, indices_ceros, 'linear');
    %valores_interp(valores_interp < 0) = 0;
    %valores_interp(valores_interp > 1) = 1;  
    % Asignar los valores interpolados al vector original
    valores(indices_ceros) = valores_interp;
end

function valores = interpolar16(valores)
    % Encontrar los índices de los valores que no son cero
    indices_no_ceros = find(valores ~= 0);
    valores_no_ceros = valores(indices_no_ceros);
    
    % Encontrar los índices de los valores que son cero
    indices_ceros = find(valores == 0);
    
    % Calcular la interpolación lineal usando interp1 con los mismos puntos de interpolación
    valores_interp = interp1(indices_no_ceros, valores_no_ceros, indices_ceros, 'pchip');
    %valores_interp(valores_interp < 0) = 0;
    %valores_interp(valores_interp > 1) = 1;  
    % Asignar los valores interpolados al vector original
    valores(indices_ceros) = valores_interp;
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

function bayer3D = espacionRGB(bayerRI, bayerVI, bayerAI, cameraToRGB)
    [filas, columnas] = size(bayerRI);
    bayer3D = cat(3, bayerRI, bayerVI, bayerAI);
    bayer_reshaped = reshape(bayer3D, [], 3)';
    rgb_reshaped = cameraToRGB * bayer_reshaped;
    bayer3D = reshape(rgb_reshaped', filas, columnas, []);
    %bayer3D(bayer3D < 0) = 0;
end

function imagenColor = generate_gamma(bayerColor) 
    %gamma = 1/2.222;
    gamma = 0.7;
    a_max = max(bayerColor(:));
    bayerColor(:,:,1) = bayerColor(:,:,1) .^ gamma;
    % Corrección gamma para el canal verde
    bayerColor(:,:,2) = bayerColor(:,:,2) .^ gamma;
    % Corrección gamma para el canal azul
    bayerColor(:,:,3) = bayerColor(:,:,3).^ gamma;

    %bayerColor = (double(bayerColor) / 255) .^ gamma * 255; % Canal G
    %bayerColor = (bayerColor/a_max ).^ gamma;
    imagenColor = bayerColor;
end

