
files2read = cell(30,1);
for c = 0:1:4
    for d = 0:1:5 
        files2read{c*6+d+1} = strcat(strcat("SensorB3_x", num2str(6+c)),"_y");
        files2read{c*6+d+1} = strcat(strcat(files2read{c*6+d+1}, num2str(d)),"_Take4.txt");
    end
end

slopearray = zeros(8,30);
finalslopes = zeros(8,length(files2read));

for k = 1:length(files2read)

    fileID = fopen(files2read{k},'r');
    formatSpec = '%f %f %f %f %f %f %f %f %f';
    A = textscan(fileID, formatSpec, 'Delimiter', {'*'});
    Data = cell2mat(A);

    justTheData = Data(:,2:9);
    
%     for i = 1:length(justTheData)
%         for j = 1:length(justTheData(1,:))
%             justTheData(i,j) = -470*(justTheData(i,j) - 3300)/justTheData(i,j);
%         end
%     end

    MatNum = 0;
    DelimiterLine = [];


    for lineCount = 1:size(Data,1)
        if isnan(Data(lineCount,1)) == 1
            MatNum = MatNum + 1;
            DelimiterLine = [DelimiterLine, lineCount];
        end
    end

    startvalues = zeros(1,8);



    for i = 1:8

    startvalues(i) = mean(justTheData(1:3,i));
    %plot(1:size(Data,1),Data(:,i+1))
%     hold on
    end


    pulses = ceil(length(Data)/333);

    mini = min(min(justTheData));
    maxi = max(max(justTheData));
    slope = zeros(4,8);
    displacements = zeros(pulses,8);
    values = zeros(6,8);
    xspace = [(100:1:300) (766:1:966) (1432:1:1632) (2100:1:2150)]';
    yfit = zeros(654,8);
    fits = cell(1,8);
    
    justTheFiltered = justTheData;
    justTheFiltered(:,5) = [];
    justTheFiltered(:,4) = [];

    datasum = zeros(length(justTheFiltered),1);

    for i = 1:length(justTheFiltered(1,:))
        datasum = datasum + justTheFiltered(:,i);  
    end

    common_noise = highpass(datasum/length(justTheFiltered(1,:)),0.0000001);

    for i = 1:length(justTheFiltered(1,:))
        justTheFiltered(:,i) = justTheFiltered(:,i) - common_noise;  
    end

%     hold off
%     subplot(2,1,1);
%     plot(justTheFiltered)
%     subplot(2,1,2);
%     plot(common_noise)

    for i = 1:3
        for j = 1:length(justTheFiltered(1,:))
            center = -20 + (400*(i));
            startpoint = center - 100;
            endpoint  = center + 100;
            slope(i,j) = (mean(justTheFiltered(endpoint-10:endpoint+10,j)) - mean(justTheFiltered(startpoint-10:startpoint+10,j)));
        end

    end

    
    %slopechange =  (slope(3,:)+slope(2,:)+slope(1,:))/3; 
    slopechange = slope(2,:);
    slopearray(:,k) = slopechange;
  

end
% 



slopecorrect = slopearray';
measure_ratios = zeros(30,length(justTheFiltered(1,:)));

%hold on
matcharray = zeros(30,30);


for i = 1:30
   for j = 1:length(justTheFiltered(1,:))
       measure_ratios(i,j) = slopecorrect(i,j)/mean((abs(slopecorrect(i,:))));
   end    
end


%error_slopes = (measure_ratios - square_ratios);

for k = 1:30
    for i = 1:30
        for j = 1:length(justTheFiltered(1,:))
            matcharray(i,k) = matcharray(i,k) + abs(square_ratios_alt(i,j) - measure_ratios(k,j));
        end
    end
end

estimate = zeros(30,1);
errors  = zeros(30,1);
for i = 1:30
    mini = matcharray(1,i);
    %min_1 = matcharray(i,2);
    mindex = 1;
    %mindex_1 = 2;
    for j = 2:30
        if abs(matcharray(j,i)) < abs(mini)
            %min_1 = mini;
            %mindex_1 = mindex;
            mini = matcharray(j,i);
            mindex = j;
        end
    end
    estimate(i) = mindex;
    errors(i) = mod(abs(estimate(i) - i),6) + rem(abs(estimate(i) - i),6);
end

% disp(mean(mean(slopecorrect ./ measure_ratios)));


hold on
plot(square_ratios,'k')
plot(measure_ratios)

%square_ratios_4 = measure_ratios;
%hold off

%figure;

% for i = 1:30
%     error_slopes(i,8) = sum(error_slopes(i,:));
% end

%plot(error_slopes,'LineWidth',1)



% ratios = zeros(11,7);
% for i = 1:11
%    for j = 1:7
%        ratios(i,j) = target(i,j)/mean(abs((target(i,:))));
%     end    
% end

