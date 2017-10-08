function [Theta_update] = nnCostFunction_perceptron(Theta1, X, y, learning_rate)
%Theta1' = 785*10 
%X = n*785
m = size(X,1);

Theta = Theta1';%785x10
y_ = [ones(m, 1) X]*Theta;%n*10
[y_ index] = max(y_');%index: nx1 indicates the class predicted
%y: nx1 indeicates true class labels
error_index = index' ~= y;%nx1 with 1 indicates the miss classified ones

for i=1:size(X,1)%epoch number
    if (error_index(i,:)==1) %misclassfied
        %index(i)%predict label
        %y(i)%true label
        Theta(:,index(i))=Theta(:,index(i))+learning_rate*X(i,:)';%785x1
        Theta(:,y(i))=Theta(:,y(i))-learning_rate*X(i,:)';%785x1
    end 
end 

Theta_update = Theta;
% y(y==0) = -1;
% 
% [c,d] = size(Theta1);%1x17
% m = size(X, 1);
% 
% 
% a_1 = max(0,-[ones(m, 1) X]* Theta1'.*y);%x*w'+b %x*w'+b=n*1 %1200*1 %x is nx784->n*785 %Theta1' = 785*10 
% index_nonzero = find(a_1);%corresponds to error samples
% 
% J = sum(a_1);
% 
% X_new = [ones(m, 1) X];%1200x17
% Theta1_grad = -y(index_nonzero,:)'*X_new(index_nonzero,:);%1xn * nx17
% 
% grad = Theta1_grad;
end
