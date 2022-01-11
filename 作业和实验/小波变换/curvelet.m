%% curvelet
clear;
clc;
close all;
% 保存图像路径
save_path = 'C:\Users\admin\Desktop\nextcloud\HIT\课程\小波变换\课程实验\报告\curvelet\';
% 系数保留量
perc = [0.05, 0.1, 0.2];
% 图像路径
ipath = ["standard_lena.bmp", "baboon.BMP", "BARB.BMP"];
for i = ipath
    my_curvelet(i, perc, save_path);
end
close all;

function my_curvelet(ipath, per, save_path)
    %% 读入图像
    X = imread(ipath);
    % 显示原始图像
    figure('NumberTitle', 'off', 'Name', strcat(ipath, '原始输入图像'));
    subplot(121);   imshow(X);  title(strcat(ipath, '原始输入图像'));
    %% curvelet变换
    C = fdct_usfft(double(X), 0);
    cfs =[];
    for s=1:length(C)
      for w=1:length(C{s})
        cfs = [cfs; abs(C{s}{w}(:))];
      end
    end
    % 显示原始图像系数
    cimg = fdct_usfft_dispcoef(C);
    subplot(122);   colormap gray;  imagesc(abs(cimg)); axis('image'); title(strcat(ipath, '原始图像分解系数（对数表示）'));
    % 保存图像
    saveas(gcf, strcat(save_path, ipath, '原始图像及其分解系数（对数表示）.png'));
    %% 截取系数
    cfs = sort(cfs);
    cfs = cfs(end:-1:1);
    copyC = C;
    for perc = per
        C = copyC;
        nb = round(perc * length(cfs));
        cutoff = cfs(nb);
        for s = 1:length(C)
          for w = 1:length(C{s})
            C{s}{w} = C{s}{w} .* (abs(C{s}{w}) > cutoff);
          end
        end
       %% 重建
        recX = uint8(real(ifdct_usfft(C, 0)));
        % 显示重建图像
        figure('NumberTitle', 'off', 'Name', strcat(ipath, '保留高频子带前', num2str(perc * 100), '%系数重建图像'));
        subplot(121);   imshow(recX);  title(strcat(ipath, '保留高频子带内', num2str(perc * 100), '%（由大到小）系数重建结果'));
        % 显示处理后的系数
        cimg = fdct_usfft_dispcoef(C);
        subplot(122);   colormap gray;  imagesc(abs(cimg)); axis('image'); title(strcat(ipath, '保留高频子带前', num2str(perc * 100), '%系数'));
        % 保存图像
        saveas(gcf, strcat(save_path, ipath, '保留高频子带前', num2str(perc * 100), '%系数重建图像及其分解系数（对数表示）.png'));
       %% 图像熵和信噪比
        % 图像熵
        disp(strcat(ipath, '保留高频子带前', num2str(perc * 100), '%系数重建图像的图像熵为', num2str(image_entropy(recX))));
        % 信噪比
        disp(strcat(ipath, '保留高频子带前', num2str(perc * 100), '%系数重构图像的信噪比为', num2str(compute_snr(X, recX))));
    end
end
