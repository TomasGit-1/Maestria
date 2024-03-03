%Validamos primera y ultima
if all(bayer_rojo_completo(end,:) == 0)
   bayer_rojo_completo(end, :) = bayer_rojo_completo(end - 1, :);
end
if all(bayer_rojo_completo(:, end) == 0)
    bayer_rojo_completo(:, end) = bayer_rojo_completo(:, end - 1);
end

%Aplicando interpoleacion Lineal a los borde
filas = bayer_rojo_completo([1, end], :);
columnas = bayer_rojo_completo(:, [1, end]);
filas_no_cero = filas(any(filas ~= 0, 2), :);

for i = 1:size(filas, 1)
    x = filas(i,:);
    indices_ceros = find(x == 0);
    indices_no_ceros = find(x ~= 0);
    x_interp = interp1(indices_no_ceros, x(indices_no_ceros), indices_ceros, 'linear');
    x_interp(isnan(x_interp)) = 0;
    x(indices_ceros) = x_interp;
    if i == 2
        bayer_rojo_completo(end, :) = x;
    else
        bayer_rojo_completo(i, :) = x;
    end
end

for i = 1:size(columnas, 2)
    x = columnas(:,i);
    indices_ceros = find(x == 0);
    indices_no_ceros = find(x ~= 0);
    x_interp = interp1(indices_no_ceros, x(indices_no_ceros), indices_ceros, 'linear');
    x_interp(isnan(x_interp)) = 0;
    x(indices_ceros) = x_interp;
    if i == 2
        bayer_rojo_completo(:, end) = x;
    else
        bayer_rojo_completo(:,i) = x; 
    end
end



