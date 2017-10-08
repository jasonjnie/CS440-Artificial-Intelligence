fileID = fopen('traininglabels.txt','r');
formatSpec = '%f';
train_label = fscanf(fileID,formatSpec);

fileID = fopen('trainingimages.txt','r');
formatSpec = '%c';
train_image = fscanf(fileID,formatSpec);

for i = 1:5000*28
    train_image_modify(i,:)= train_image((i-1)*29+1:(i-1)*29+1+27);%(5000x28)x28
end
%train_image_modify(1:28,:) is first image

s = struct;%5000 training tokens with its corresponding image and label
for j = 1:5000
    s(j).image = train_image_modify((j-1)*28+1:(j-1)*28+1+27,:);%each is (28*28)
    s(j).label = train_label(j);%each is one digit
end 

%% training:
prob = cell([10,3]); %class number * char number * image
for i = 1:10
    for j = 1:3
    prob{i,j} = zeros(28,28);
    end 
end 
count = zeros(10,3);

for k = 1:5000
    i = s(k).label;
    i = i+1;
    %#
    cur_image = s(k).image;
    cur_image(cur_image=='#') = 1;
    cur_image(cur_image=='+') = 0;
    cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
    prob{i,1} = double(cur_image) + prob{i,1};
    count(i,1)= count(i,1)+1;
    
    %+
    cur_image = s(k).image;
    cur_image(cur_image=='#') = 0;
    cur_image(cur_image=='+') = 1;
    cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
    prob{i,2} = double(cur_image) + prob{i,2};
    count(i,2)= count(i,2)+1;
       
    % 
    cur_image = s(k).image;
    cur_image(cur_image=='#') = 0;
    cur_image(cur_image=='+') = 0;
    cur_image(cur_image==' ') = 1;%cur_image is the 28x28 matrix of 1 or 0
    prob{i,3} = double(cur_image) + prob{i,3};
    count(i,3)= count(i,3)+1;   
end 
%count(i,:) three entries same.

k=0.1;
for i = 1:10
    for j = 1:3
    prob{i,j} = (k+prob{i,j})/(count(i,j)+2*k);
    end 
end 

%% testing:
fileID = fopen('testlabels.txt','r');
formatSpec = '%f';
test_label = fscanf(fileID,formatSpec);

fileID = fopen('testimages.txt','r');
formatSpec = '%c';
test_image = fscanf(fileID,formatSpec);

for i = 1:1000*28
    test_image_modify(i,:)= test_image((i-1)*29+1:(i-1)*29+1+27);%(1000x28)x28
end
%train_image_modify(1:28,:) is first image

s_test = struct;%5000 training tokens with its corresponding image and label
for j = 1:1000
    s_test(j).image = test_image_modify((j-1)*28+1:(j-1)*28+1+27,:);%each is (28*28)
    s_test(j).label = test_label(j);%each is one digit
end

test_result = zeros(1000,10);
for k = 1:1000
    for i=1:10
    %#
    cur_image = s_test(k).image;
    cur_image(cur_image=='#') = 1;
    cur_image(cur_image=='+') = 0;
    cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
    cur_image = double(cur_image); 
    prob_star = cur_image.*prob{i,1};
    prob_star(prob_star==0)=1;
    %+
    cur_image = s_test(k).image;
    cur_image(cur_image=='#') = 0;
    cur_image(cur_image=='+') = 1;
    cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
    cur_image = double(cur_image);   
    prob_plus = cur_image.*prob{i,2};    
    prob_plus(prob_plus==0)=1;
    % 
    cur_image = s_test(k).image;
    cur_image(cur_image=='#') = 0;
    cur_image(cur_image=='+') = 0;
    cur_image(cur_image==' ') = 1;%cur_image is the 28x28 matrix of 1 or 0
    cur_image = double(cur_image);
    prob_white = cur_image.*prob{i,3}; 
    prob_white(prob_white==0)=1;
    
    test_result(k,i)=log(count(i,1)/5000)+sum(sum(log(prob_white)))+sum(sum(log(prob_plus)))+sum(sum(log(prob_star)));
    end 
end 

[value index] = max(test_result');
predict_label = index -1;

accuracy_total = sum(test_label==predict_label')/1000;
