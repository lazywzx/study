% 设定真值向量
tvar = [50 60 70]';
disp("真值向量：");
disp(tvar);

% 设定传递矩阵
H1 = [1 -1 1; 0 0 1; 1 1 1];
H2 = [1 1 1; 4 2 1; 9 3 1];
fprintf("H1 = \t\t\tH2 = \n");
disp([H1, H2]);

count = 1;
for i=1:10
    % 观测模型
    z1 = awgn(H1 * tvar, 10);
    z2 = awgn(H2 * tvar, 10);
    % 估计向量
    evar1 = (H1' * H1)^(-1) * H1' * z1;
    disp(sum(evar1)/3);
    disp(sum(evar2)/3);
    evar2 = (H2' * H2)^(-1) * H2' * z2;
    
    fprintf("第%d次观测：\n", count);
    fprintf(" H1估计值： \tH2估计值：\n");
    disp([evar1, evar2]);
    count = count + 1;
end




