    %{
    N = 256;
    q_values = linspace(0, 1, N)';    
    %q_values = exp(linspace(0, pi, N))';
    a_values = (1:N)';
    LA = [a_values, q_values];    
    qpuntos = 10;
    q_indices = round(linspace(100, 200, qpuntos));
    LA(~ismember(1:N, q_indices), 2) = 0; 
    %}