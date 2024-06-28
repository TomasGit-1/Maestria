
function imgNoFilter = ATMFilter(img , d)
    [width, height] = size(img);
    imgNoFilter = zeros(width-1, height-1);
    d = d/2;
    for row=2:width-1
        for col=2:height-1
            mask = [img(row-1,col-1) img(row-1,col) img(row-1,col+1); 
                    img(row,col-1)   img(row,col)   img(row,col+1); 
                    img(row+1,col-1)  img(row+1,col) img(row+1,col+1)];   
            flattening = sort(mask(:));
            newFlat = flattening(d+1: 9-d);
            newPixel = sum(newFlat)/ size(newFlat,1);
            imgNoFilter(row,col) = newPixel;
        end
    end
end
