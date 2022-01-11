%% wavelet
clear;
clc;
close all;
% 保存图像路径
save_path = 'C:\Users\admin\Desktop\nextcloud\HIT\课程\小波变换\课程实验\报告\wavelet\';
% 系数保留量
perc = [0.05, 0.1, 0.2];
% 图像路径
ipath = ["standard_lena.bmp", "baboon.BMP", "BARB.BMP"];
for i = ipath
    my_wavelet(i, perc, save_path);
end
close all;

function my_wavelet(ipath, per, save_path)
    %% 读取图像
    X = imread(ipath);
    % 显示原始图像
    figure('NumberTitle', 'off', 'Name', strcat(ipath, '原始输入图像'));
    imshow(X);  title(strcat(ipath, '原始输入图像'));
    % 保存图像
    imwrite(X, strcat(save_path, ipath, '原始输入图像.png'));
    %% wavelet变换
    [c,s] = wavedec2(double(X), 2, 'sym5');
    % 提取各子带系数
    % 第一层系数
    H1 = detcoef2('h', c, s, 1);
    V1 = detcoef2('v', c, s, 1);
    D1 = detcoef2('d', c, s, 1);
    % 第二层系数
    A2 = appcoef2(c, s, 'sym5', 2);
    H2 = detcoef2('h', c, s, 2);
    V2 = detcoef2('v', c, s, 2);
    D2 = detcoef2('d', c, s, 2);
    % 显示分解结果
    figure('NumberTitle', 'off', 'Name', strcat(ipath, '二层分解结果'));
    subplot(4, 4, 1);   imshow(A2, []); title('二层低频');
    subplot(4, 4, 2);   imshow(H2, []); title('二层水平高频');
    subplot(4, 4, 5);   imshow(V2, []); title('二层垂直高频');
    subplot(4, 4, 6);   imshow(D2, []); title('二层对角高频');
    subplot(4, 4, [3, 4, 7, 8]);   imshow(H1, []);  title('一层水平高频');
    subplot(4, 4, [9, 10, 13, 14]);   imshow(V1, []);   title('一层垂直高频');
    subplot(4, 4, [11, 12, 15, 16]);   imshow(D1, []);  title('一层对角高频');
    % 保存图像
    saveas(gcf, strcat(save_path, ipath, '二层分解结果.png'));
    %% 保持低频子带不变，截取高频子带不同比例系数
    for perc = per
        % 第一层高频子带
        cH1 = select_coefficient(perc, H1);
        cV1 = select_coefficient(perc, V1);
        cD1 = select_coefficient(perc, D1);
        % 第二层高频子带
        cH2 = select_coefficient(perc, H2);
        cV2 = select_coefficient(perc, V2);
        cD2 = select_coefficient(perc, D2);
        % 显示处理后的子带
        figure('NumberTitle', 'off', 'Name', strcat(ipath, '各高频子带处理后的结果(保留前', num2str(perc * 100), '%)的系数'));
        subplot(4, 4, 1);   imshow(A2, []); title('二层低频');
        subplot(4, 4, 2);   imshow(cH2, []);    title('二层水平高频');
        subplot(4, 4, 5);   imshow(cV2, []);    title('二层垂直高频');
        subplot(4, 4, 6);   imshow(cD2, []);    title('二层对角高频');
        subplot(4, 4, [3, 4, 7, 8]);   imshow(cH1, []); title('一层水平高频');
        subplot(4, 4, [9, 10, 13, 14]);   imshow(cV1, []);  title('一层垂直高频');
        subplot(4, 4, [11, 12, 15, 16]);   imshow(cD1, []); title('一层对角高频');
        % 保存图像
        saveas(gcf, strcat(save_path, ipath, '各高频子带处理后的结果(保留前', num2str(perc * 100), '%)的系数.png'));
        %% 用处理后的子带重建
        rec_set = [A2(:)', cH2(:)', cV2(:)', cD2(:)', cH1(:)', cV1(:)', cD1(:)'];
        recX = uint8(waverec2(rec_set, s, 'sym5'));
        % 显示重建结果
        figure('NumberTitle', 'off', 'Name', strcat(ipath, '保留高频子带前', num2str(perc * 100), '%系数重建图像'));
        imshow(recX);    title(strcat(ipath, '保留高频子带内', num2str(perc * 100), '%（由大到小）系数重建结果'));
        % 保存图像
        imwrite(recX, strcat(save_path, ipath, '保留高频子带前', num2str(perc * 100), '%系数重建图像.png'));
        %% 图像熵和信噪比
        % 图像熵
        disp(strcat(ipath, '保留高频子带前', num2str(perc * 100), '%系数重建图像的图像熵为', num2str(image_entropy(recX))));
        % 信噪比
        disp(strcat(ipath, '保留高频子带前', num2str(perc * 100), '%系数重建图像的信噪比为', num2str(compute_snr(X, recX))));
    end
end
