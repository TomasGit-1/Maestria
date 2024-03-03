
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
