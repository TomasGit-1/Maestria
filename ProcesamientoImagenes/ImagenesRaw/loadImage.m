fileName = 'paisaje.ARW';
bayerImage = rawread(fileName);
bayerInfo = rawinfo(fileName)
cameraToRGB = bayerInfo.ColorInfo.CameraTosRGB
%Definimos las matriz a utilizar
bayer_rggb = uint16([800,800;800,800]);