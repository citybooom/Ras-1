
fileID = fopen('Test15_C2.txt','r');
formatSpec = '%f %f %f %f %f %f %f %f %f';
A = textscan(fileID, formatSpec, 'Delimiter', {'*'});
Data = cell2mat(A);
 

justTheData = Data(:,2:9);
%justTheFiltered = lowpass(justTheData,0.01);
justTheFiltered = justTheData;

% for i = 1:length(justTheData)
%     for j = 1:length(justTheData(1,:))
%         justTheData(i,j) = 47*(10*justTheData(i,j)-33)/(justTheData(i,j));
%     end
% end
    
%B = arrayfun(func,A)

%justTheFiltered = justTheData;

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
startvalues(i) = mean(justTheFiltered(1:3,i));
%plot(justTheFiltered)
hold on
end


mini = min(min(justTheFiltered));
maxi = max(max(justTheFiltered));
slope = zeros(5,8);
displacements = zeros(5,8);
values = zeros(6,8);
xspace = [(100:1:300) (766:1:966) (1432:1:1632) (2100:1:2150)]';
yfit = zeros(654,8);
fits = cell(1,8);

justTheFiltered(:,5) = [];

datasum = zeros(length(justTheFiltered),1);

for i = 1:length(justTheFiltered(1,:))
    datasum = datasum + justTheFiltered(:,i);  
end

common_noise = highpass(datasum/length(justTheFiltered(1,:)),0.0000001);

for i = 1:length(justTheFiltered(1,:))
    justTheFiltered(:,i) = justTheFiltered(:,i) - common_noise;  
end

hold off
subplot(2,1,1);
plot(justTheFiltered)
subplot(2,1,2);
plot(common_noise)

for i = 1:3
    for j = 1:7
        center = -30 + (400*(i));
        startpoint = center - 100;
        endpoint  = center + 100;
        slope(i,j) = (mean(justTheFiltered(endpoint-10:endpoint+10,j)) - mean(justTheFiltered(startpoint-10:startpoint+10,j)));
    end
    
end
slope(1,:) = slope(1,:) / 100;
slope(2,:) = slope(2,:) / 200;
slope(3,:) = slope(3,:) / 300;
slope(4,:) = slope(4,:) / 400;
slope(5,:) = slope(5,:) / 500;


% 
% hold on
% plot(slope)
% axis([1,3,-150,250])
% 
% hold off

% 
% for i = 1:pulses
%     for j = 1:8
%     displacements(i,j) = slope(1,j)*(167+333*(i-1));
%     end
% end
% 
% fitvals = zeros(1,8);
% 
% for i = 1:pulses
%     line([167+333*(i-1) 167+333*(i-1)],[mini maxi],'LineWidth',1) 
%     for j = 1:8
%         fitvals(j) = fits{j}(167+333*(i-1));
%     end
%     value = mean(justTheFiltered(167+333*(i-1)-5:167+333*(i-1)+5,:)) - fitvals;
%    value = mean(justTheFiltered(167+333*(i-1)-5:167+333*(i-1)+5,:)) - (startvalues + displacements(i,:));
%     values(i,:) = value;
% end
% 
% 
% 
% 
% f1 = fit(xspace,yfit,'poly2');
% 
% plot((1:1:lineCount), f1(1:1:lineCount));
% 
% grid minor;
% lgd = legend("1", "2","3", "4", "5", "6", "7", "8");
% title(lgd, "Channel No.")
% ylabel('Voltage Reading (mV)')
% title('Sensor32_x5_y_Trial2')
% 
% 
% figure 
% 
% 
% for i = 0:2:pulses
%     values(pulses-i,:) = [];
% end
% 
% plot(values,'LineWidth',1)
% 
% 
% function res = restovolt(volt)
%     res = 4700*volt/(33-10*volt); 
% end