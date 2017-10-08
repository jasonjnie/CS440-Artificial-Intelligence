
X = matfile('X_train.mat');
X_train = X.X;
y = matfile('y_train.mat');
y_train = y.y;

X = matfile('X_test.mat');
X_test = X.X;
y = matfile('y_test.mat');
y_test = y.y;

k = 3;
count = 0;
y_predict = zeros(1000,1);
for i=1:size(X_test,1)
    NN = zeros(size(X_train,1),1);
    KNN = zeros(k,1);
    for j=1:size(X_train,1)%each test sample, store distance to all the training samples
        %NN(j,1) = sqrt(sum(abs(X_test(i,:)-X_train(j,:)).^2));%Euclidean distance
        NN(j,1) = sum(abs(X_test(i,:)-X_train(j,:)));%Manhanttan distance
    end 
    [data,idx] = sort(NN,'ascend');
    KNN = y_train(idx(1:k),1);%knn labels in training data
     
    [M F predict] = mode(KNN);
    
    y_predict(i,1) = predict{1}(1);
    for m=1:size(predict{1},1) 
        if(predict{1}(m) == y_test(i,1))
            count = count+1;
            y_predict(i,1) = predict{1}(m);
        end 
    end 
end 

test_accuracy = count/size(X_test,1);
confusion_matrix = confusionmat(y_predict,y_test);