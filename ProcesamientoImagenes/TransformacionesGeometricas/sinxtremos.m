fila = [0 0 0 1 2 0 0 0 3 4 0 0 0 0];
fila_interpolada = interpolacionSinExtremos(fila);
disp(fila_interpolada);


function fila_interpolada = interpolacionSinExtremos(fila)
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
end