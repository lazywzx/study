%% 系数处理函数
function [coemax] = select_coefficient(ratio, coemax)
    [row, col] = size(coemax);
    % 二维数据转一维数据
    coemax = reshape(coemax, col * row, 1);
    % 由大到小排序
    [sortcoemax, index] = sort(abs(coemax), 'descend');
    % 计算阈值
    thesh = sortcoemax(ceil(col * row * ratio));
    % 截取系数
    for i = 1:size(coemax)
        coemax(index(i)) = coemax(index(i)) .* (abs(coemax(index(i)) > thesh));
    end
    % 恢复维度
    coemax = reshape(coemax, row, col);
end
