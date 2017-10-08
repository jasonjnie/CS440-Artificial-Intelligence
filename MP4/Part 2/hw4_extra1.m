%% Setup the parameters 
input_layer_size  = 784;%784 features each sample 
num_labels = 10;%binary classification         
                         
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

%% perceptron         
% % ================ Initializing Pameters ================
 initial_Theta = randInitializeWeights(input_layer_size, num_labels);%returns 10x785
% %% =================== Training NN ===================                
 %costs = zeros(5000,1);

 %epoch = 1000;
 epoch = 1000;
 for itr = 1:epoch
        learning_rate = 1/(1000+itr);
%         [X_data,index] = datasample(X,epoch,'Replace',false);%X_data: epoch * 784
%         y_data = y(index',:);%y_data: epoch * 1
        idx = randperm(size(X,1));
        X_data = X(idx,:);
        y_data = y(idx,:);
        
        y_ = sigmoid([ones(size(X_data,1), 1) X_data]*initial_Theta');%epoch * 10
        
        [y_max index] = max(y_');%epoch * 1(index: predicted labels)
         error_index = index' ~= y_data;%misclassifictaion

         %initial_Theta = initial_Theta + learning_rate*(y_data-index').*y_.*(1-y_)*[ones(size(X_data,1), 1) X_data];
        
         for i=1:size(X_data,1)%epoch
             if (error_index(i,:)==1) %misclassfied
             %index(i) - predict label
             %y_data(i) - true label
             sig1 = sigmoid(initial_Theta(index(i),:)*[ones(1, 1) X_data(i,:)]');
             sig2 = sigmoid(initial_Theta(y_data(i),:)*[ones(1, 1) X_data(i,:)]');
             
             initial_Theta(index(i),:)=initial_Theta(index(i),:)-learning_rate*[ones(1, 1) X_data(i,:)]*sig1*(1-sig1);%1x785
             initial_Theta(y_data(i),:)=initial_Theta(y_data(i),:)+learning_rate*[ones(1, 1) X_data(i,:)]*sig2*(1-sig2);%1x785
             %change the row (1/10) when class missclassified
             end 
         end 

        error_rates(itr) =  error_rates_perceptron(initial_Theta);
%         save('error_rates_perceptron.txt','error_rates','-ascii');
%         costs(itr) = cost;
%         save('costs_perceptron.txt','costs','-ascii');
 end
 

        plot(error_rates);
        title('perceptron');
        xlabel('epochs');
        ylabel('training corpus error rates');
%         save('Theta_perceptron.txt','initial_Theta1','-ascii');

%% testing:
X = matfile('X_test.mat');
X_test = X.X;
y = matfile('y_test.mat');
y_test = y.y;
 

m = size(X_test, 1);
a = sigmoid([ones(m, 1) X_test]* initial_Theta');%epoch x 10
[data,index] = max(a');
y_test = y_test+1;
test_accuracy = sum(index' == y_test)/m;

%% confusion matrix
confusion_matrix = confusionmat(index',y_test);
