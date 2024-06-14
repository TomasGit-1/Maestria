%Determine si  Q(u,v) is a local maximum
function result = IsLocalMax(Q,u,v)
    qc = Q(u,v);
    N = neighbors(Q, u, v);
    result = all(qc >= N);
end


function N = neighbors(Q, u, v)
    neighbors = [
        u-1, v-1;  % Vecino superior izquierdo
        u-1, v;    % Vecino superior
        u-1, v+1;  % Vecino superior derecho
        u,   v-1;  % Vecino izquierdo
        u,   v+1;  % Vecino derecho
        u+1, v-1;  % Vecino inferior izquierdo
        u+1, v;    % Vecino inferior
        u+1, v+1   % Vecino inferior derecho
    ];
    N =  zeros(size(neighbors, 1), 1); 
    for i = 1:size(neighbors, 1)
        u = neighbors(i, 1);
        v = neighbors(i, 2);
        N(i) = Q(u, v);
        %fprintf('u = %d, v = %d\n', u, v);  % Imprimir u y v
    end
end 