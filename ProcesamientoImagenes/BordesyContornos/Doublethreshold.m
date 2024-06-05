function res = Doublethreshold(E2)
    [M,N] = size(E2);
    lowThreholdRatio = 0.05;
    highThresholdratio = 0.09;
    
    highThreshold = max(max(E2)) * highThresholdratio;
    lowThreshold = highThreshold * lowThreholdRatio;
    
    res = zeros(M,N);
    weak = 0;
    strong = 255;
    [strong_r,strong_c] = find(E2 >= highThreshold);
    [zeros_r, zeros_c] = find(E2 < lowThreshold);
    [weak_r, weak_c] = find(E2 <= highThreshold & E2 >= lowThreholdRatio);
    
    for r=1:size(strong_r,1)
        res(strong_r(r),strong_c(r)) = strong;
    end
    
    for r=1:size(weak_r,1)
        res(weak_r(r),weak_c(r)) = weak;
    end
end