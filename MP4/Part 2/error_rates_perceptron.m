function [error_rates] = error_rates_perceptron(initial_Theta1)
 X = matfile('X_train.mat');
 X = X.X;
 y = matfile('y_train.mat');
 y = y.y;
 
 
Theta = initial_Theta1;%1x17
m = size(X, 1);

a = [ones(m, 1) X]* Theta';%epoch x 10
[data,index] = max(a');

y = y+1;

error_rates = 1-sum(index' == y)/m;

end 