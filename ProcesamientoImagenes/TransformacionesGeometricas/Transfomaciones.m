clear all;
imgFlowers = imread("flowers.jpg");
imgCube = imread("cube.jpg");

tx = 12;
ty = 6;
imgTraslationFlowers = traslacion(imgFlowers, tx, ty);

tx = 120;
ty = -220;
imgTraslationCube = traslacion(imgCube, tx, ty);

ex = 0.222;
ey = 0.222;
imgEscaladoFlowers = escalado(imgFlowers, ex, ey);

ex = 2;
ey = 3;
imgEscaladoCube = escalado(imgCube, ex, ey);

a = 0.4;
imgSesgadoFlowers = sesgado(imgFlowers, a);

a = 0.1;
imgSesgadoCube = sesgado(imgCube, a);


a = 0.2;
imgRotacionFlower = rotacion(imgFlowers, a);
a = 0.2;
imgRotacionCube = rotacion(imgCube, a);


figure(1)
    subplot(1,4,[1,2]);
    imshow(imgFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgCube,[]);
    title("Original");

figure(2)
    subplot(1,4,[1,2]);
    imshow(imgTraslationFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgTraslationCube,[]);
    title("Traslacion");

figure(3)
    subplot(1,4,[1,2]);
    imshow(imgEscaladoFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgEscaladoCube,[]);
    title("Escalado");

figure(4)
    subplot(1,4,[1,2]);
    imshow(imgSesgadoFlowers,[]);
    subplot(1,4,[3,4]);
    imshow(imgSesgadoCube,[]);
    title("Sesgado");

figure(5)
    subplot(1,4,[1,2]);
    imshow(imgRotacionFlower,[]);
    subplot(1,4,[3,4]);
    imshow(imgRotacionCube,[]);
    title("Rotacion");


function imgTranslation = traslacion(img, tx, ty)
    for y = 1:size(img,1)
        for x=1:size(img,2)
            xNew = x + tx;
            yNew = y + ty;
            if xNew >= 1 && xNew <= size(img, 2) && yNew >= 1 && yNew <= size(img, 1)
                %imgTranslation(xNew,yNew,:) = img(x,y,:);
                imgTranslation(xNew,yNew,:) = img(x,y,:);
            end 
        end
    end
end

function imgEscalado = escalado(img, ex, ey)
    for y = 1:size(img,1)
        for x=1:size(img,2)
            xNew = uint16(x * ex);
            yNew = uint16(y * ey);
            if xNew >= 1 && xNew <= size(img, 2) && yNew >= 1 && yNew <= size(img, 1)
                imgEscalado(xNew,yNew,:) = img(x,y,:);
            end 
        end
    end
end

function imgSesgado = sesgado(img, a)
    for y = 1:size(img,1)
        for x=1:size(img,2)
            xNew = uint16(x + (a*y));
            yNew = y;
            if xNew >= 1 && xNew <= size(img, 2) && yNew >= 1 && yNew <= size(img, 1)
                imgSesgado(xNew,yNew,:) = img(x,y,:);
            end 
        end
    end
end

function imgRotacion = rotacion(img,a)

  % Calcular el centro de la imagen
  centro_x = size(img, 2) / 2;
  centro_y = size(img, 1) / 2;

  for y = 1:size(img,1)
        for x=1:size(img,2)
            x_adjusted = x - centro_x;
            y_adjusted = y - centro_y;
            xNew = uint16(x_adjusted * cos(a) - y_adjusted * sin(a)) + centro_y ;
            yNew = uint16(x_adjusted * sin(a) + y_adjusted * cos(a)) + centro_y;
            if xNew >= 1 && xNew <= size(img, 2) && yNew >= 1 && yNew <= size(img, 1)
                imgRotacion(xNew,yNew,:) = img(x,y,:);
            end 
        end
  end
end
