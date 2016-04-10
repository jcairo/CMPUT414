clear
close all;

%% loading bvh file
[FileName,PathName] = uigetfile('*.bvh*','Select a Image file');
File = fullfile('',FileName); 
[skel, channels, frameLength] = bvhReadFile(File);

%% get the number of rows in channels and joints
%  set the number of clusters
ch_row = size(channels, 1);
num_joints = size(skel.tree, 2);
ch_kmean = 4;
dis_kmean = 4;

%% reduce the channels using PCA
[coeff, score] = pca(channels);

%% get the kmeans for channels
[ch_labels, ch_centroid] = kmeans(channels, ch_kmean);

%% plot the 3D scatter plots based on score
figure(1);
scatter3(score(:, 1), score(:, 2), score(:,3));

%% calculating the distance between root and joints
distance = zeros(ch_row,num_joints-1);
for frames = 1:ch_row
    points = bvh2xyz(skel, channels(frames, :));
    for joints = 2:num_joints
        distance(frames, joints-1) = pdist2(points(1, :), points(joints,:));
    end
end

%% reduce the matrix using PCA
pcaDistance = pca(distance);

%% get the kmean for distance
[dis_labels, dis_centroid] = kmeans(distance, dis_kmean);

%% plot the 3D scatter plots based on pcaDistance
figure(2);
scatter3(pcaDistance(:, 1), pcaDistance(:, 2), pcaDistance(:, 3));

%% plot the clutering against time frames
figure(3);
plot(ch_labels);

figure(4);
plot(dis_labels);

%% cost function, first draft, it is not fully intergated.
%%this constant should be trained base on the average cost domin range.
%%the idea is to convert the orginal cost graph(1/x shaped) to a (x+1/x shaped) graph
%%there will definately be a bottom of the graph, and we believe that that's gonna be the k value we need.
%%the advantage compared with the elbow problem is that this function(if works) will be 
%%easier to be determined by a machine
magicalconstant = 42;
costarray = zeros(1, 10);
for kvalue = 1: 10
%% since we are dealing with small motion
    [ch_labels, ch_centroid] = kmeans(channels, kvalue);
    total = 0;
    for frames = 1:ch_row	
        points = bvh2xyz(skel, channels(frames, :));
        for joints = 1:9
            %%compare each node position with centroid
        	temp = ch_centroid(kvalue, joints);
            temp = temp/kvalue;
        	%%cost should be sum of equare errors
        	total = total + temp*temp;
        end
    end
    costarray(1, kvalue) = total + magicalconstant*kvalue;
end