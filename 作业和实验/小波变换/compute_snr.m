%% 计算信噪比
function [SNR] = compute_snr(X, recX)
    mu = mean(mean((X - recX) .^2));    % 噪声均方差
    ro = mean(mean(X .^2));    % 原图对比度
    SNR = 20 * log10(double(ro / mu));  % 对数表示信噪比
end
