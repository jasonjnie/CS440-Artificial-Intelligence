function [J Theta1_grad Theta2_grad Theta3_grad] = nnCostFunction_sigmoid(Theta1, Theta2, Theta3,input_layer_size, hidden_layer_size1, hidden_layer_size2,num_labels,  X, y)

m = size(X, 1);
recode_y = zeros(m, num_labels);
recode_y(sub2ind(size(recode_y), [1:m]',y)) = 1;%recode y into num_label dim

a_2 = sigmoid([ones(m, 1) X]* Theta1');
a_3 = sigmoid([ones(m, 1) a_2] * Theta2');
a_4 = nnsoftmax([ones(m, 1) a_3] * Theta3'); %final calculated output

% J = 1/m * (-recode_y .* log(a_4) - (1 - recode_y) .* log(1 - a_4));%change this!!?
% J = sum(J(:));
J = -recode_y .* log(a_4);
%display(a_4);
J = sum(J(:));

delta_4 = a_4 - recode_y;%500x9
%X: 500x1120
%weight3: 9x51
%weight2: 50x51
%weight1: 50x(1121)
delta_3 = delta_4 * Theta3(:,2:end) .* sigmoidGradient([ones(m, 1) a_2] * Theta2');%(500x50).*(500x50)
delta_2 = delta_3 * Theta2(:,2:end) .* sigmoidGradient([ones(m, 1) X] * Theta1');

Theta1_grad = delta_2' * [ones(m, 1) X];%50x1121
Theta2_grad = delta_3' * [ones(m, 1) a_2]; 
Theta3_grad = delta_4' * [ones(m, 1) a_3]; 

end
