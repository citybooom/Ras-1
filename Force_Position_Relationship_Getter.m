% clear; 
% clc;

files2read = cell(19,1);

for c = 3.5:0.5:12.5
    files2read{(c-3)*2} = strcat("Sensor32_x5_y", num2str(c));
    files2read{(c-3)*2} = strcat(files2read{(c-3)*2},"_Trial1.txt");
end

finalslopes = zeros(8,length(files2read));

for k = 1:length(files2read)

    fileID = fopen(files2read{k},'r');
    formatSpec = '%f %f %f %f %f %f %f %f %f';
    A = textscan(fileID, formatSpec, 'Delimiter', {'*'});
    Data = cell2mat(A);

    justTheData = Data(:,2:9);
    
    for i = 1:length(justTheData)
        for j = 1:8
            justTheData(i,j) = -470*(justTheData(i,j) - 3300)/justTheData(i,j);
        end
    end

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
    hold on
    end


    pulses = ceil(length(Data)/333);

    mini = min(min(justTheData));
    maxi = max(max(justTheData));
    slope = zeros(pulses,8);
    displacements = zeros(pulses,8);
    values = zeros(6,8);
    xspace = [(100:1:300) (766:1:966) (1432:1:1632) (2100:1:2150)]';
    yfit = zeros(654,8);
    fits = cell(1,8);

    for i = 1:pulses
        for j = 1:8
            center = 150 + (333*(i-1));
            startpoint = center - 30;
            endpoint  = center + 30;
            slope(i,j) = (mean(justTheData(endpoint-5:endpoint+5,j)) - mean(justTheData(startpoint-5:startpoint+5,j)))/600;
            %line([startpoint endpoint],[ mean(justTheData(startpoint-5:startpoint+5,j)) (mean(justTheData(endpoint-5:endpoint+5,j)))],'LineWidth',1)
            if i == 1 
                yfit(:,j) = [justTheData(100:300,j)' justTheData(766:966,j)' justTheData(1432:1632,j)' justTheData(2100:2150,j)']';
                fits{j} = fit(xspace,yfit(:,j),'exp2');
               % plot((1:1:lineCount), fits{j}(1:1:lineCount));
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
        %line([167+333*(i-1) 167+333*(i-1)],[mini maxi],'LineWidth',1) 
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
% 
%     grid minor;
%     lgd = legend("1", "2","3", "4", "5", "6", "7", "8");
%     title(lgd, "Channel No.")
%     ylabel('Voltage Reading (mV)')
%     title('Force Baseline Test: Sensor15 Pos3 Take2')


    %figure 


    for i = 0:2:pulses
        values(pulses-i,:) = [];
    end

    

    for i = 1:8
        finalslopes(i,k) = values(3,i) - values(1,i);
    end

end

plot(finalslopes','LineWidth',1)
lgd = legend("1", "2","3", "4", "5", "6", "7", "8");
%plot(finalslopes(2,:),'LineWidth',1)

