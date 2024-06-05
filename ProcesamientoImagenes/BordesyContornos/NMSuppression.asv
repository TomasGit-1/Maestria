function E2 =  NMSuppression(img,theta)    
    [M,N] = size(img);
    E1 = zeros(M, N);
    E2 = zeros(M, N);
    theta = -pi + (2 * pi) * rand(M, N);
    angle = theta * 180./pi;
    angle(angle<0) = angle(angle<0) + 180;
    for r=2:M-1
        for c=2:N-1
            q = 255;
            p = 255;
            %angle 0
            if (0<=angle(r,c) && angle(r,c)< 22.5) || (157.5 <= angle(r,c) && angle(r,c)<= 180)
                q = E1(r,c+1);
                p = E1(r,c-1);
            %angle 45
            elseif (22.5 <= angle(r,c) && angle(r,c)<67.5)
                q = E1(r+1, c-1);
                p = E1(r-1, c+1);
            %angle 90
            elseif (67.5 <= angle(r,c) && angle(r,c)<112.5)
                q = img(r+1, c-1);
                p = img(r-1, c+1);
            %angle 135
            elseif (112.5 <= angle(r,c) && angle(r,c)<157.5)
                q = img(r-1,c-1);
                p = img(r+1, c+1);
            end
            if (E1(r,c)>=q) && (E1(r,c) >= p)
                E2(r,c) = E1(r,c);
            else
                E2(r,c) = 0;
            end
        end
    end
end