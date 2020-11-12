A = fileread("Single_data_C1_30.txt");
count = 1;
lasti = 1;
lineArray = ["Start"];

for i = (10000:length(A))
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


dataCache = [];
for i = (2:length(dataArray))
    dataCache = cat(1, dataCache, dataArray{i});
end

Reading = zeros(8,1);
BaselineData = dataCache(length(dataCache) - 10:length(dataCache),:);
Baselines = mean(BaselineData);
Peak = max(dataCache);
Trough = min(dataCache);
for k = 1:8
    if(abs(Peak(k) - Baselines(k)) > abs(Trough(k) - Baselines(k)))
        Reading(k) = Peak(k) - Baselines(k);
    else
        Reading(k) = Trough(k) - Baselines(k);
    end
end

Ratios = zeros(8,1);

average = 0;
for k = 1:8
   average = average + Reading(k)/8;
end
for k = 1:8
   Ratios(k) = Reading(k)/average;
end

Visual = zeros(10,24);

for i = 1:10
    for j = 1:24
        match = 0;
        for k = 1:8
             match = match + abs(Ratios(k) - golden_ratio(i,j,k));
        end
        Visual(i,j) = match;
    end
end

surf(Visual);
axis equal

