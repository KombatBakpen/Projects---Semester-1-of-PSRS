clear; close all; clc;
% Written by Bakpen Kombat. 
image_folder = 'images/';
ground_truth_folder = 'Ground_truth/';
image_files = dir([image_folder, '*.bmp']);

total_similarity = 0;
num_images = min(numel(image_files), 600); % Process only 10 images

for i = 1:num_images
    img_name = image_files(i).name;
    img1 = imread(fullfile(image_folder, img_name));
    img2 = imread(fullfile(ground_truth_folder, strrep(img_name, '.bmp', '.png')));
    
    % Gaussian filtering
    filter_size = 5; % Define the filter size for the Gaussian filter
    sigma = 1; % Define the standard deviation for the Gaussian filter
    img1_filtered = imgaussfilt(img1, sigma, 'FilterSize', filter_size); % Apply Gaussian filtering to the image
    
    threshold = 90;
    img_bw = img1_filtered < threshold;
    img2_bw = img2 > 0; % Convert to binary (assuming Ground_truth image has non-zero values for the region of interest)
    
    % Morphological treatment (example: using dilation)
    SE = strel('disk', 3); % Define a disk-shaped structuring element for dilation
    img_bw_processed = imdilate(img_bw, SE); % Perform dilation on the processed image
    
    % Calculate intersection and union with processed image
    intersection = img_bw_processed & img2_bw;
    union = img_bw_processed | img2_bw;

    % Calculate IoU (Intersection over Union)
    result = sum(intersection(:)) / sum(union(:));
    
    total_similarity = total_similarity + result;
end

average_similarity = total_similarity / num_images;
fprintf('for the first %d images after l treatment: %.4f\n', num_images, average_similarity);

