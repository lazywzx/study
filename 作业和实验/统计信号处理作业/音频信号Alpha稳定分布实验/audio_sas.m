%% 实验一
% 六个场景的音频文件，画出时域波形和alpha稳定分布图，共六个
clear;
clc;
%% 循环调用函数，画出六组图
audios = string({'./教室.m4a', './男声.m4a', './女声.m4a', './寝室.m4a', './食堂.m4a', './音乐.m4a'});
for i = 1:6
    plot_sas(audios(i), i);
end

function plot_sas(path, fig_num)
%% 读入音频文件
[x, Fs] = audioread(path);
N = length(x);  % 信号序列长度
t = (0: N - 1) / Fs;    % 真实时刻序列

%% 画出时域波形
figure(fig_num);
subplot(211);
plot(t, x);
title(string(path) + ' 时域波形');
xlabel('时间'); ylabel('幅值');
hold on;
% alpha曲线图
subplot(212);
plot(t, x * 0, 'r');
title(string(path) + ' alpha分布');
xlabel('时间'); ylabel('alpha');
hold on;

%% 取对数阶
M = 80000;   % 滑动窗宽度
distance = 4000; % 滑动间距
z = abs(x);
[p, ~] = find(z == 0);  % 防止除0错误
z(p) = 1e-10;
z = log(z);

%% 主要算法与可视化
distance = 4000; % 滑动间距
alpha = zeros(length(z) - M, 1);
for k = M + 1: distance: N
    postion = k-M: k-1; % 滑动窗位置
    %% 画出滑动窗波形叠加图
    subplot(211);
    if exist('h', 'var')
        delete(h);  % 删除上次循环画出的图
    end
    h = plot(postion / Fs, x(postion), 'r');    % 画出本次循环的图

    %% 求解alpha
    postion = k-M: k-1; % 滑动窗位置
    sigma2 = std(z(postion))^2;
    alphatmp = (1 / (sigma2 * 6 / pi^2 - 0.5))^0.5;
    if isreal(alphatmp)
        alpha(k) = alphatmp;
    end

    %% 画出alpha
    subplot(212);
    plot(postion / Fs, alpha(postion), 'r.');
    % 延时以显示
    pause(0.01);

end
end
