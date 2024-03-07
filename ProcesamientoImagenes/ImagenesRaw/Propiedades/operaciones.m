
%for fila = 1:num_filas
%    for col = 1:num_columnas
%        elemento = subBayer(fila, col)
%        disp(['Elemento en la posición (' num2str(fila) ',' num2str(col) '): ' num2str(elemento)]);
%    end
%end




bayer_normalizado

%max_valor = max(bayerImage(:));

%bayerinfo=rawinfo(fileName)
%bayerinfo.ColorInfo
%imshow(bayerImage,[]);
%filename = 'paisaje.ARW';
%bayerImage = imread(filename);
%imshow(bayerImage, []);

%Interpolacion
%pixeles_a_interpolar = (bayer_rojo_completo == 0);
%indices_interpolar = find(pixeles_a_interpolar);
%matriz_interpolada(indices_interpolar) = imresize(bayer_rojo_completo(indices_interpolar), size(bayer_rojo_completo(indices_interpolar)), 'bilinear');

%valores_interpolar = bayer_rojo_completo(pixeles_a_interpolar);  % Obtener los valores a interpolar
%valores_interpolar_redimensionados = imresize(valores_interpolar, size(valores_interpolar), 'bilinear');  % Interpolar los valores
%matriz_interpolada(indices_interpolar) = valores_interpolar_redimensionados;  % Asignar los valores interpolados a matriz_interpolada

%matriz_interpoladatemp = imresize(bayer_rojo_completo, size(bayer_rojo_completo), 'bilinear');
%matriz_interpolada = matriz_interpoladatemp .* double(pixeles_a_interpolar) + bayer_rojo_completo;
%imshow(matriz_interpolada);



% Generar una máscara de los píxeles a interpolar
pixeles_a_interpolar = (bayer_rojo_completo == 0);
% Obtener los índices de los píxeles a interpolar
indices_interpolar = find(pixeles_a_interpolar);
% Interpolar solo en los píxeles a interpolar
valores_interpolar = bayer_rojo_completo(indices_interpolar);
valores_interpolar_redimensionados = imresize(valores_interpolar, size(valores_interpolar), 'bilinear');
% Crear una matriz temporal para almacenar los valores interpolados
matriz_interpolada_temp = bayer_rojo_completo;
matriz_interpolada_temp(indices_interpolar) = valores_interpolar_redimensionados;
% Combinar la matriz temporal con la matriz original para obtener la matriz interpolada final
matriz_interpolada = matriz_interpolada_temp;



    y1 = sub2ind(size(bayer_completo_temp), rows, cols-1);
    y2 = sub2ind(size(bayer_completo_temp), rows-1, cols);
    y_first = y1 + (x - x1) * (y2 - y1) / (x2 - x1);
    
    % Interpolación lineal en la fila inferior
    y1 = sub2ind(size(bayer_completo_temp), rows+1, cols);
    y2 = (sub2ind(size(bayer_completo_temp), rows, cols+1);
    y_second = y1 + (x - x1) * (y2 - y1) / (x2 - x1);
    
    % Interpolación bilineal
    y_second = y_first + (x - x1) * (y_second - y_first) / (x2 - x1);
    
    % Asignar los valores interpolados a las posiciones actuales en la matriz
    bayer_completo_temp(sub2ind(size(bayer_completo_temp), rows, cols)) = y_second;
