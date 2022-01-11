%% contourlet
clear;
clc;
close all;
% 保存图像路径
save_path = 'C:\Users\admin\Desktop\nextcloud\HIT\课程\小波变换\课程实验\报告\contourlet\';
% 系数保留量
perc = [0.05, 0.1, 0.2];
% 图像路径
ipath = ["standard_lena.bmp", "baboon.BMP", "BARB.BMP"];
for i = ipath
    my_contourlet(i, perc, save_path);
end
close all;

function my_contourlet(ipath, per, save_path)
    %% 读取图像
    X = double(imread(ipath));
    % 显示原始图像
    figure('NumberTitle', 'off', 'Name', strcat(ipath, '原始输入图像'));
    subplot(121);   imshow(uint8(X));  title(strcat(ipath, '原始输入图像'));
    %% contourlet变换
    y = pdfbdec(X, '9-7', 'pkva', [0 2]);
    % 显示原始图像分解结果
    subplot(122);   showpdfb(y);    title(strcat(ipath, '原始图像分解结果'));
    % 保存图像
    saveas(gcf, strcat(save_path, ipath, '原始图像及分解结果.png'));
    %% 处理系数
    copyy = y;
    for perc = per
        y = copyy;
        for j = 1:3
            y{2}{j}=select_coefficient(perc, y{2}{j});
        end
        for j = 1:4
            y{3}{j} = select_coefficient(perc, y{3}{j});
        end
       %% 重建
        recX = uint8(pdfbrec(y, '9-7', 'pkva'));
        % 显示重建结果
        figure('NumberTitle', 'off', 'Name', strcat(ipath, '保留高频子带前', num2str(perc * 100), '%系数重建图像'));
        subplot(121);   imshow(recX);  title(strcat(ipath, '保留高频子带内', num2str(perc * 100), '%（由大到小）系数重建结果'));
        % 显示处理后的分解系数
        subplot(122);   showpdfb(y); title(strcat(ipath, '保留高频子带前', num2str(perc * 100), '%系数'));
        % 保存图像
        saveas(gcf, strcat(save_path, ipath, '保留高频子带前', num2str(perc * 100), '%系数重建图像及分解结果.png'));
       %% 图像熵和信噪比
        % 图像熵
        disp(strcat(ipath, '保留高频子带前', num2str(perc * 100), '%系数重建图像的图像熵为', num2str(image_entropy(recX))));
        % 信噪比
        disp(strcat(ipath, '保留高频子带前', num2str(perc * 100), '%系数重构图像的信噪比为', num2str(compute_snr(uint8(X), recX))));
    end
end
