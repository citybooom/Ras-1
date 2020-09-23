clear; 
clc;

fileID = fopen('Sensor18_x7_y1.5.txt','r');
formatSpec = '%f %f %f %f %f %f %f %f %f';
A = textscan(fileID, formatSpec, 'Delimiter', {'*'});
Data = cell2mat(A);

justTheData = Data(:,2:9);

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
plot(1:size(Data,1),Data(:,i+1))
hold on
end


pulses = ceil(length(Data)/333);

mini = min(min(justTheData));
maxi = max(max(justTheData));
slope = zeros(pulses,8);
displacements = zeros(pulses,8);
values = zeros(6,8);
xspace = (1:1:300)';
yfit = zeros(300,8);
fits = cell(1,8);

for i = 1:pulses
    for j = 1:8
        center = 150 + (333*(i-1));
        startpoint = center - 80;
        endpoint  = center + 80;
        slope(i,j) = (mean(justTheData(endpoint-5:endpoint+5,j)) - mean(justTheData(startpoint-5:startpoint+5,j)))/160;
        line([startpoint endpoint],[ mean(justTheData(startpoint-5:startpoint+5,j)) (mean(justTheData(endpoint-5:endpoint+5,j)))],'LineWidth',1)
        if i == 1 
            yfit(:,j) = justTheData(1:300,j);
            fits{j} = fit(xspace,yfit(:,j),'poly1');
            plot((1:1:lineCount), fits{j}(1:1:lineCount));
%             line([0 length(Data)],[ startvalues(j) startvalues(j) + slope(1,j)*length(Data)],'LineWidth',1)
        end
    end
    
end

for i = 1:pulses
    for j = 1:8
    displacements(i,j) = slope(1,j)*(167+333*(i-1));
    end
end

fitvals = zeros(1,8);

for i = 1:pulses
    line([167+333*(i-1) 167+333*(i-1)],[mini maxi],'LineWidth',1) 
    for j = 1:8
        fitvals(j) = fits{j}(167+333*(i-1));
    end
    value = mean(justTheData(167+333*(i-1)-5:167+333*(i-1)+5,:)) - fitvals;
%    value = mean(justTheData(167+333*(i-1)-5:167+333*(i-1)+5,:)) - (startvalues + displacements(i,:));
    values(i,:) = value;
end



% 
% f1 = fit(xspace,yfit,'poly2');
% 
% plot((1:1:lineCount), f1(1:1:lineCount));

grid minor;
lgd = legend("1", "2","3", "4", "5", "6", "7", "8");
title(lgd, "Channel No.")
ylabel('Voltage Reading (mV)')
title('Force Baseline Test: Sensor15 Pos3 Take2')


figure 


for i = 0:2:pulses
    values(pulses-i,:) = [];
end

plot(values,'LineWidth',1)