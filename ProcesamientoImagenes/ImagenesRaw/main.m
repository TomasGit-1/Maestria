
fileName = 'paisaje.ARW';
bayerImage= [];
bayerInfo= [];
cameraToRGB= [];
bayer_rggb= [];

bayerImage,bayerInfo,cameraToRGB,bayer_rggb = loadImageFunc(fileName);

function [bayerImage,bayerInfo,cameraToRGB,bayer_rggb] = loadImageFunc(fileName)
    fileName = path;
    bayerImage = rawread(fileName);
    bayerInfo = rawinfo(fileName);
    cameraToRGB = bayerInfo.ColorInfo.CameraTosRGB;
    %Definimos las matriz a utilizar
    bayer_rggb = uint16([800,800;800,800]);
end