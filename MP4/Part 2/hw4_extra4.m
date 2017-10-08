%% Setup the parameters 
input_layer_size  = 784;%784 features each sample 
num_labels = 10;%binary classification         
hidden_layer_size1 = 50; 
hidden_layer_size2 = 50;                     
%% get X, y
%train:

% fileID = fopen('traininglabels.txt','r');
% formatSpec = '%f';
% train_label = fscanf(fileID,formatSpec);
% 
% fileID = fopen('trainingimages.txt','r');
% formatSpec = '%c';
% train_image = fscanf(fileID,formatSpec);
% 
% for i = 1:5000*28
%     train_image_modify(i,:)= train_image((i-1)*29+1:(i-1)*29+1+27);%(5000x28)x28
% end
% %train_image_modify(1:28,:) is first image

% X = zeros(5000,28*28);
% y = zeros(5000,1);
% 
% for j = 1:5000
%     cur_image = reshape(train_image_modify((j-1)*28+1:(j-1)*28+1+27,:),1,28*28);
%     cur_image(cur_image=='#') = 1;
%     cur_image(cur_image=='+') = 1;
%     cur_image(cur_image==' ') = 0;
%     cur_image = double(cur_image);
%     X(j,:) = cur_image;%5000x784
%     y(j,:) = train_label(j);%5000x1
%     
% end 

X = matfile('X_train.mat');
X = X.X;
y = matfile('y_train.mat');
y = y.y;

y = y+1;
% %one hot vector(has added each entry by 1)
% y_modify = zeros(5000,10);
% for k = 1:5000
%     y_modify(k,y(k)+1) =1; 
% end 
% y = y_modify;

%test:
% fileID = fopen('testlabels.txt','r');
% formatSpec = '%f';
% test_label = fscanf(fileID,formatSpec);
% 
% fileID = fopen('testimages.txt','r');
% formatSpec = '%c';
% test_image = fscanf(fileID,formatSpec);
% 
% for i = 1:1000*28
%     test_image_modify(i,:)= test_image((i-1)*29+1:(i-1)*29+1+27);%(1000x28)x28
% end
% 
% X = zeros(1000,28*28);
% y = zeros(1000,1);
%  
%  for j = 1:1000
%      cur_image = reshape(test_image_modify((j-1)*28+1:(j-1)*28+1+27,:),1,28*28);
%      cur_image(cur_image=='#') = 1;
%      cur_image(cur_image=='+') = 1;
%      cur_image(cur_image==' ') = 0;
%      cur_image = double(cur_image);
%      X(j,:) = cur_image;%1000x784
%      y(j,:) = test_label(j);%1000x1
%      
%  end 
%% logistic 
% % ================ Initializing Pameters ================
 Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size1);%(m,n)return (nx (m+1)) 
 Theta2 = randInitializeWeights(hidden_layer_size1, hidden_layer_size2);
 Theta3 = randInitializeWeights(hidden_layer_size2, num_labels);
% %% =================== Training NN ===================              
 error_rates = zeros(500,1);
 loss = zeros(500,1);
 learning_rate = 0.001;
 
 for itr = 1:500
      for i = 1:50
          
        [X_input,idx] = datasample(X,100,'Replace',false);
        y_input = y(idx,:);
        [loss Theta1_grad Theta2_grad Theta3_grad] = nnCostFunction_sigmoid(Theta1, Theta2, Theta3,input_layer_size, hidden_layer_size1, hidden_layer_size2,num_labels, X_input, y_input);
        
        Theta1 = Theta1 - learning_rate * Theta1_grad;
        Theta2 = Theta2 - learning_rate * Theta2_grad;
        Theta3 = Theta3 - learning_rate * Theta3_grad;

      end
        error_rates(itr) = error_rates_sigmoid(X,y,Theta1,Theta2,Theta3);
        %error_rates(itr) =  error_rates_sigmoid(Theta1,Theta2,Theta3);
 end
 
 
        plot(error_rates);
        title('sigmoid');
        xlabel('epochs');
        ylabel('training corpus error rates');
        
X = matfile('X_test.mat');
X_test = X.X;
y = matfile('y_test.mat');
y_test = y.y;
y_test = y_test+1;

accuracy_sigmoid = 1-error_rates_sigmoid(X_test,y_test,Theta1,Theta2,Theta3);
display(accuracy_sigmoid);


%% tanh
% % ================ Initializing Pameters ================
 Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size1);%(m,n)return (nx (m+1)) 
 Theta2 = randInitializeWeights(hidden_layer_size1, hidden_layer_size2);
 Theta3 = randInitializeWeights(hidden_layer_size2, num_labels);
% %% =================== Training NN ===================              
 error_rates = zeros(500,1);
 loss = zeros(500,1);
 learning_rate = 0.001;
 
%5280concatenate
 for itr = 1:500
      for i = 1:50
          
        [X_input,idx] = datasample(X,100,'Replace',false);
        y_input = y(idx,:);
        [loss Theta1_grad Theta2_grad Theta3_grad] = nnCostFunction_tanh(Theta1, Theta2, Theta3,input_layer_size, hidden_layer_size1, hidden_layer_size2,num_labels, X_input, y_input);
        
        Theta1 = Theta1 - learning_rate * Theta1_grad;
        Theta2 = Theta2 - learning_rate * Theta2_grad;
        Theta3 = Theta3 - learning_rate * Theta3_grad;

      end

        error_rates(itr) =  error_rates_ttanh(X,y,Theta1,Theta2,Theta3);
 end


         plot(error_rates);
         title('tanh');
         xlabel('epochs');
         ylabel('training corpus error rates');
        
X = matfile('X_test.mat');
X_test = X.X;
y = matfile('y_test.mat');
y_test = y.y;
y_test = y_test+1;

accuracy_tanh = 1-error_rates_ttanh(X_test,y_test,Theta1,Theta2,Theta3);
display(accuracy_tanh);
        
%% relu
% % ================ Initializing Pameters ================
 Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size1);%(m,n)return (nx (m+1)) 
 Theta2 = randInitializeWeights(hidden_layer_size1, hidden_layer_size2);
 Theta3 = randInitializeWeights(hidden_layer_size2, num_labels);
% %% =================== Training NN ===================              
 error_rates = zeros(500,1);
 loss = zeros(500,1);
 learning_rate = 0.0001;
 
%5280concatenate
 for itr = 1:500
      for i = 1:50
          
        [X_input,idx] = datasample(X,100,'Replace',false);
        y_input = y(idx,:);
        [loss Theta1_grad Theta2_grad Theta3_grad] = nnCostFunction_relu(Theta1, Theta2, Theta3,input_layer_size, hidden_layer_size1, hidden_layer_size2,num_labels, X_input, y_input);
        
        Theta1 = Theta1 - learning_rate * Theta1_grad;
        Theta2 = Theta2 - learning_rate * Theta2_grad;
        Theta3 = Theta3 - learning_rate * Theta3_grad;

      end
        %loss(itr) = loss;
        error_rates(itr) =  error_rates_relu(X,y,Theta1,Theta2,Theta3);
 end

         plot(error_rates);
         title('relu');
         xlabel('epochs');
         ylabel('training corpus error rates');
        
X = matfile('X_test.mat');
X_test = X.X;
y = matfile('y_test.mat');
y_test = y.y;
y_test = y_test+1;

accuracy_relu = 1-error_rates_relu(X_test,y_test,Theta1,Theta2,Theta3);
display(accuracy_relu);
