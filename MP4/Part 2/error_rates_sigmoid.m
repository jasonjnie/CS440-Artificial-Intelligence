function [error_rate] = error_rates_sigmoid(X,y,Theta1,Theta2,Theta3)

m = size(X, 1);
a_2 = sigmoid([ones(m, 1) X]* Theta1');%  17x10
a_3 = sigmoid([ones(m, 1) a_2] * Theta2');
a_4 = nnsoftmax([ones(m, 1) a_3] * Theta3');

[Value, Index]=max(a_4,[],2);%index is the index of max number each row 
%display(size(a_4));
%Index = Index+1; % y calculated target label

error_rate = 1 - sum(Index==y)/size(y,1);
confusionmat(Index,y)
end 