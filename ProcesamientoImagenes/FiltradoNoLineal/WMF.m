function imgNoFilter = WMF(img , W)
    [width, height] = size(img);
    imgNoFilter = zeros(width-1, height-1);
    [m, n] = size(W);
    for row=2:width-1
        for col=2:height-1
            mask = [img(row-1,col-1) img(row-1,col) img(row-1,col+1); 
                    img(row,col-1)   img(row,col)   img(row,col+1); 
                    img(row+1,col-1)  img(row+1,col) img(row+1,col+1)];

            preFlattening = mask(:);
            posW = W(:);
            repeatF = repelem(preFlattening, posW);
            sortinfF = sort(repeatF);
            imgNoFilter(row,col) = median(sortinfF);
        end
    end
end
