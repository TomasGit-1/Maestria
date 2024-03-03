[fila, columana] = size(bayer_rojo_completo)

% Obtener las dimensiones de las matrices
[filas, columnas] = size(bayer_rojo_completo);

r = reshape(bayer_rojo_completo, [], 1);
g = reshape(bayer_verde1_completo, [], 1);
b = reshape(bayer_azul_completo, [], 1);

rgb = cameraToRGB * [r'; g'; b'];

bayer_rojo_completo = reshape(rgb(1,:), filas, columnas);
bayer_rojo_completo = reshape(rgb(2,:), filas, columnas);
bayer_azul_completo = reshape(rgb(3,:), filas, columnas);

gamma = 1/2.222;
imagen3D = cat(3, bayer_rojo_completo, bayer_rojo_completo, bayer_azul_completo);

imagen_rojo_corregido = imadjust(bayer_rojo_completo, [], [], gamma);
imagen_verde_corregido = imadjust(bayer_verde1_completo, [], [], gamma);
imagen_azul_corregido = imadjust(bayer_azul_completo, [], [], gamma);

%imagen3D = cat(3, imagen_rojo_corregido, imagen_verde_corregido, imagen_azul_corregido);
