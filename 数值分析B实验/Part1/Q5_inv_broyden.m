format long;    % 指定精度
% 初值、误差、最大迭代次数
x0 = [1, 1, 1]';
ex = [5e-6, 5e-6, 5e-6]';   % 当向量x(x, y, z)小于ex时迭代成功
ef = [1e-10, 1e-10, 1e-10]';    % 当F(x)小于ef时输出奇异标志
n = 20;

% 执行迭代
[msg, x0, k] = inv_broyden(x0, ex, ef, n);
% 输出结果
disp([msg, "迭代次数: ", num2str(k)]);
disp("向量(x, y, z)': ");
disp(x0);


function [x1, H1, F1, r0] = compute(x0, H0)
% 迭代一次

% 定义方程组
syms x y z;
F = [x * y - z^2 - 1, x * y * z + y^2 - x^2 - 2, exp(x) + z - exp(y) - 3]';

x = x0(1); y = x0(2); z = x0(3);
F0 = eval(F);   % 计算符号表达式的值
x1 = x0 - H0 * F0;
r0 = x1 - x0;

x = x1(1); y = x1(2); z = x1(3);
F1 = eval(F);
y0 = F1 - F0;
H1 = H0 + (r0 - H0 * y0) * ((r0' * H0) / (r0' * H0 * y0));
end


function [msg, x0, k] = inv_broyden(x0, ex, ef, n)
% 逆broyden法

% 定义方程组并求导
syms x y z;
F = [x * y - z^2 - 1, x * y * z + y^2 - x^2 - 2, exp(x) + z - exp(y) - 3]';
F_diff = jacobian(F, [x, y, z]);

% 求H0
x = x0(1); y = x0(2); z = x0(3);
H0 = eval(F_diff)^(-1);

% 迭代过程
msg = "";   % 迭代结果
k = 0;  % 迭代次数计数
while true
    [x0, H0, F1, r0] = compute(x0, H0); % 将返回值作为参数传回函数以迭代
    
    if sum(abs(F1) < ef) > 0    % 任意一个方程产生奇异，方程组产生奇异
        msg = "奇异标志";
        return;
    end
    
    if sum(abs(r0) < ex) == 3   % x, y, z均满足误差要求，迭代成功
        msg = "迭代成功";
        return;
    end
    
    if k == n   % 达到最大迭代次数，迭代失败
        msg = "迭代失败";
        return;
    end
    % disp(x0); % 查看每一步迭代结果
    k = k + 1;
end
end
