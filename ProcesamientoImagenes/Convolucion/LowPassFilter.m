function kernel = LowPassFilter()
    [x , y] = meshgrid([ -2 : 0.9 : 2]);
    fx = (1 + 2 * cos(x) + 2 * cos(2*x));
    fy = 1 + 2 * cos(y) + 2 * cos(2*y);
    f = fx .* fy;
    kernel = f/sum(sum(f));
    %kernel = f./25;
end 