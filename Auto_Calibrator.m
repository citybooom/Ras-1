
%formatSpec = '%f %f %f %f %f %f %f %f %f';
A = fileread("Test10.txt");
%Data = cell2mat(A);

count = 1;
lasti = 1;
lineArray = ["Start"];
for i = (1:length(A))
    if(A(i) == 13)
        charArray  = A(lasti:i-1);
        cleanedArray = [];
        for j = (1:length(charArray))
            if(charArray(j) > 44 && charArray(j) < 58 || charArray(j) == 32 || charArray(j) == 95 )
                cleanedArray = [cleanedArray charArray(j)];
            end
        end
        if(cleanedArray) 
            lineArray(count) = convertCharsToStrings(cleanedArray);
        end
        count = count + 1;
        lasti = i;
    end
end

dataArray = cell(length(lineArray),1);

for i = (1:length(lineArray))
    dataArray{i} = str2num(strrep(lineArray(i),'_',' '));
end

DataSets = cell(10,24);

first = 1;
pos = dataArray{1};
dataCache = [];
for i = (2:length(dataArray))
    if(length(dataArray{i}) == 2)
        DataSets{pos(1),pos(2)} = dataCache;
        pos = dataArray{i};
        dataCache = [];
    else
        dataCache = cat(1, dataCache, dataArray{i});
    end
end
DataSets{pos(1),pos(2)} = dataCache;

Readings = zeros(10,24,8);

for i = 1:10
    for j = 1:24
        tempdata = DataSets{i,j};
        BaselineData = tempdata(length(tempdata) - 10:length(tempdata),:);
        Baselines = mean(BaselineData);
        Peak = max(DataSets{i,j} );
        Trough = min(DataSets{i,j});
        %if(abs(Peak - Baselines) > abs(Trough - Baselines))
        for k = 1:8
            if(abs(Peak(k) - Baselines(k)) > abs(Trough(k) - Baselines(k)))
                Readings(i,j,k) = Peak(k) - Baselines(k);
            else
                Readings(i,j,k) = Trough(k) - Baselines(k);
            end
        end
        
        %else
           % Readings(i,j,:) = Trough - Baselines;
        %end
    end
end




