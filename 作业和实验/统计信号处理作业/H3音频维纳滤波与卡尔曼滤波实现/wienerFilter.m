%% wiener filter for different d(n)
close all;
clear;
clc;
%% 信号产生，对原始信号进行采样
[x, Fs] = audioread('./melancholy.mp3');
x = x(2000001:2200000, 1)';   % 截取一段信号
audiowrite('./cut.wav', x, Fs); % 保存截取的音频

dB = 1;   % 预估信号强度范围
y = wiener_filter(x, dB, Fs);

% 保存滤波结果
audiowrite('./wiener_result.wav', y, Fs);

%% 维纳滤波
function [y] = wiener_filter(x, dB, Fs)
    SNR = 10; % 初始信噪比
    % 给输入信号加入信噪比为-3dB的高斯白噪声
    s=awgn(x,SNR,'measured'); 
    % 保存加噪结果
    audiowrite('./cut_noise.wav', s, Fs);
    M = length(x);  % 信号长度
    t = 0:M-1;
    
    % 期望信号
    d = [s(1),s(1:end-1),]; % d(n)=s(n-1)
    % 滤波器的阶数，向下取整
    N = floor(length(s)*0.1);

    % 自相关函数1*(2N-1)维度，返回一个延迟范围在[-N，N]的互相关函数序列,对称的
    Rxx=xcorr(s,N-1,'biased');
    % 变成矩阵 N*N维度
    mRxx = zeros(N, N) * nan;
    for i=1:N
        for j=1:N
            mRxx(i,j)=Rxx(N-i+j); % N*N维度
        end
    end

    % 产生维纳滤波中s方向上观测信号与期望信号d的互相关矩阵
    Rxd=xcorr(s,d,N-1,'biased'); % 互相关函数1*(2N-1)维度
    % 变成矩阵1*N维度
    mRxd = zeros(1, N) * nan;
    for i=1:N
        mRxd(i)=Rxd(N-1+i); % 1*N维度
    end

    % 由wiener-Hopf方程得到滤波器最优解, h是N*1维度
    h = mRxx\mRxd'; 

    % yy = filter(h,1,s);  % 用卷积或者直接用filter都可以
    y = conv(s,h); 
    y = y(1:M); % 滤波后的输出,长度为M+N-1，要截取前M个
    e = d - y;  % 输出减去期望等于滤波误差

    %%  画图
    % 滤波前后对比
    figure(1);
    subplot(311);
    plot(t, x);
    title('原始信号波形');
    xlabel('观测点数');ylabel('信号幅度');
    axis([0 M-1 -dB dB]);
    % 原始信号频谱
    k = 2; % 缩放横轴，显示低频信息
    xfft = fft(x);
    f = Fs / M * (0: round(M / k) - 1);
    subplot(312);
    % plot(f, abs(xfft(1: round(M / k))));
    plot(f(60000: 80000), abs(xfft(60000: 80000)));
    title('原始信号频谱');
    xlabel('频率/Hz');ylabel('频域强度');
    % axis([0 f-1 -dB dB]);
    % 原始信号功率谱
    xpower = 20 * log10(abs(xfft));
    subplot(313);
    % plot(f, xpower(1: round(M / k)));
    plot(f(60000: 80000), xpower(60000: 80000));
    title('原始信号功率谱');
    xlabel('频率/Hz');ylabel('功率谱强度');
    % 原始信号直方图
    nbins = 100;
    figure(5);
    histogram(x, nbins, 'Normalization', 'probability');
    title('原始信号直方图');
    xlabel('幅度'); ylabel('数量');
    % axis([-1 1 0 1]);
    
    figure(2);
    subplot(311);
    plot(t, s);
    title('加噪信号波形');
    xlabel('观测点数');ylabel('信号幅度');
    axis([0 M-1 -dB dB]);
    % 加噪信号频谱
    sfft = fft(s);
    subplot(312);
    % plot(f, abs(sfft(1: round(M / k))));
    plot(f(60000: 80000), abs(sfft(60000: 80000)));
    title('加噪信号频谱');
    xlabel('频率/Hz');ylabel('频域强度');
    % axis([0 f-1 -dB dB]);
    % 加噪信号功率谱
    spower = 20 * log10(abs(sfft));
    subplot(313);
    % plot(f, spower(1: round(M / k)));
    plot(f(60000: 80000), spower(60000: 80000));
    title('加噪信号功率谱');
    xlabel('频率/Hz');ylabel('功率谱强度');
    % 加噪信号直方图
    figure(6);
    histogram(s, nbins, 'Normalization', 'probability');
    title('加噪信号直方图');
    xlabel('幅度'); ylabel('数量');
    % axis([-1 1 0 1]);
    
    figure(3);
    subplot(311);
    plot(t, y);
    title('维纳滤波后波形');
    xlabel('观测点数');ylabel('误差幅度');
    axis([0 M-1 -dB dB]);
    % 滤波后信号频谱
    yfft = fft(y);
    subplot(312);
    % plot(f, abs(yfft(1: round(M / k))));
    plot(f(60000: 80000), abs(yfft(60000: 80000)));
    title('维纳滤波后频谱');
    xlabel('频率/Hz');ylabel('频域强度');
    % axis([0 f-1 -dB dB]);
    % 滤波信号功率谱
    ypower = 20 * log10(abs(yfft));
    subplot(313);
    % plot(f, ypower(1: round(M / k)));
    plot(f(60000: 80000), ypower(60000: 80000));
    title('滤波信号功率谱');
    xlabel('频率/Hz');ylabel('功率谱强度');
    % 滤波信号直方图
    figure(7);
    histogram(y, nbins, 'Normalization', 'probability');
    title('滤波信号直方图');
    xlabel('幅度'); ylabel('数量');
    % axis([-1 1 0 1]);

    % 期望和滤波后的信号对比
    figure(4);
    subplot(211);
    plot(t, d, 'r-', t, y, 'b-','LineWidth',1);
    legend('期望信号','滤波结果');
    title('期望信号与维纳滤波结果对比');
    xlabel('观测点数');ylabel('信号幅度');
    axis([0 M-1 -dB dB]);

    subplot(212);
    plot(t, e);
    title('输出误差');
    xlabel('观测点数');ylabel('误差幅度');
    axis([0 M-1 -dB dB]);
    % 三种直方图对比
    figure(8);
    histogram(x, nbins, 'Normalization', 'probability');
    hold on
    histogram(s, nbins, 'Normalization', 'probability');
    hold on
    histogram(y, nbins, 'Normalization', 'probability');
end
