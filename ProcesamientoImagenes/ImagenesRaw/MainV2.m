fileName = 'paisaje.ARW';
bayerImage = rawread(fileName);
bayerInfo = rawinfo(fileName);
cameraToRGB = bayerInfo.ColorInfo.CameraTosRGB;
%Definimos las matriz a utilizar
bayer_rggb = uint16([800,800;800,800]);
balanceB = [2.964,1; 1, 1.832];
%subBayer = bayerImage(500:1000, 500:1000);

subBayer = bayerImage(1:10, 1:10);

%subBayer = bayerImage;

bayerNomalizado = normalizate_bayer(subBayer,bayer_rggb);
bayerBalanceB = balance_blancos(bayerNomalizado,balanceB);


bayerRojo = separar_rojo(bayerBalanceB);
bayerRI = interpolacionRojo(bayerRojo);

bayerVerde = separarVerde(bayerBalanceB);
bayerVI = interpolacionVerde(bayerVerde);

bayerAzul = separarAzul(bayerBalanceB);
bayerAI = interpolacionAzul(bayerAzul);

bayerColor = espacionRGB(bayerRI, bayerVI, bayerAI, cameraToRGB );
bayerColor =generate_gamma(bayerColor);

%{

figure(1)
    subplot(2, 2, 1);
    imshow(bayerNomalizado, []);
    title('Imagen normalizada');

    subplot(2, 2, 2);
    imshow(bayerBalanceB, []);
    title('Balance de blancos');

figure(2)
    imshow(cat(2, bayerVerde, bayerVI));
    title("Canal Verde");

figure(3)
    imshow(cat(2, bayerAzul, bayerAI));
    title("Canal Azul")

figure(4)
    imagenColor1 = cat(3, bayerRojo, bayerVerde, bayerAzul);  
    imshow(imagenColor);

figure(4)
    imagenColor2 = cat(3, bayerRojo, bayerVerde, bayerAzul);  
    imshow(imagenColor)

figure(5)
    imshow(bayerColor);
%}

imnprimir(subBayer, bayerNomalizado, bayerBalanceB, bayerRojo, bayerVerde,bayerAzul, bayerRI,bayerVI,bayerAI,bayerColor);

function bayerNormalizate = normalizate_bayer(subBayer,bayer_rggbT)
    funcion_resta = @(block_struct) block_struct.data - bayer_rggbT;
    resultado = blockproc(subBayer, [2, 2], funcion_resta);
    max_valor = max(resultado, [], 'all');
    bayerNormalizate = double(resultado) / double(max_valor);
end

function bayer_balance_blancos = balance_blancos(bayer_normalizado,balanceB)
    funcion_ajuste_W = @(block_struct) block_struct.data * balanceB;
    bayer_balance_blancos = blockproc(bayer_normalizado, [2, 2], funcion_ajuste_W);
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
    posiciones = [pos_filas_ceros, pos_columnas_ceros];

    bayerRI = interpolacion_bilinealCruz(bayerRI, [pos_filas_ceros, pos_columnas_ceros]);
end

function bayerVI =  interpolacionVerde(bayerVI)

    filas = bayerVI([1, end], :);
    columnas = bayerVI(:, [1, end]);
    bayerVI(1,1) =  bayerVI(1,2);
    bayerVI(end,end) =  bayerVI(end-1);
    bayerVI = interpolar_bordes(bayerVI);
    [pos_filas_ceros, pos_columnas_ceros] = find(bayerVI == 0);
    posiciones = [pos_filas_ceros, pos_columnas_ceros];
    %rowcolP = posiciones(all(mod(posiciones, 2) == 0, 2), :);
    bayerVI = interpolacion_bilinealCruz(bayerVI, posiciones);
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

    %Aplicamos lineal a las filas pares
    filas_pares = 2:2:size(bayerAI, 1);
    filas_con_cero = filas_pares(any(bayerAI(filas_pares, :) == 0, 2));
    bayer_filas_pares = bayerAI(filas_con_cero, :);

    % Interpolar las filas pares que tienen al menos un 0

    bayer_filas_pares_interp = interpolar(bayer_filas_pares);
    
    % Actualizar las filas interpoladas en la matriz original
    bayerAI(filas_con_cero, :) = bayer_filas_pares_interp;   
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

function valores_interp = interpolar(valores)
    %indices_no_ceros = find(~indices_ceros);
    %valores_interp = valores;
    %valores_interp(indices_ceros) = interp1(indices_no_ceros, valores(indices_no_ceros), find(indices_ceros), 'linear');

    % Encuentra los índices de los valores no cero y los valores cero en el vector
    indices_no_ceros = find(valores ~= 0);
    indices_ceros = find(valores == 0);
    
    % Encuentra los dos índices más cercanos que no son cero para cada valor cero
    x0_indices = max(bsxfun(@lt, indices_no_ceros', indices_ceros), [], 1);
    x1_indices = min(bsxfun(@gt, indices_no_ceros', indices_ceros), [], 1);
    
    % Obtiene los valores correspondientes de x0 y x1
    x0 = indices_no_ceros(x0_indices);
    x1 = indices_no_ceros(x1_indices);
    
    % Obtiene los valores de los puntos conocidos más cercanos
    y0 = valores(x0);
    y1 = valores(x1);
    
    % Realiza la interpolación utilizando interp1
    interpolated_values = interp1([x0; x1], [y0; y1], indices_ceros);
    valores_interp = valores;

    % Asigna los valores interpolados al vector original en las posiciones de los valores cero
    valores_interp(indices_ceros) = interpolated_values;
    
    % Rellena los valores NaN con una interpolación adicional
    nan_indices = isnan(valores_interp);
    valores_interp(nan_indices) = interp1(indices_no_ceros, valores(indices_no_ceros), find(nan_indices), 'linear');
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
    
    %ColorR = rgb(:, :, 1);
    %ColorV = rgb(:, :, 2);
    %ColorA = rgb(:, :, 3);
    %{
    ColorR = zeros(filas, columnas);
    ColorV = zeros(filas, columnas);
    ColorA = zeros(filas, columnas);    
    for i = 1:filas
        for j = 1:columnas
            r = bayerRI(i,j);
            v = bayerVI(i, j);
            b = bayerAI(i, j);
            rgb = [r; v;b];
            rgb = cameraToRGB * rgb;
            ColorR(i,j) = rgb(1);
            ColorV(i,j) = rgb(2);
            ColorA(i,j) = rgb(3);
        end
    end
    %}
end

function imagenColor = generate_gamma(bayerColor)   
    gamma = 1/2.222;
    ColorR = bayerColor(:,:,1);
    ColorV = bayerColor(:,:,2);
    ColorA = bayerColor(:,:,3);
    % Aplicar la corrección gamma a cada canal de color
    ColorR_corregido = ColorR .^ (1/gamma);
    ColorV_corregido = ColorV .^ (1/gamma);
    ColorA_corregido = ColorA .^ (1/gamma);
    
    % Asegurarse de que los valores estén en el rango [0, 1]
    %ColorR_corregido = min(max(ColorR_corregido, 0), 1);
    %ColorV_corregido = min(max(ColorV_corregido, 0), 1);
    %ColorA_corregido = min(max(ColorA_corregido, 0), 1);
    
    % Mostrar los resultados
    imagenColor = cat(3, ColorR_corregido, ColorV_corregido, ColorA_corregido);    
end

function imnprimir(subBayer, bayerNomalizado, bayerBalanceB, bayerRojo, bayerVerde,bayerAzul, bayerRI,bayerVI,bayerAI,bayerColor)
    filas = 5;
    columnas = 3;
    subplot(filas, columnas, 1); % Subplot de 1 fila y 3 columnas, primer gráfico
    imshow(subBayer, []); % Mostrar bayerImage
    title('Imagen original');
    
    subplot(filas, columnas, 2);
    imshow(bayerNomalizado, []);
    title('Imagen normalizada');
    
    subplot(filas, columnas, 3);
    imshow(bayerBalanceB, []); 
    title('Imagen normalizada blanco');
    
    subplot(filas, columnas, 4);
    imshow(bayerRojo, []);
    title('Mosaico R');
    
    subplot(filas, columnas, 5); 
    imshow(bayerVerde, []); 
    title('Mosaico GG');
    
    subplot(filas, columnas, 6); 
    imshow(bayerAzul, []);
    title('Mosaico B');
    
    subplot(filas, columnas, 7);
    imshow(bayerRI, []);
    title('Mosaico Completo R');
    
    subplot(filas, columnas, 8); 
    imshow(bayerVI, []); 
    title('Mosaico Completo GG');
    
    subplot(filas, columnas, 9); 
    imshow(bayerAI, []);
    title('Mosaico Completo A');
    
    imagen_real = real(bayerColor);
    subplot(filas, columnas, 10);
    imshow(imagen_real, []);
    title('Color');
end 
