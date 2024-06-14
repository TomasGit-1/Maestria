function GoodCorners = CLEANUPNEIGHBORS(Corners, dmin)
    % Inicializar la lista de buenas esquinas
    GoodCorners = [];
    
    % Mientras la lista de Corners no esté vacía
    while ~isempty(Corners)
        % Remover la primera esquina de Corners y añadirla a GoodCorners
        Ci = Corners(1, :);
        GoodCorners = [GoodCorners; Ci];
        
        % Eliminar la primera esquina de Corners
        Corners(1, :) = [];
        % Extraer el valor que representa la distancia (el último valor en este caso)
        dist_Ci = Ci(end);
        CjAll = Corners(:,end);
        distances = double(dist_Ci) - double(CjAll);  
        %distances = distances/max(distances);
        % Eliminar todas las esquinas que estén dentro de dmin de Ci
        Corners(distances < dmin, :) = [];
    end
end