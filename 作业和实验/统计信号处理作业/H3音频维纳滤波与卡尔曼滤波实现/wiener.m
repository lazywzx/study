%% wiener filter for different d(n)
%% StarryHuang 2021.1.9
close all;
clear;
clc;
%% 信号产生，对原始信号进行采样
A=10;            % 信号的幅值
B=15;            % 信号的幅值
f1=1000;      % 信号1的频率
f2=2000;      % 信号2的频率
fs=10^5;    % 采样频率
t=0:999;  % 采样点t = [0,999],长度1000
M = length(t);  % 信号长度
s=A*sin(2*pi*f1*t/fs) + B*sin(2*pi*f2*t/fs); % 采样正弦波信号为Signal
SNR = 3; % 初始信噪比
x=awgn(s,SNR,'measured'); %观测信号 x=s+v.，给正弦波信号加入信噪比为-3dB的高斯白噪声
v=x - s; % 高斯白噪声，误差信号，每次运行都不一样
%% 第一种情况——期望信号d(n)为感兴趣的原信号Signal
% d = s; 
%% 第二种情况——期望信号d(n)为Noise  v
% d = v; 
%% 第三种情况—— 期望信号d(n)为x(n-1)
d = [x(1),x(1:end-1),]; % d(n)=x(n-1)
disp(size(x(1:end-1)));

%% 维纳滤波
N = floor(length(x)*0.1);  % 滤波器的阶数，向下取整
% N=100; % 维纳滤波器阶数
Rxx=xcorr(x,N-1,'biased'); % 自相关函数1*(2N-1)维度，返回一个延迟范围在[-N，N]的互相关函数序列,对称的
% 变成矩阵 N*N维度
mRxx = zeros(N, N) * nan;
for i=1:N
    for j=1:N
        mRxx(i,j)=Rxx(N-i+j); % N*N维度
    end
end

%产生维纳滤波中x 方向上观测信号与期望信号d的互相关矩阵
Rxd=xcorr(x,d,N-1,'biased'); % 互相关函数1*(2N-1)维度


% 变成矩阵1*N维度
mRxd = zeros(1, N) * nan;
for i=1:N
    mRxd(i)=Rxd(N-1+i); % 1*N维度
end

h = mRxx\mRxd'; % 由wiener-Hopf方程得到滤波器最优解, h是N*1维度

%% 检验wiener滤波效果
y = conv(x,h); % 滤波后的输出,长度为M+N-1，要截取前M个。
y = y(1:M); % yy = filter(h,1,x);  % 用卷积或者直接用filter都可以
Py=sum(power(y,2))/M; %滤波后信号y的功率
e = d - y;  % 输出减去期望等于滤波误差
J = sum(power(e,2))/M; % 滤波后噪声功率
SNR_after = 10*log10((Py-J)/J); % 滤波后信噪比 db单位
imv = 10*log10((Py-J)/J/power(10,SNR/10)); % 滤波后较滤波前信噪比提高了imv dB。

%%  画图
% 原始信号x，噪声v，观测波形d
figure(1);
subplot(311);
plot(t,s); % 输入函数
title(' Signal原信号');

subplot(312);
plot(t,v); % 输入函数
title(' Noise噪声');

subplot(313);
plot(t,x); % 输入函数
title(' X(n)观测波形');

%% d = s
% 期望和滤波后的信号对比
figure(2);
subplot(211);
plot(t, d, 'r-', t, y, 'b-','LineWidth',1);
legend('期望信号','滤波后结果'); title('期望信号与滤波结果对比');
xlabel('观测点数');ylabel('信号幅度');
axis([0 1000 -50 50]);

subplot(212);
plot(t, e);
title('输出误差');
xlabel('观测点数');ylabel('误差幅度');
axis([0 1000 -50 50]);

% 滤波前后对比
figure(3);
subplot(211);
plot(t, x);
title('维纳滤波前');
xlabel('观测点数');ylabel('信号幅度');
axis([0 1000 -50 50]);

subplot(212);
plot(t, y);
title('维纳滤波后');
xlabel('观测点数');ylabel('误差幅度');
axis([0 1000 -50 50]);
