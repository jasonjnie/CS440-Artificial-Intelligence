fileID = fopen('facedatatrainlabels.txt','r');
formatSpec = '%f';
train_label = fscanf(fileID,formatSpec);

fileID = fopen('facedatatrain.txt','r');
formatSpec = '%c';
train_image = fscanf(fileID,formatSpec);
%each face 70x61
for i = 1:451*70
    train_image_modify(i,:)= train_image((i-1)*61+1:(i-1)*61+61);%(451x70)x61
end
%train_image_modify(1:70,:) is first image

s = struct;%5000 training tokens with its corresponding image and label
for j = 1:451
    s(j).image = train_image_modify((j-1)*70+1:(j-1)*70+70,:);%each is (70*61)
    s(j).label = train_label(j);%each is one digit
end 

%% training:
prob = cell([10,2]); %class number * char number * image
for i = 1:10
    for j = 1:2
    prob{i,j} = zeros(70,61);
    end 
end 
count = zeros(10,2);

for k = 1:451
    i = s(k).label;
    i = i+1;
    %#
    cur_image = s(k).image;
    cur_image(cur_image=='#') = 1;
    cur_image(cur_image==' ') = 0;%cur_image is the 70x70 matrix of 1 or 0
    prob{i,1} = double(cur_image) + prob{i,1};
    count(i,1)= count(i,1)+1;
       
    % 
    cur_image = s(k).image;
    cur_image(cur_image=='#') = 0;
    cur_image(cur_image==' ') = 1;%cur_image is the 28x28 matrix of 1 or 0
    prob{i,2} = double(cur_image) + prob{i,2};
    count(i,2)= count(i,2)+1;   
end 
%count(i,:) three entries same.

k=0.1;
for i = 1:10
    for j = 1:2
    prob{i,j} = (k+prob{i,j})/(count(i,j)+2*k);
    end 
end 

%% testing:
fileID = fopen('facedatatestlabels.txt','r');
formatSpec = '%f';
test_label = fscanf(fileID,formatSpec);

fileID = fopen('facedatatest.txt','r');
formatSpec = '%c';
test_image = fscanf(fileID,formatSpec);

for i = 1:150*70
    test_image_modify(i,:)= test_image((i-1)*61+1:(i-1)*61+61);%(451x70)x61
end
%train_image_modify(1:70,:) is first image

s_test = struct;%5000 training tokens with its corresponding image and label
for j = 1:150
    s_test(j).image = test_image_modify((j-1)*70+1:(j-1)*70+70,:);%each is (70*61)
    s_test(j).label = test_label(j);%each is one digit
end 

test_result = zeros(150,10);
for k = 1:150
    for i=1:10
    %#
    cur_image = s_test(k).image;
    cur_image(cur_image=='#') = 1;
    cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
    cur_image = double(cur_image); 
    prob_star = cur_image.*prob{i,1};
    prob_star(prob_star==0)=1;
    
    % 
    cur_image = s_test(k).image;
    cur_image(cur_image=='#') = 0;
    cur_image(cur_image==' ') = 1;%cur_image is the 28x28 matrix of 1 or 0
    cur_image = double(cur_image);
    prob_white = cur_image.*prob{i,2}; 
    prob_white(prob_white==0)=1;
    
    test_result(k,i)=log(count(i,1)/150)+sum(sum(log(prob_white)))+sum(sum(log(prob_star)));
    end 
end 

[value index] = max(test_result');
predict_label = index -1;

accuracy_total = sum(test_label==predict_label')/150;


%%


count_0_test=0;
count_1_test=0;
count_2_test=0;
count_3_test=0;
count_4_test=0;
count_5_test=0;
count_6_test=0;
count_7_test=0;
count_8_test=0;
count_9_test=0;
correct_0=0;
correct_1=0;
correct_2=0;
correct_3=0;
correct_4=0;
correct_5=0;
correct_6=0;
correct_7=0;
correct_8=0;
correct_9=0;

for m = 1:1000
    if (test_label(m) == 0)
        count_0_test = count_0_test+1;
        correct_0 = correct_0 +(test_label(m)==predict_label(m));
    end 
    
    if (test_label(m) == 1)
        count_1_test = count_1_test+1;
        correct_1 = correct_1 +(test_label(m)==predict_label(m));
    end    
    
    if (test_label(m) == 2)
        count_2_test = count_2_test+1;
        correct_2 = correct_2 +(test_label(m)==predict_label(m));
    end
    
    if (test_label(m) == 3)
        count_3_test = count_3_test+1;
        correct_3 = correct_3 +(test_label(m)==predict_label(m));
    end 
    
    if (test_label(m) == 4)
        count_4_test = count_4_test+1;
        correct_4 = correct_4 +(test_label(m)==predict_label(m));
    end 
    
    if (test_label(m) == 5)
        count_5_test = count_5_test+1;
        correct_5 = correct_5 +(test_label(m)==predict_label(m));
    end 
    
    if (test_label(m) == 6)
        count_6_test = count_6_test+1;
        correct_6 = correct_6 +(test_label(m)==predict_label(m));
    end 
    
    if (test_label(m) == 7)
        count_7_test = count_7_test+1;
        correct_7 = correct_7 +(test_label(m)==predict_label(m));
    end 
    
    if (test_label(m) == 8)
        count_8_test = count_8_test+1;
        correct_8 = correct_8 +(test_label(m)==predict_label(m));
    end 
    
    if (test_label(m) == 0)
        count_9_test = count_9_test+1;
        correct_9 = correct_9 +(test_label(m)==predict_label(m));
    end 
end 

accuracy_0 = correct_0/count_0_test;
accuracy_1 = correct_1/count_1_test;
accuracy_2 = correct_2/count_2_test;
accuracy_3 = correct_3/count_3_test;
accuracy_4 = correct_4/count_4_test;
accuracy_5 = correct_5/count_5_test;
accuracy_6 = correct_6/count_6_test;
accuracy_7 = correct_7/count_7_test;
accuracy_8 = correct_8/count_8_test;
accuracy_9 = correct_9/count_9_test;

%% cofusion matrix

confusion_matrix = zeros(10,10);
for i = 1:10
    index_label=find(test_label==(i-1));%return the index of test labels with label i
    output = predict_label(index_label);%corresponding output label in predict labels
    confusion_matrix(i,1) = sum(output==0)/length(output);%number that predict label is predicted as 1 given test label i
    confusion_matrix(i,2) = sum(output==1)/length(output);
    confusion_matrix(i,3) = sum(output==2)/length(output);
    confusion_matrix(i,4) = sum(output==3)/length(output);
    confusion_matrix(i,5) = sum(output==4)/length(output);
    confusion_matrix(i,6) = sum(output==5)/length(output); 
    confusion_matrix(i,7) = sum(output==6)/length(output);
    confusion_matrix(i,8) = sum(output==7)/length(output);
    confusion_matrix(i,9) = sum(output==8)/length(output);
    confusion_matrix(i,10) = sum(output==9)/length(output);
end 


