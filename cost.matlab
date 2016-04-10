%%%%%%%%%%%%%%%%%loop body of a for loop which run kmeans from k = 1 to k = 10
[FileName,PathName] = uigetfile('*.bvh*','Select a Image file');
File = fullfile('',FileName); 
[skel, channels, frameLength] = bvhReadFile(File);
magicalconstant = 42
%%this constant should be trained base on the average cost domin range.
%%the idea is to convert the orginal cost graph(1/x shaped) to a (x+1/x shaped) graph
%% there will definately be a bottom of the graph, and we believe that that's gonna be the k value we need.
%%the advantage compared with the elbow problem is that this function(if works) will be 
%%easier to be determined by a machine
%% get the number of rows in channels and joints
%  set the number of clusters
ch_row = size(channels, 1);
num_joints = size(skel.tree, 2);
for kvalue = 1: 10
%%since we are dealing with small motion
    [ch_labels, ch_centroid] = kmeans(channels, kvalue);
    sum = 0
    for frames = 1:ch_row	
        points = bvh2xyz(skel, channels(frames, :));
        for joints = 1:num_joints
        	temp = pdist2(points(joints,:), ch_centroid(ch_labels(frames,:),:));%% compare each node position with centroid
        	sum += temp*temp
        	%% cost should be sum of equare errors
        end
    end
    costarray(1, :) = sum + magicalconstant*kvalue
end
%%%%%%%%%%%%%%%%%
