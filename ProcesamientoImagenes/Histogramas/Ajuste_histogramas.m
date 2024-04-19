img = imread("Imagenes/lenaColor.png");
imgGray = rgb2gray(img);
[rows, cols] = size(imgGray);
h = histograma(imgGray);
H = HistogramA(h);

imgE = HEqualization(H, rows, cols , 255 ,imgGray);
hE = histograma(imgE);
HE = HistogramA(hE);

ref = exp(0:pi/255:pi);
ref = sin(0:pi/255:pi);
ref = cos(0:pi/255:pi);
ref = abs(ref)
%ref = log(1:256);
%x = 0:255;
%ref = x.^2;

imgS= HSpecification(H,ref,imgGray);
hS = histograma(imgS);
HS = HistogramA(hS);

LR = generateL(256);
imgSpiece = HPieceWise(H,LR,imgGray);
hSpiece = histograma(imgSpiece);
HSpiece = HistogramA(hSpiece);


imgR = imread("Imagenes/frutos_rojos.png");
imgGrayR = rgb2gray(imgR);
hR = histograma(imgGrayR);
HR = HistogramA(hR);
imgMacth= macth(H,HR,imgGray);
hMacth = histograma(imgMacth);
HMatch = HistogramA(hMacth);


figure
subplot(3,3,1); imshow(imgGray); title('Imagen Original');
subplot(3,3,2); bar(1:256, h);  title('Histograma h');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,3); bar(1:256, H);  title('Histograma H');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');

subplot(3,3,4); imshow(imgE); title('Imagen Equalization');
subplot(3,3,5); bar(1:256, hE);  title('Histograma hE');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,6); bar(1:256, HE);  title('Histograma HE');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');

subplot(3,3,7); imshow(imgE); title('Imagen Specification');
subplot(3,3,8); bar(1:256, hS);  title('Histograma hS');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,9); bar(1:256, HS);  title('Histograma HS');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');

figure 
subplot(3,3,1); imshow(imgSpiece); title('Imagen PieceWise');
subplot(3,3,2); bar(1:256, hSpiece);  title('Histograma hS L');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,3); bar(1:256, HSpiece);  title('Histograma HS L');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');

subplot(3,3,4); imshow(imgGrayR); title('Imagen Referencia');
subplot(3,3,5); bar(1:256, hR);  title('Histograma hM');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,6); bar(1:256, HR);  title('Histograma HM');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');

subplot(3,3,7); imshow(imgMacth); title('Imagen Match');
subplot(3,3,8); bar(1:256, hMacth);  title('Histograma hM ');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');
subplot(3,3,9); bar(1:256, HMatch);  title('Histograma HM ');xlabel('Intensidad de Píxeles'); ylabel('Frecuencia');


function img2 = macth(HA, HR , img1)
    % hA: histograma de la imagen objetivo
    % hR: histograma de referencia (del mismo tamaño que hA)
    
    K = numel(HA);
    PA = HA;
    PR = HR;
    fhs = zeros(K, 1);
    for a = 1:K
        j = K;
        while (j >= 1) && (PA(a) <= PR(j))
            fhs(a) = j;
            j = j - 1;
        end
    end
    img2 = uint8(zeros(size(img1)));
    for r = 1:size(img1,1)
        for c = 1:size(img1 , 2)
            img2(r,c) = uint8(fhs(img1(r, c)));
        end
    end

    
end


function  LA = generateL(N)
%x_change = [0,10, 20 , 30, 40, 50];
    x_change = [1,2,3,4,5,6];
    y_values = [0.7,0.8, 0.84,0.88,0.9, 1]; 
    LA = [x_change; y_values]';    
end

function img2 = HPieceWise(hA, LR , img1)
    K = numel(hA);
    PA = hA / hA(end);
    fhs = zeros(1, K);
   
    for a = 0:(K-1)
        b = PA(a + 1);

        if b <= LR(1,2)
            a_prime = 0;
        elseif b >= 1
            a_prime = 255;
        else
            %eMPIEZA DESDE 1
            n = numel(LR(:, 2)) - 1;
            while n >= 0 && LR(n + 1, 2) > b
                n = n - 1;
            end
            a_prime = LR(n+1, 1) + (b - LR(n+1, 2)) * (LR(n + 2, 1) - LR(n+1, 1)) / (LR(n + 2, 2) - LR(n+1, 2));
        end
        disp(a);
        fhs(a + 1) = uint8(a_prime * 255);
    end
    img2 = uint8(zeros(size(img1)));

    for r = 1:size(img1,1)
        for c = 1:size(img1 , 2)
            img2(r,c) = uint8(fhs(img1(r, c)));
        end
    end
end



function img2 = HSpecification(H,ref ,img1)
    refC = zeros(256,1);
    for bin=2:256
        refC(bin) = refC(bin-1) + ref(bin);
    end
    %Normalizamos datos en un rando de 0,1
    refC = refC / refC(end);
    H = H / H(end);
    tabla = zeros(256,1);

    for intensidad=0:255
        %Generamos las busquedas de los indices a los que le pertenece la
        %intensisdad
        res = find(H(intensidad + 1 ) >= refC);
        tabla(intensidad + 1) = res(end) -1;
    end
    
    img2 = uint8(zeros(size(img1)));
    
    for r = 1:size(img1,1)
        for c = 1:size(img1 , 2)
            img2(r,c) = uint8(tabla(img1(r, c) + 1));
        end
    end
end

function imgE= HEqualization(H , M , N , k , img)
    factor = k/ (M * N);
    LUT = zeros(256,1);
    for intensidad=1:256
        LUT(intensidad) = floor( H(intensidad) * factor);
    end
    imgE = uint8(zeros(size(img)));
    for r =1: size(img,1)
        for c =1: size(img , 2)
            imgE(r,c) = uint8(LUT(img(r,c)));
        end
    end
end 

function h = histograma(imgGray)
    h = zeros(256, 1);
    for row = 1:size(imgGray, 1)
        for col = 1:size(imgGray, 2)
            intensidad_pixel = imgGray(row, col);
            h(intensidad_pixel + 1) = h(intensidad_pixel + 1) + 1;
        end
    end
end

function H = HistogramA(h)
    H = zeros(256, 1);
    H(1) = h(1);
    for j=2:size(h)
        H(j) = H(j-1) + h(j);
    end
end