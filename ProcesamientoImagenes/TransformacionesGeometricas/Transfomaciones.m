clear all;
img = imread("flowers.jpg");

tx = 12;
ty = 6;
imgTraslation = traslacion(img, tx, ty);

ex = 1.2;
ey = 1.2;
imgEscalado = escalado(img, ex, ey);

a = 0.1;
imgSesgado = sesgado(img, a);


a = 1;
imgRotacion = rotacion(img, a);


figure(1)
    subplot(1,4,[1,2]);
    imshow(img,[]);
    subplot(1,4,[3,4])
    imshow(imgTraslation,[]);
    title("Traslacion");
   
figure(2)
    subplot(1,4,[1,2]);
    imshow(img,[]);
    subplot(1,4,[3,4])
    imshow(imgEscalado,[]);
    title("Escalado");


figure(3)
    subplot(1,4,[1,2]);
    imshow(img,[]);
    subplot(1,4,[3,4])
    imshow(imgSesgado,[]);
    title("Sesgado");

figure(4)
    subplot(1,4,[1,2]);
    imshow(img,[]);
    subplot(1,4,[3,4])
    imshow(imgRotacion,[]);
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
  for y = 1:size(img,1)
        for x=1:size(img,2)
            xNew = uint16(x * cos(a) - y * sin(a));
            yNew = uint16(x * sin(a) + y * cos(a));
            if xNew >= 1 && xNew <= size(img, 2) && yNew >= 1 && yNew <= size(img, 1)
                imgRotacion(xNew,yNew,:) = img(x,y,:);
            end 
        end
  end
end
