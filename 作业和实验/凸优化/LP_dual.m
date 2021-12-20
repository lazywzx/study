clear;
clc;
%% define coefficients
c = [47, 93, 17, -93]';
A = [-1, -6, 1, 3;
     -1, -2, 7, 1;
     0, 3, -10, -1;
     -6, -11, -2, 12;
     1, 6, -1, -3];
b = [-3, 5, -8, -7, 4]';
%% define variables
x = sdpvar(4, 1);
lamda = sdpvar(5, 1);
%% objective
pri_obj = c'*x;
dual_obj = -lamda'*b;
%% constrains
pri_cons = [A*x <= b];
dual_cons = [c' + lamda'*A == zeros(4, 1)', lamda >= zeros(5, 1)];
%% options
options = sdpsettings('solver', 'sedumi', 'verbose', 0);
%% optimize
optimize(pri_cons, pri_obj, options);
optimize(dual_cons, -dual_obj, options);
%% solution
pri_sol = value(x);
dual_sol = value(lamda);
%% disp
disp('主问题的最优解：');
disp(pri_sol);
disp('对偶问题的最优解：');
disp(dual_sol);
%% verify KKT conditions
disp('验证KKT条件：');
disp('Ax - b: ');
disp(A*pri_sol - b);
disp('lamda: ');
disp(dual_sol);
disp('lamda(Ax - b): ');
disp(dual_sol'*(A*pri_sol - b));
disp('c + lamdaA');
disp(c' + dual_sol' * A);
