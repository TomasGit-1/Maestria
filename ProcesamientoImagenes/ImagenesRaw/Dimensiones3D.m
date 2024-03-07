% Obtener las dimensiones de las matrices
[filas, columnas] = size(bayer_rojo_completo);

%{
r = reshape(bayer_rojo_completo, [], 1);
g = reshape(bayer_verde1_completo, [], 1);
b = reshape(bayer_azul_completo, [], 1);

rgb = cameraToRGB * [r'; g'; b'];

bayer_rojo_completo3d = reshape(rgb(1,:), filas, columnas);
bayer_verde1_completo3d = reshape(rgb(2,:), filas, columnas);
bayer_azul_completo3d = reshape(rgb(3,:), filas, columnas);

gamma = 1/2.222;
%imagen3D = cat(3, bayer_rojo_completo, bayer_verde1_completo, bayer_azul_completo);

imagen_rojo_corregido = imadjust(bayer_rojo_completo3d, [], [], gamma);
imagen_verde_corregido = imadjust(bayer_verde1_completo3d, [], [], gamma);
imagen_azul_corregido = imadjust(bayer_azul_completo3d, [], [], gamma);

imagen3D = cat(3, imagen_rojo_corregido, imagen_verde_corregido, imagen_azul_corregido);
%}


ColorR = zeros(filas, columnas);
ColorV = zeros(filas, columnas);
ColorA = zeros(filas, columnas);

for i = 1:filas
    for j = 1:columnas
        r = bayer_rojo_completo(i,j);
        v = bayer_verde1_completo(i, j);
        b = bayer_azul_completo(i, j);
        rgb = [r; v;b];
        rgb = cameraToRGB * rgb;
        ColorR(i,j) = rgb(1);
        ColorV(i,j) = rgb(2);
        ColorA(i,j) = rgb(3);
    end
end

%factor_atenuacion = 0.6;
%canal_verde_atenuado = ColorV * factor_atenuacion;

gamma = 1/2.222;
%gamma = 0.5;
Tempimagen3D = cat(3, bayer_rojo_completo, bayer_verde1_completo, bayer_azul_completo);

imagen_rojo_corregido = imadjust(ColorR, [], [], gamma);
imagen_verde_corregido = imadjust(ColorV, [], [], gamma);
imagen_azul_corregido = imadjust(ColorA, [], [], gamma);


imagen3D = cat(3, imagen_rojo_corregido, imagen_verde_corregido, imagen_azul_corregido);

%{
max_valor = max(max(max(imagen3D)));
min_valor = min(min(min(imagen3D)));
imagen3D_normalizada = (imagen3D - min_valor) / (max_valor - min_valor);
%}