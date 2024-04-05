clear all;
imgFlowers = imread("flowers.jpg");
imgCube = imread("cube.jpg");

tx = 12;
ty = 6;
imgTraslationFlowers = traslacion(imgFlowers, tx, ty);

tx = 120;
ty = 0;
imgTraslationCube = traslacion(imgCube, tx, ty);

ex = 0.222;
ey = 0.222;
imgEscaladoFlowers = escalado(imgFlowers, ex, ey);

ex = 1.2;
ey = 1.2;
imgEscaladoFlowers2 = escalado(imgFlowers, ex, ey);
%imgEscaladoFlowers2 = interpolacionBicubica(imgEscaladoFlowers2);

%Inclininacion
a = 0.4;
imgSesgadoFlowers = sesgado(imgFlowers, a);
a = 0.1;
imgSesgadoCube = sesgado(imgCube, a);

a = 0.2;
imgRotacionFlower = rotacion(imgFlowers, a);
a = 0.4;
imgRotacionCube = rotacion(imgFlowers, a);


figure(1)
    subplot(1,4,[1,2]);
    imshow(imgFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgCube,[]);
    title("Original");
%{
figure(2)
    subplot(1,4,[1,2]);
    imshow(imgTraslationFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgTraslationCube,[]);
    title("Traslacion");
figure(3)
    subplot(1,4,[1,2]);
    imshow(imgEscaladoFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgEscaladoFlowers2,[]);
    title("Escalado");
%}

%{
figure(4)
    subplot(1,4,[1,2]);
    imshow(imgSesgadoFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgSesgadoCube,[]);
    title("Sesgado");

%}

a = 45;
imgRotacionFlower = rotacion(imgFlowers, a);
a = 10;
imgRotacionCube = rotacion(imgFlowers, a);
%imgRotacionCube =imgRotacionCube(1:10,1:100);
imgRotacionCube2 = interpolacionSinExtremos(imgRotacionCube);

figure(5)
subplot(1,4,[1,2]);
imshow(imgRotacionFlower,[]);
subplot(1,4,[3,4]);
imshow(imgRotacionCube,[]);
title("Rotacion");

function imgTranslation = traslacion(img, tx, ty)
    for y = 1:size(img,1)
        for x=1:size(img,2)
            xNew = x + tx;
            yNew = y + ty;
            if xNew >= 1 && xNew <= size(img, 2) && yNew >= 1 && yNew <= size(img, 1)
                imgTranslation(yNew,xNew,:) = img(y,x,:);
            end 
        end
    end
end

function imgEscalado = escalado(img, ex, ey)
    for y = 1:size(img,1)
        for x=1:size(img,2)
            xNew = uint16(x * ex);
            yNew = uint16(y * ey);
            if xNew >= 1 && xNew <= size(img, 2) && yNew >= 1 && yNew <= size(img, 1)
                imgEscalado(yNew,xNew,:) = img(y,x,:);
            end 
        end
    end
end

function imgSesgado = sesgado(img, a)
    for y = 1:size(img,1)
        for x=1:size(img,2)
            xNew = uint16(x + (a*y));
            yNew = y;
            if xNew >= 1 && xNew <= size(img, 2) && yNew >= 1 && yNew <= size(img, 1)
                imgSesgado(yNew,xNew,:) = img(y,x,:);
            end 
        end
    end
end


function imgRotacion = rotacion(img,a)
    centro_x = size(img,1) / 2;
    centro_y = size(img,2) / 2;
      for y = 1:size(img,1)
            for x=1:size(img,2)
                x_adjusted = x - centro_x;
                y_adjusted = y - centro_y;
                xNew = uint16(x_adjusted * cos(a) - y_adjusted * sin(a) + centro_x);
                yNew = uint16(x_adjusted * sin(a) + y_adjusted * cos(a) + centro_y);
                if xNew >= 1 && xNew <= size(img, 2) && yNew >= 1 && yNew <= size(img, 1)
                    imgRotacion(yNew,xNew,:) = img(y,x,:);
                end 
            end
      end
end



function imagen_interpolada = interpolacion(imagen_rgb)

    canal_rojo = imagen_rgb(:,:,1);
    canal_verde = imagen_rgb(:,:,2);
    canal_azul = imagen_rgb(:,:,3);
    
    canal_rojo = interpolacionInterp1(canal_rojo);
    canal_verde = interpolacionInterp1(canal_verde);
    canal_azul = interpolacionInterp1(canal_verde);

    imagen_interpolada = cat(3, canal_rojo,canal_verde, canal_azul)

   
end


function img = interpolacionSinExtremos(img)
    imgInterpolada =uint8(zeros(size(img)));
    for i = 1:size(img, 1)
        fila = img(i, :);
        % Encuentra los índices de los píxeles que no son negros
        indices_no_negros = find(fila ~= 0);
    
        % Verifica si hay al menos dos píxeles no negros para poder realizar interpolación
        if numel(indices_no_negros) >= 2
            % Calcula la interpolación lineal usando solo los píxeles no negros
            valores_no_negros = double(fila(indices_no_negros));
            valores_interp = interp1(indices_no_negros, valores_no_negros, 1:numel(fila), 'linear');    
            % Asigna los valores interpolados a los píxeles negros dentro del rango de píxeles no negros
            fila_interpolada = fila;
            fila_interpolada(fila == 0 & 1:numel(fila) >= indices_no_negros(1) & 1:numel(fila) <= indices_no_negros(end)) = valores_interp(fila == 0 & 1:numel(fila) >= indices_no_negros(1) & 1:numel(fila) <= indices_no_negros(end));
        else
            % Si hay menos de dos píxeles no negros, simplemente asigna la fila original
            fila_interpolada = fila;
        end
        img(i, :) = fila_interpolada;
    end
end

function imgInterpolada = interpolacionInterp1(img)
    imgInterpolada =uint8(zeros(size(img)));
    for i = 1:size(img, 1)
        fila = img(i, :);
        
        % Encontrar los índices de los valores que no son cero
        indices_no_ceros = find(fila ~= 0);
        valores_no_ceros = double(fila(indices_no_ceros));        
        
        % Verificar si hay ceros al principio y al final de la fila
        if numel(indices_no_ceros) < numel(fila) % Si hay ceros
            % Encontrar el índice del primer valor no cero
            primer_no_cero = indices_no_ceros(1);
            % Encontrar el índice del último valor no cero
            ultimo_no_cero = indices_no_ceros(end);
            
            % Obtener solo los índices de los ceros que están dentro del rango de valores no cero
            indices_ceros = setdiff(primer_no_cero:ultimo_no_cero, indices_no_ceros);
            
            % Calcular la interpolación lineal solo para los ceros dentro del rango
            if ~isempty(indices_ceros)
                valores_interp = interp1(indices_no_ceros, valores_no_ceros, indices_ceros, 'linear');
                % Asignar los valores interpolados a los ceros dentro del rango
                fila(indices_ceros) = uint8(valores_interp);   
            end
        end
        
        % Asignar la fila interpolada a la imagen interpolada
        imgInterpolada(i, :) = fila;
    end

   
end

