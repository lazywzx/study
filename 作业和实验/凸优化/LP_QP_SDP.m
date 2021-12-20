clear;
clc;
%% LP
% % define coefficients
% c = [4, -3, -6, 1]';
% A = [3, 5, -6;
%     2, -1, 3;
%     7, -4, 8;
%     -5, 2, 3];
% Ix = [-100, -100, -100, -100]';
% ux = [100, 100, 100, 100]';
% Iy = [-100, -100, -100]';
% uy = [100, 100, 100]';
% % define variables
% x = sdpvar(4, 1);
% y = sdpvar(3, 1);
% % objective
% obj = c' * x;
% % constrains
% cons = [x == A * y, Ix <= x <= ux, Iy <= y <= uy];
% % options
% options = sdpsettings('solver', 'sedumi', 'verbose', 0);
% % optimize
% optimize(cons, obj, options);
% % solution
% x_sol = value(x);
% y_sol = value(y);
% % disp
% disp('LP: ');
% disp('optimal x: ');
% disp(x_sol);
% disp('optimal y: ');
% disp(y_sol);
%% QP
% % define coefficients
% Q = [2, 5, 3;
%     4, 6, 8;
%     1, 0, 7];
% A = [5, 2;
%     -1, -3;
%     6, 8];
% Q1 = [1, 2, 3;
%     3, 6, 9;
%     4, 2, 5];
% Q2 = [7, 2, 1;
%     9, 3, 5;
%     6, 1, 4];
% b1 = 100;
% b2 = 100;
% u = [100, -100]';
% % define variables
% x = sdpvar(3, 1);
% y = sdpvar(2, 1);
% % objective
% obj = x' * Q * x;
% % constrains
% cons = [x == A * y, x' * Q1 * x <= b1, x' * Q2 * x <= b2, y <= u];
% % options
% options = sdpsettings('solver', '', 'verbose', 0);
% % optimize
% optimize(cons, obj, options);
% % solution
% x_sol = value(x);
% y_sol = value(y);
% % disp
% disp('QP: ');
% disp('optimal x: ');
% disp(x_sol);
% disp('optimal y: ');
% disp(y_sol);
%% SDP
% define coefficients
C = diag([5, 6, 9, 3]);
A = [1, -5, 2, 1;
    -2, 3, 6, -9;
    3, -5, 8, 8];
E = [5, 3, -2, 4;
    6, -3, 4, 1];
b = [100, 100, 100];
f = [100, 10];
% define variables
X = sdpvar(4, 4, 'symmetric');
% objective
obj = trace(C * X);
% constrains
cons = [X >= 0];
for k = 1: 3
    cons = cons + [trace(diag(A(k, :)) * X) <= b(k)];
end

for k = 1: 2
    cons = cons + [trace(diag(E(k, :)) * X) == f(k)];
end
% options
options = sdpsettings('solver', 'sedumi', 'verbose', 0);
% optimize
optimize(cons, obj, options);
% solution
X_sol = value(X);
% disp
disp('SDP: ');
disp('optimal x: ');
disp(X_sol);
