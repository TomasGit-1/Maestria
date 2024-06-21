img = imread("tablero.png");

if ndims(img) == 2
    % La imagen ya está en escala de grises
    imgGray = img;
elseif ndims(img) == 3 && size(img, 3) == 3
    % Convertir la imagen a escala de grises si está en color
    imgGray = rgb2gray(img);
else
    % Manejar caso donde la imagen no tiene el formato esperado
    error('La imagen no está en el formato esperado.');
end


GoodCorners = HarrisCornersC(imgGray);

% Extraer las coordenadas x e y de los datos
x = GoodCorners(:, 1);
y = GoodCorners(:, 2);

% Mostrar la imagen en blanco y negro
figure;
    imshow(imgGray);
    hold on;
    scatter(x, y, 100, 'r', 'filled');    
    xlabel('Coordenada X');
    ylabel('Coordenada Y');
    title('Puntos sobre Imagen en Blanco y Negro');
    hold off;