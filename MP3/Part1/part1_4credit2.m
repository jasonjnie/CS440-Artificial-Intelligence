%disjoint patches

%patch size
p_x = 2;
p_y = 2;
%feature image size
x = 14;
y = 14;
%% 
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


for k = 1:5000
    modify_image = cell([x,y]);    
    cur_image = s(k).image;
    cur_image(cur_image=='#') = 1;
    cur_image(cur_image=='+') = 1;
    cur_image(cur_image==' ') = 0;
    image = double(cur_image);%each image is now stored in either 1 or 0 at each pixel 
    for l = 1:x
        for m = 1:y
            arr = [];
            for c = 0:(p_x-1)
                for d = 0:(p_y-1)
                    arr = [arr image(p_x*l-(p_x-1)+c,p_y*m-(p_y-1)+d)];
                end 
            end
            modify_image{l,m} = arr;
        end 
    end 
    
    s(k).image = modify_image;%modif_image is 14x14, each cell is a vector of 4 values
end 

%% training:
prob = zeros(10,x,y,2^(p_x*p_y));%10 class * modified image * features values
count = zeros(10);
for k = 1:5000
    i = s(k).label;
    i = i+1;%indicates the class number
    count(i) = count(i) + 1; %number of class i
    
    cur_image = s(k).image;
    for m = 1:x
        for n = 1:y
            % to get the [,,,,] represented number
            j=bi2de(cur_image{m,n})+1;           
            prob(i,m,n,j) = prob(i,m,n,j) +1;%given particular class i, the number of particular [,,,,] that pixel position gets
        end 
    end 
end 

k=0.1;
for i = 1:10
    for j = 1:2^(p_x*p_y)
    prob(i,:,:,j) = (k+prob(i,:,:,j))/(count(i)+2*k);%prob(i,:,:,j) is the probability in shape of [14x14] image; 
    %probability of each pixel being j feature value, given class i
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

modify_image = cell([x,y]);
for k = 1:1000
    cur_image = s_test(k).image;
    cur_image(cur_image=='#') = 1;
    cur_image(cur_image=='+') = 1;
    cur_image(cur_image==' ') = 0;
    image = double(cur_image);%each image is now stored in either 1 or 0 at each pixel 
    for l = 1:x
        for m = 1:y
            arr = [];
            for c = 0:(p_x-1)
                for d = 0:(p_y-1)
                    arr = [arr image(p_x*l-(p_x-1)+c,p_y*m-(p_y-1)+d)];
                end 
            end
            modify_image{l,m} = arr;
        end 
    end
    s_test(k).image = modify_image;%modif_image is 14x14, each cell is a vector of 4 values
end 

%%%%%%%%%%%%%%%%

test_result = zeros(1000,10);
%prob = zeros(10,14,14,16);%10 class * modified image * features values
for k = 1:1000
    
    for i = 1:10 
    
        cur_image = s_test(k).image;%????test image???pixel?????feature value?
        
        for m = 1:x
            for n = 1:y
                j=bi2de(cur_image{m,n})+1;  
                test_result(k,i) = test_result(k,i) + log(prob(i,m,n,j));%given particular class i, the number of particular [,,,,] that pixel position gets
            end 
        end
        
        test_result(k,i) = log(count(i)/5000)+test_result(k,i);
    
    end

end 


[value index] = max(test_result');
predict_label = index -1;

accuracy_total = sum(test_label==predict_label')/1000;
