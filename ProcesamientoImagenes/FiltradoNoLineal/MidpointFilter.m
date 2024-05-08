function imgNoFilter = MidpointFilter(img)
    [width, height] = size(img);
    imgNoFilter = zeros(width-1, height-1);
    for row=2:width-1
        for col=2:height-1
            mask = [img(row-1,col-1) img(row-1,col) img(row-1,col+1); 
                    img(row,col-1)   img(row,col)   img(row,col+1); 
                    img(row+1,col-1)  img(row+1,col) img(row+1,col+1)];   
            flattening = mask(:);            
            newPixel = max(flattening) + min(flattening);
            imgNoFilter(row,col) = newPixel / 2;
        end
    end
end
