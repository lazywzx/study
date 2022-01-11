%% 图像熵计算函数
function [H_x] = image_entropy(img)
    [C, L] = size(img); % 求图像的规格
    Img_size =C * L;    % 图像像素点的总个数
    G = 256;    % 图像的灰度级
    H_x = 0;
    nk = zeros(G, 1);   % 产生一个G行1列的全零矩阵
    for i = 1:C
        for j = 1:L
            Img_level = img(i, j) + 1;    % 获取图像的灰度级
            nk(Img_level) = nk(Img_level) + 1;  % 统计每个灰度级像素的点数
        end
    end
    for k = 1:G
        Ps(k) = nk(k) / Img_size;   % 计算每一个像素点的概率
        if Ps(k) ~= 0
            H_x = - Ps(k) * log2(Ps(k)) + H_x;  % 求熵值的公式
        end
    end
end
