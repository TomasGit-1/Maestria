function kernel = sharpeningFilter()
    [x , y] = meshgrid([ -5 : 0.8 : 5]);
    fx = 2 - (1/2 * cos(x));
    fy = 1/2 * cos(y);
    f = fx - fy;
    kernel = f / sum(sum(f));
end