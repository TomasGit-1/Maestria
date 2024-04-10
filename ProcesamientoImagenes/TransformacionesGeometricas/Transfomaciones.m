clear all;
imgFlowers = imread("flowers.jpg");
imgCube = imread("cube.jpg");

figure(1)
    subplot(1,4,[1,2]);
    imshow(imgFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgCube,[]);
    title("Original");


tx = 12;
ty = 6;
imgTraslationFlowers = traslacion(imgFlowers, tx, ty);

tx = 120;
ty = 0;
imgTraslationCube = traslacion(imgCube, tx, ty);


figure(2)
    subplot(1,4,[1,2]);
    imshow(imgTraslationFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgTraslationCube,[]);
    title("Traslacion");


ex = 0.222;
ey = 0.222;
imgEscaladoFlowers = escalado(imgFlowers, ex, ey);
imgEscaladoFlowers = interpolacionRGB(imgEscaladoFlowers);
imgEscaladoFlowers = interpolacionRGBHorizontal(imgEscaladoFlowers);

ex = 1.2;
ey = 1.2;
imgEscaladoFlowers2 = escalado(imgFlowers, ex, ey);
imgEscaladoFlowers2 = interpolacionRGB(imgEscaladoFlowers2);
imgEscaladoFlowers2 = interpolacionRGBHorizontal(imgEscaladoFlowers2);

figure(3)
    subplot(1,4,[1,2]);
    imshow(imgEscaladoFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgEscaladoFlowers2,[]);
    title("Escalado");

%Inclininacion
a = 0.4;
imgSesgadoFlowers = sesgado(imgFlowers, a);
a = 0.1;
imgSesgadoCube = sesgado(imgCube, a);

figure(4)
    subplot(1,4,[1,2]);
    imshow(imgSesgadoFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgSesgadoCube,[]);
    title("Sesgado");

a = 45;
imgRotacionFlower = rotacion(imgFlowers, a);
imgRotacionFlower = interpolacionRGB(imgRotacionFlower);

a = 10;
imgRotacionCube = rotacion(imgFlowers, a);
imgRotacionCube = interpolacionRGB(imgRotacionCube);

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

function img = interpolacionRGB(img)    
    [altura, ancho, ~] = size(img);
    for i = 1:altura
        fila = squeeze(img(i, :, :)); % Convertir la fila en una matriz 512x3 (canales de color)
        primer_no_cero = find(any(fila ~= 0, 2), 1, 'first'); % Encontrar el primer píxel no negro en cualquier canal
        ultimo_no_cero = find(any(fila ~= 0, 2), 1, 'last'); % Encontrar el último píxel no negro en cualquier canal
        sub_fila = fila(primer_no_cero:ultimo_no_cero, :); % Extraer la subfila con píxeles no negros
        indices_no_negros = find(any(sub_fila ~= 0, 2)); % Encontrar los índices de los píxeles no negros en la subfila
        if numel(indices_no_negros) >= 2
            % Interpolar las intensidades utilizando las posiciones relativas
            valores_no_negros = double(sub_fila(indices_no_negros, :));
            indices_negros = find(all(sub_fila == 0, 2));
            posiciones_interp = indices_negros;
            valores_interp = interp1(indices_no_negros, valores_no_negros, posiciones_interp, 'linear');

            % Asignar los valores interpolados solo a los píxeles originales que eran negros
            sub_fila(indices_negros, :) = valores_interp;

            % Asignar la sub_fila interpolada a la fila original
            fila(primer_no_cero:ultimo_no_cero, :) = sub_fila;
        end
        
        % Asignar la fila interpolada a la imagen original
        img(i, :, :) = fila;
    end
end

function img = interpolacionRGBHorizontal(img)    
    [altura, ancho, ~] = size(img);
    for j = 1:ancho
        columna = squeeze(img(:, j, :));     
        indices_negros = find(all(columna == 0, 2));
        if numel(indices_negros) >= 2
            intensidades_no_negras = double(columna(~all(columna == 0, 2), :));
            posiciones_no_negras = find(~all(columna == 0, 2));            
            posiciones_interp = indices_negros;
            valores_interp = interp1(posiciones_no_negras, intensidades_no_negras, posiciones_interp, 'linear', 'extrap');            
            columna(indices_negros, :) = valores_interp;
        end        
        img(:, j, :) = columna;
    end
end
