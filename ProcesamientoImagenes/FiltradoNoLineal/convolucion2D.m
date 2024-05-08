function imgConvolucionada = convolucion2D(img,nneighbors,kernel)
    imgResize = padarray(img, [nneighbors, nneighbors], 0);
    imgConvolucionada = zeros(size(img));
    [row, col ] = size(imgResize);
    for r=nneighbors+1:row-nneighbors
        for c=nneighbors+1:col-nneighbors
            tempConvo = double(imgResize(r-nneighbors:r+nneighbors,c-nneighbors:c+nneighbors)) .* kernel;
            imgConvolucionada(r-nneighbors,c-nneighbors) = sum(tempConvo(:)) ;
        end
    end
end


