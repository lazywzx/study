% 画出自己声音的频谱
% 计算声音波长

% 读取音频文件
[x, Fs] = audioread('./my_voice.m4a');

% 画出时域波形
M = length(x);  % 信号的序列长度
T = M / Fs;   % 信号的时间长度
t = (0: M-1) / Fs;    % 信号的采样点时刻序列
figure(1);
subplot(311);
plot(t, x);
title('时域波形');
xlabel('时间'); ylabel('幅值');
axis([0 T -0.5 0.5]);

% 画出频谱
f = (0: round(M / 2) - 1) / M * Fs; % 信号的实际频点序列
y = fft(x); % 傅里叶变换到频域
subplot(312);
plot(f, abs(y(1: round(M / 2))));
title('频域频域');
xlabel('频率'); ylabel('幅值');

% 放大低频部分
subplot(313);
plot(f(1: round(M / 50)), abs(y(1: round(M / 50))));
title('频域低频部分');
xlabel('频率'); ylabel('幅值');

 % 计算波长
[fm, index] = max(abs(y(1: round(M / 2))));
l = 340 / f(index);
disp(['声音波长为：', num2str(l), '米']);
