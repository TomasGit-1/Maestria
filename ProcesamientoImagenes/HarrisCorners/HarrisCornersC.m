function GoodCorners = HarrisCornersC(imgGray)
    %PreFilter
    Hpx = [2 4 2]/9;
    Hpy = [2; 5; 2]/9;
    Hp = Hpx .* Hpy;

    I_ = uint8(conv2(imgGray, Hp, 'same'));
    
    %Horizontal and vertical  derivate
    Hdx = [-0.453014 0 0.453014;];
    Hdy = [-0.453014; 0; 0.453014];
    Ix = conv2(double(I_), Hdx, 'same');
    Ix = abs(Ix);
    Iy = conv2(double(I_), Hdy, 'same');
    Iy = abs(Iy);
    
    %Compute the local structure matrix M(u, v):
    A = Ix.^2;
    B = Iy.^2;
    C = Ix .* Iy;
    
    %BlurFilter
    Hbx = [1 6 15 20 15 6 1];
    Hby = [1; 6; 15; 20; 15; 6; 1];
    Hb = Hbx .* Hby;

    A_ = conv2(double(A), Hb, 'same');
    B_ = conv2(double(B), Hb, 'same');
    C_ = conv2(double(C), Hb, 'same');
    
    
    %Compute the corner response function
    alpha = 0.05;
    th = 100000;
    dmin = 200 ;

    Q = (A_ .* B_ - C_.^2) - alpha .* (A_ + B_).^2;
    Q(Q < 0) = 0;
    %Q = im2uint16(Q);
    %max_value = max(max(Q));
    %Q = Q * (255 / max_value);
    
    
    Q = padarray(Q, [1, 1], 0);
    [M,N] = size(Q);
    Corners = [];
    for u = 2:M-1
        for v = 2:N-1
            if Q(u,v) > th && IsLocalMax(Q, u , v)
                newCorner = [v,u, Q(u, v)];
                Corners = [Corners; newCorner];
            end 
        end
    end
    Corners = sortrows(Corners, -3);
    GoodCorners = uint16(CLEANUPNEIGHBORS(Corners,dmin));
end