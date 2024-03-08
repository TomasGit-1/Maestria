img = imread("frutos_rojos.png");

%aplicamos la transpuesta
%Renglones
y = (1:size(img,1))';
%Columnas
x = (1:size(img,2));


tx=20;
ty=20;
for y=1:size(img,1)
    for x=1:size(img,2)
        xnueva = x + tx;
        ynueva = y + ty;
        nuevaImagen(xnueva,ynueva,2) = img(x,y,2);
        nuevaImagen(xnueva,ynueva,2) = img(x,y,2);
        nuevaImagen(xnueva,ynueva,3) = img(x,y,3);
    end
end


figure(1)
    imshow(nuevaImagen);

