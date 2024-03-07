disp("LLamado de funciones");
function [bayerImage,bayerInfo,cameraToRGB,bayer_rggb] = loadImageFunc(path)
    fileName = path;
    bayerImage = rawread(fileName);
    bayerInfo = rawinfo(fileName)
    cameraToRGB = bayerInfo.ColorInfo.CameraTosRGB
    %Definimos las matriz a utilizar
    bayer_rggb = uint16([800,800;800,800]);
end
