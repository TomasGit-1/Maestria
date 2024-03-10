% Vector dado
vec = [1,2,3,4,5,6;
       1,0,3,4,0,6;
       1,0,3,4,0,6;
       1,2,3,4,5,6];

%vec = [0.1874,0.18415,0.1809,0.18415;]
vec = [0.1874,0,0.18415,0.1809,0,0.18415;];
vec = [ 1.1070    ,1.1070         ,0    ,1.2964         ,0    ,1.8880]
vec = [ 1.4449  ,  1.4449     ,    0   , 1.7916         ,0    ,1.1171]

   

% Encuentra los índices de los valores 0
indices_ceros = find(vec == 0);
% Encuentra los índices de los valores que no son 0
indices_no_ceros = find(vec ~= 0);

% Para cada valor 0, calcula el valor interpolado
for i = 1:length(indices_ceros)
    zero_index = indices_ceros(i);
    %Arriba
    % Encuentra los dos índices más cercanos que no son 0
    x0 = max(indices_no_ceros(indices_no_ceros < zero_index));
    x1 = min(indices_no_ceros(indices_no_ceros > zero_index));
    % Calcula el valor interpolado usando la ecuación de la recta
    interpolated_value = ((vec(x1) - vec(x0)) / (x1 - x0)) * (zero_index - x0) + vec(x0);
    % Asigna el valor interpolado al valor 0 en el vector
    vec(zero_index) = interpolated_value;
end
disp(vec);
%{
% Para cada valor 0, calcula el valor interpolado
for i = 1:length(indices_ceros)
    zero_index = indices_ceros(i);
    
    % Encuentra los dos índices más cercanos que no son 0
    x0 = max(indices_no_ceros(indices_no_ceros < zero_index));
    x1 = min(indices_no_ceros(indices_no_ceros > zero_index));
    
    % Calcula el valor interpolado usando la ecuación de la recta
    interpolated_value = ((vec(x1) - vec(x0)) / (x1 - x0)) * (zero_index - x0) + vec(x0);
    
    % Asigna el valor interpolado al valor 0 en el vector
    vec(zero_index) = interpolated_value;
end
%}
%{

vec2 = [1,0,3,0,4];

for i = 1:length(indices_ceros)
    zero_index = indices_ceros(i);
    % Encuentra los dos índices más cercanos que no son cero
    x0 = max(indices_no_ceros(indices_no_ceros < zero_index));
    x1 = min(indices_no_ceros(indices_no_ceros > zero_index));
    
    % Calcula el valor interpolado usando interp1
    interpolated_value = interp1([x0, x1], [vec2(x0), vec2(x1)], zero_index);
    
    % Asigna el valor interpolado al valor cero en el vector
    vec2(zero_index) = interpolated_value;
end
%vec2 = [0.1874, 0, 0.1809,0.1874, 0, 0.1809];
%vec2(indices_ceros) = interp1(indices_no_ceros, vec2(indices_no_ceros), find(indices_ceros), 'spline');
disp(vec2);




% Vector dado
%vec3 = [1,0,3,0,4,1,0,3,0,4];
vec3 = [0.1874,0,0.18415,0.1809,0,0.18415;]

% Encuentra los índices de los valores no cero y los valores cero en el vector
indices_no_ceros = find(vec3 ~= 0);
indices_ceros = find(vec3 == 0);

% Encuentra los dos índices más cercanos que no son cero para cada valor cero
%Rx0_indices = max(bsxfun(@lt, indices_no_ceros', indices_ceros), [], 1);
%x1_indices = min(bsxfun(@gt, indices_no_ceros', indices_ceros), [], 1);

left_indices = sub2ind(size(vec3), rows, cols);
right_indices = sub2ind(size(vec3), rows-1, cols+1);

% Obtiene los valores correspondientes de x0 y x1
x0 = indices_no_ceros(x0_indices);
x1 = indices_no_ceros(x1_indices);

% Obtiene los valores de los puntos conocidos más cercanos
y0 = vec3(x0);
y1 = vec3(x1);

% Realiza la interpolación utilizando interp1
interpolated_values = interp1([x0; x1], [y0; y1], indices_ceros);

% Asigna los valores interpolados al vector original en las posiciones de los valores cero
vec3(indices_ceros) = interpolated_values;

% Rellena los valores NaN con una interpolación adicional
nan_indices = isnan(vec3);
vec3(nan_indices) = interp1(indices_no_ceros, vec3(indices_no_ceros), find(nan_indices), 'linear');

disp(vec3);

disp(vec3);

%}
