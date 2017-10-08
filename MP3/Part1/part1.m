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
%given class 0:
p_0 = zeros(28,28);
p_1 = zeros(28,28);
p_2 = zeros(28,28);
p_3 = zeros(28,28);
p_4 = zeros(28,28);
p_5 = zeros(28,28);
p_6 = zeros(28,28);
p_7 = zeros(28,28);
p_8 = zeros(28,28);
p_9 = zeros(28,28);
count_0 = 0;
count_1 = 0;
count_2 = 0;
count_3 = 0;
count_4 = 0;
count_5 = 0;
count_6 = 0;
count_7 = 0;
count_8 = 0;
count_9 = 0;
for k = 1:5000
    if (s(k).label == 0)
        cur_image = s(k).image;
        cur_image(cur_image=='#') = 1;
        cur_image(cur_image=='+') = 1;
        cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
        p_0 = double(cur_image) + p_0;
        count_0= count_0+1;
    end 
    
    if (s(k).label == 1)
        cur_image = s(k).image;
        cur_image(cur_image=='#') = 1;
        cur_image(cur_image=='+') = 1;
        cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
        p_1 = double(cur_image) + p_1;
        count_1= count_1+1;
    end 
    
    if (s(k).label == 2)
        cur_image = s(k).image;
        cur_image(cur_image=='#') = 1;
        cur_image(cur_image=='+') = 1;
        cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
        p_2 = double(cur_image) + p_2;
        count_2= count_2+1;
    end 

    if (s(k).label == 3)
        cur_image = s(k).image;
        cur_image(cur_image=='#') = 1;
        cur_image(cur_image=='+') = 1;%cur_image is the 28x28 matrix of 1 or 0
        cur_image(cur_image==' ') = 0;
        p_3 = double(cur_image) + p_3;
        count_3= count_3+1;
    end 
    
    if (s(k).label == 4)
        cur_image = s(k).image;
        cur_image(cur_image=='#') = 1;
        cur_image(cur_image=='+') = 1;
        cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
        p_4 = double(cur_image) + p_4;
        count_4= count_4+1;
    end  
    
    if (s(k).label == 5)
        cur_image = s(k).image;
        cur_image(cur_image=='#') = 1;
        cur_image(cur_image=='+') = 1;
        cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
        p_5 = double(cur_image) + p_5;
        count_5= count_5+1;
    end    
    
    if (s(k).label == 6)
        cur_image = s(k).image;
        cur_image(cur_image=='#') = 1;
        cur_image(cur_image=='+') = 1;%cur_image is the 28x28 matrix of 1 or 0
        cur_image(cur_image==' ') = 0;
        p_6 = double(cur_image) + p_6;
        count_6= count_6+1;
    end
    
    if (s(k).label == 7)
        cur_image = s(k).image;
        cur_image(cur_image=='#') = 1;
        cur_image(cur_image=='+') = 1;
        cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
        p_7 = double(cur_image) + p_7;
        count_7= count_7+1;
    end
    
    if (s(k).label == 8)
        cur_image = s(k).image;
        cur_image(cur_image=='#') = 1;
        cur_image(cur_image=='+') = 1;
        cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
        p_8 = double(cur_image) + p_8;
        count_8= count_8+1;
    end
    
    if (s(k).label == 9)
        cur_image = s(k).image;
        cur_image(cur_image=='#') = 1;
        cur_image(cur_image=='+') = 1;
        cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
        p_9 = double(cur_image) + p_9;
        count_9= count_9+1;
    end
end

k = 0.1; %0.1-10
p_0 = (k+p_0)/(count_0+2*k);
p_1 = (k+p_1)/(count_1+2*k);%p_1 is the probability of getting char(#/+) at each position given class 1
p_2 = (k+p_2)/(count_2+2*k);
p_3 = (k+p_3)/(count_3+2*k);
p_4 = (k+p_4)/(count_4+2*k);
p_5 = (k+p_5)/(count_5+2*k);
p_6 = (k+p_6)/(count_6+2*k);
p_7 = (k+p_7)/(count_7+2*k);
p_8 = (k+p_8)/(count_8+2*k);
p_9 = (k+p_9)/(count_9+2*k);

%% testing
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
lowest_0 = 10000;
lowest_1 = 10000;
lowest_2 = 10000;
lowest_3 = 10000;
lowest_4 = 10000;
lowest_5 = 10000;
lowest_6 = 10000;
lowest_7 = 10000;
lowest_8 = 10000;
lowest_9 = 10000;
highest_0 = -10000;
highest_1 = -10000;
highest_2 = -10000;
highest_3 = -10000;
highest_4 = -10000;
highest_5 = -10000;
highest_6 = -10000;
highest_7 = -10000;
highest_8 = -10000;
highest_9 = -10000;
for k = 1:1000
    cur_image = s_test(k).image;
    cur_image(cur_image=='#') = 1;
    cur_image(cur_image=='+') = 1;
    cur_image(cur_image==' ') = 0;%cur_image is the 28x28 matrix of 1 or 0
    cur_image = double(cur_image);
    
    p_0_char = p_0.*cur_image;
    p_0_char(p_0_char==0) = 1;
    p_0_nonchar = (1-p_0).*(~cur_image);
    p_0_nonchar(p_0_nonchar==0) = 1;
    test_result(k,1)=log(count_0/5000)+sum(sum(log(p_0_char)))+sum(sum(log(p_0_nonchar)));
    if (s_test(k).label==0)%if this image is label 0
        if(sum(sum(log(p_0_char)))+sum(sum(log(p_0_nonchar)))<lowest_0)
            lowest_0 = sum(sum(log(p_0_char)))+sum(sum(log(p_0_nonchar)));
            lowest_image_0 = k;
        end 
        if(sum(sum(log(p_0_char)))+sum(sum(log(p_0_nonchar)))>highest_0)
            highest_0 = sum(sum(log(p_0_char)))+sum(sum(log(p_0_nonchar)));
            highest_image_0 = k;
        end
    end 
    
    p_1_char = p_1.*cur_image;
    p_1_char(p_1_char==0) = 1;
    p_1_nonchar = (1-p_1).*(~cur_image);
    p_1_nonchar(p_1_nonchar==0) = 1;
    test_result(k,2)=log(count_1/5000)+sum(sum(log(p_1_char)))+sum(sum(log(p_1_nonchar)));
    if (s_test(k).label==1)
    if(sum(sum(log(p_1_char)))+sum(sum(log(p_1_nonchar)))<lowest_1)
        lowest_1 = sum(sum(log(p_1_char)))+sum(sum(log(p_1_nonchar)));
        lowest_image_1 = k;
    end
    if(sum(sum(log(p_1_char)))+sum(sum(log(p_1_nonchar)))>highest_1)
        highest_1 = sum(sum(log(p_1_char)))+sum(sum(log(p_1_nonchar)));
        highest_image_1 = k;
    end
    end 
    
    p_2_char = p_2.*cur_image;
    p_2_char(p_2_char==0) = 1;
    p_2_nonchar = (1-p_2).*(~cur_image);
    p_2_nonchar(p_2_nonchar==0) = 1;
    test_result(k,3)=log(count_2/5000)+sum(sum(log(p_2_char)))+sum(sum(log(p_2_nonchar)));
    if (s_test(k).label==2)
    if(sum(sum(log(p_2_char)))+sum(sum(log(p_2_nonchar)))<lowest_2)
        lowest_2 = sum(sum(log(p_2_char)))+sum(sum(log(p_2_nonchar)));
        lowest_image_2 = k;
    end
    if(sum(sum(log(p_2_char)))+sum(sum(log(p_2_nonchar)))>highest_2)
        highest_2 = sum(sum(log(p_2_char)))+sum(sum(log(p_2_nonchar)));
        highest_image_2 = k;
    end    
    end
        
    p_3_char = p_3.*cur_image;
    p_3_char(p_3_char==0) = 1;
    p_3_nonchar = (1-p_3).*(~cur_image);
    p_3_nonchar(p_3_nonchar==0) = 1;
    test_result(k,4)=log(count_3/5000)+sum(sum(log(p_3_char)))+sum(sum(log(p_3_nonchar)));
    if (s_test(k).label==3)
    if(sum(sum(log(p_3_char)))+sum(sum(log(p_3_nonchar)))<lowest_3)
        lowest_3 = sum(sum(log(p_3_char)))+sum(sum(log(p_3_nonchar)));
        lowest_image_3 = k;
    end
    if(sum(sum(log(p_3_char)))+sum(sum(log(p_3_nonchar)))>highest_3)
        highest_3 = sum(sum(log(p_3_char)))+sum(sum(log(p_3_nonchar)));
        highest_image_3 = k;
    end
    end
    
    p_4_char = p_4.*cur_image;
    p_4_char(p_4_char==0) = 1;
    p_4_nonchar = (1-p_4).*(~cur_image);
    p_4_nonchar(p_4_nonchar==0) = 1;
    test_result(k,5)=log(count_4/5000)+sum(sum(log(p_4_char)))+sum(sum(log(p_4_nonchar)));
    if (s_test(k).label==4)
    if(sum(sum(log(p_4_char)))+sum(sum(log(p_4_nonchar)))<lowest_4)
        lowest_4 = sum(sum(log(p_4_char)))+sum(sum(log(p_4_nonchar)));
        lowest_image_4 = k;
    end
    if(sum(sum(log(p_4_char)))+sum(sum(log(p_4_nonchar)))>highest_4)
        highest_4 = sum(sum(log(p_4_char)))+sum(sum(log(p_4_nonchar)));
        highest_image_4 = k;
    end
    end
    
    p_5_char = p_5.*cur_image;
    p_5_char(p_5_char==0) = 1;
    p_5_nonchar = (1-p_5).*(~cur_image);
    p_5_nonchar(p_5_nonchar==0) = 1;
    test_result(k,6)=log(count_5/5000)+sum(sum(log(p_5_char)))+sum(sum(log(p_5_nonchar)));
    if (s_test(k).label==5)
    if(sum(sum(log(p_5_char)))+sum(sum(log(p_5_nonchar)))<lowest_5)
        lowest_5 = sum(sum(log(p_5_char)))+sum(sum(log(p_3_nonchar)));
        lowest_image_5 = k;
    end
    if(sum(sum(log(p_5_char)))+sum(sum(log(p_5_nonchar)))>highest_5)
        highest_5 = sum(sum(log(p_5_char)))+sum(sum(log(p_5_nonchar)));
        highest_image_5 = k;
    end    
    end
    
    p_6_char = p_6.*cur_image;
    p_6_char(p_6_char==0) = 1;
    p_6_nonchar = (1-p_6).*(~cur_image);
    p_6_nonchar(p_6_nonchar==0) = 1;
    test_result(k,7)=log(count_6/5000)+sum(sum(log(p_6_char)))+sum(sum(log(p_6_nonchar)));
    if (s_test(k).label==6)
    if(sum(sum(log(p_6_char)))+sum(sum(log(p_6_nonchar)))<lowest_6)
        lowest_6 = sum(sum(log(p_6_char)))+sum(sum(log(p_6_nonchar)));
        lowest_image_6 = k;
    end
    if(sum(sum(log(p_6_char)))+sum(sum(log(p_6_nonchar)))>highest_6)
        highest_6 = sum(sum(log(p_6_char)))+sum(sum(log(p_6_nonchar)));
        highest_image_6 = k;
    end
    end
    
    p_7_char = p_7.*cur_image;
    p_7_char(p_7_char==0) = 1;
    p_7_nonchar = (1-p_7).*(~cur_image);
    p_7_nonchar(p_7_nonchar==0) = 1;
    test_result(k,8)=log(count_7/5000)+sum(sum(log(p_7_char)))+sum(sum(log(p_7_nonchar)));
    if (s_test(k).label==7)
    if(sum(sum(log(p_7_char)))+sum(sum(log(p_7_nonchar)))<lowest_7)
        lowest_7 = sum(sum(log(p_7_char)))+sum(sum(log(p_7_nonchar)));
        lowest_image_7 = k;
    end
    if(sum(sum(log(p_7_char)))+sum(sum(log(p_7_nonchar)))>highest_7)
        highest_7 = sum(sum(log(p_7_char)))+sum(sum(log(p_7_nonchar)));
        highest_image_7 = k;
    end
    end
    
    p_8_char = p_8.*cur_image;
    p_8_char(p_8_char==0) = 1;
    p_8_nonchar = (1-p_8).*(~cur_image);
    p_8_nonchar(p_8_nonchar==0) = 1;
    test_result(k,9)=log(count_8/5000)+sum(sum(log(p_8_char)))+sum(sum(log(p_8_nonchar))); 
    if (s_test(k).label==8)
    if(sum(sum(log(p_8_char)))+sum(sum(log(p_8_nonchar)))<lowest_8)
        lowest_8 = sum(sum(log(p_8_char)))+sum(sum(log(p_8_nonchar)));
        lowest_image_8 = k;
    end
    if(sum(sum(log(p_8_char)))+sum(sum(log(p_8_nonchar)))>highest_8)
        highest_8 = sum(sum(log(p_8_char)))+sum(sum(log(p_8_nonchar)));
        highest_image_8 = k;
    end
    end
    
    p_9_char = p_9.*cur_image;
    p_9_char(p_9_char==0) = 1;
    p_9_nonchar = (1-p_9).*(~cur_image);
    p_9_nonchar(p_9_nonchar==0) = 1;
    test_result(k,10)=log(count_9/5000)+sum(sum(log(p_9_char)))+sum(sum(log(p_9_nonchar)));  
    if (s_test(k).label==9)
    if(sum(sum(log(p_9_char)))+sum(sum(log(p_9_nonchar)))<lowest_9)
        lowest_9 = sum(sum(log(p_9_char)))+sum(sum(log(p_9_nonchar)));
        lowest_image_9 = k;
    end
    if(sum(sum(log(p_9_char)))+sum(sum(log(p_9_nonchar)))>highest_9)
        highest_9 = sum(sum(log(p_9_char)))+sum(sum(log(p_9_nonchar)));
        highest_image_9 = k;
    end
    end
end 

[value index] = max(test_result');
predict_label = index -1;

accuracy_total = sum(test_label==predict_label')/1000;



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


%% odds ratio
% max confusion matrix ratio are: 9-4 8-3 9-7 3-5
imagesc(log(p_8));
colormap(jet);

imagesc(log(p_9)-log(p_4));
colormap(jet);