clear
close all;

%% loading bvh file
[FileName,PathName] = uigetfile('*.bvh*','Select a Image file');
File = fullfile('',FileName); 
[skel, channels, frameLength] = bvhReadFile(File);

%% reduce the channels using PCA
[coeff, score]=pca(channels);

%% plot the 3D scatter plots based on score
figure(1);
scatter3(score(:, 1), score(:, 2), score(:,3));

%% calculating the distance between root and joints
distance = zeros(1147,37);
for frames = 1:1147
    points = bvh2xyz(skel, channels(frames, :));
    for joints = 2:38
        distance(frames, joints-1) = pdist2(points(1, :), points(joints,:));
    end
end

%% reduce the matrix using PCA
pcaDistance = pca(distance);

%% plot the 3D scatter plots based on pcaDistance
figure(2);
scatter3(pcaDistance(:, 1), pcaDistance(:, 2), pcaDistance(:, 3));