fileName = 'paisaje.ARW';
bayerImage = rawread(fileName);
bayerInfo = rawinfo(fileName);
cameraToRGB = bayerInfo.ColorInfo.CameraTosRGB;
%Definimos las matriz a utilizar
bayer_rggb = uint16([800,800;800,800]);
balanceB = [2.964,1; 1, 1.832];
%subBayer = bayerImage(500:1800, 500:2000);
subBayer = bayerImage(1000:1006, 1000:1006);

bayerNomalizado = normalizate_bayer(subBayer,bayer_rggb);

function bayerNormalizate = normalizate_bayer(subBayer,bayer_rggbT)
    funcion_resta = @(block_struct) block_struct.data - bayer_rggbT;
    resultado = blockproc(subBayer, [2, 2], funcion_resta);
    max_valor = max(subBayer, [], 'all');
    bayerNormalizate = double(subBayer) ./ double(max_valor);
end