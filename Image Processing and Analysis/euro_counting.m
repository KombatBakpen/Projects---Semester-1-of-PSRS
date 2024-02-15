clear; close all; clc;

%% ||Euros counting project|| by Bakpen Kombat and Deborah Adingu||

%% Dataset
image = ["euros6.bmp", "euros7.bmp", "euros8.bmp", "euros9.bmp", "euros10.bmp"];

%% Counting the total number of coins and amount
counts = [];
allTotalAmounts = [];
allNbs = [];
for i = 1:numel(image)
    [count, total_amount, nb] = detect_Coins(image{i});
    counts(:, i) = count; % Store results column by column
    allTotalAmounts(i) = total_amount;
    allNbs(i) = nb;
end
%% Saving into a database 

columnNames = {'Files', '1 cent','2 cents','10 cents','5 cents','20 cents', '1 euro','50 cents', '2 euros'};

columnNames{end+1} = 'Total Amount';
columnNames{end+1} = 'Number of Coins';
resultTable = array2table([image; counts; allTotalAmounts; allNbs].', 'VariableNames', columnNames);

csvFileName = 'database.csv'; % file name; database
writetable(resultTable, csvFileName);

disp(['Results saved to ' csvFileName]);

%% Function for Preproposing 
%%
function [count, total_amount, nb] = detect_Coins(imageName) 
   %% Reading and converting the image image to gray scale
    img_rgb = imread(imageName);
    img = rgb2gray(img_rgb);
%% Apply a median filter on each image
   img = medfilt2(img, [3, 3]);
    figure('Name', 'Processing until labelling');
    subplot(2, 2, 1);
    imshow(img);
     %% Thresholding
    threshold = 70;
    img_1 = img > threshold;
    imshow(img_1);
    
    %% Fill the holes in images
    img_fill = imfill(img_1, 'holes');
    subplot(2, 2, 2);
    imshow(img_fill);
    
    %% Morphology (Erosion)
    SE = strel('disk', 11);
    img_erode = imerode(img_fill, SE);
    subplot(2, 2, 3);
    imshow(img_erode); title('Mophological pretreatement: Erosion');
    
    %% Labelling
    [img_2, nb] = bwlabel(img_erode);
    img_label = label2rgb(img_2, 'jet', [0, 0, 0]);
    subplot(2, 2, 4);
    imshow(img_label); title ('Labelled Image');
    
   %% Signature: computing the area of the images 
    label = regionprops(img_2, 'Centroid');
    org_centroids = cat(1, label.Centroid);
    %% K-MEANS Clustering 

    feature_vec = regionprops(img_2, 'Area', 'Centroid'); 
    areas = [feature_vec.Area];
    k = 8;
    [idx, centroids] = kmeans(areas', k);

    %% Calculates average areas for each cluster
    cluster_averages = zeros(k, 1); 
    for i = 1:k
        cluster_averages(i) = mean(areas(idx == i));
    end
    
    %% Create a list of cluster indices and their corresponding average areas
    cluster_info = [(1:k)', cluster_averages];
    
    %% Sorting the list based on average areas
    sorted_cluster_info = sortrows(cluster_info, 2);
    
    %% Extract the sorted cluster indices
    sorted_idx = idx;
    for i = 1:k
        sorted_idx(idx == sorted_cluster_info(i, 1)) = i;
    end
  %% Label the RGB images based on their denominations using colormap
   
    cmap = jet(k);
    colored_img_label = img_rgb;
    
    denominations = ["1 cent", "2 cents", "10 cents", "5 cents", "20 cents", "1 euro", "50 cents", "2 euros"];
    amount = [0.01, 0.02, 0.1, 0.05, 0.2, 1, 0.5, 2];
    count = zeros(1, 8);
    total_amount = 0;
    for i = 1:nb
        label_indices = (img_2 == i);
        cluster_index = sorted_idx(i);
        count(cluster_index) = count(cluster_index) + 1;
        colored_img_label = insertText(colored_img_label, [org_centroids(i, 1) - 3, org_centroids(i, 2) - 3], denominations(cluster_index), 'FontSize', 15);
    end
    
    figure;
    imshow(colored_img_label);
    title('Colored Labels Based on Clusters');
    %% Counting the total number of coins in each images and total amount 
    for i = 1:8
        disp("No of " + denominations(i) + " is: " + count(i));
        total_amount = total_amount + (amount(i) * count(i));
    end
    
    disp("Total no of coins is: " + nb);
    disp("Total amount is: " + total_amount);
end


