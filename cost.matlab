%%data, the orginal data contains 3d points 

%%%%%%%%%%%%%%%%%loop body of a for loop which run kmeans from k = 1 to k = 10
sum = 0
for frames = 1:ch_row	
    points = bvh2xyz(skel, channels(frames, :));
    for joints = 1:num_joints
    	sum += pdist2(points(joints,:), ch_centroid(ch_labels(frames,:),:));%% compare each node position with centroid
    end
end

%%%%%%%%%%%%%%%%%