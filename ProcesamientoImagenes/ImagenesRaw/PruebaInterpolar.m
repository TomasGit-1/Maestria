vec3 = [0.1874,0,0.18415,0.1809,0,0.18415;];
valores =[ 0.5209         ,0    ,0.5451         ,0    ,0.5183         ,0    ,0.4299         ,0    ,0.3907    ,0.3907];
valores = [ 1.1070    ,1.1070         ,0    ,1.2964         ,0    ,1.8880];
valores = [ 1.1070    ,1.1070         ,0    ,1.2964         ,0    ,1.8880]
%valores = [ 1.4449  ,  1.4449     ,    0   , 1.7916         ,0    ,1.1171]

disp(valores);
vec6 = interpolasr(valores);
disp(vec6);

%vec4 = interpolasr(vec3);
%vec5 = interpolar(vec3);
%disp(vec5);
%disp(vec6);



function vec = interpolar2(vec)
    %%Igual a la formual directa
    % Encontrar los índices de los valores que no son cero
    indices_no_ceros = find(vec ~= 0);
    valores_no_ceros = vec(indices_no_ceros);
    
    % Encontrar los índices de los valores que son cero
    indices_ceros = find(vec == 0);
    
    % Calcular la interpolación lineal usando interp1 con los mismos puntos de interpolación
    valores_interp = interp1(indices_no_ceros, valores_no_ceros, indices_ceros, 'linear');
    
    % Asignar los valores interpolados al vector original
    vec(indices_ceros) = valores_interp;
end

function valores_interp = interpolar(valores)
    %Mejor precision
    indices_ceros = find(valores == 0);
    indices_no_ceros = find(valores ~= 0);
    valores_interp = valores;
    valores_interp(indices_ceros) = interp1(indices_no_ceros, valores(indices_no_ceros), find(indices_ceros), 'linear');
end

function vec = interpolasr(vec)
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
end 