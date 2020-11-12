

A = fileread("Test19_C1_beeg.txt");
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
        for k = 1:8
            if(abs(Peak(k) - Baselines(k)) > abs(Trough(k) - Baselines(k)))
                Readings(i,j,k) = Peak(k) - Baselines(k);
            else
                Readings(i,j,k) = Trough(k) - Baselines(k);
            end
        end
    end
end

Ratios = zeros(10,24,8);

for i = 1:length(DataSets(:,1))
    for j = 1:length(DataSets(1,:))
        average = 0;
        for k = 1:8
           average = average + (Readings(i,j,k)/8);
        end
        for k = 1:8
           Ratios(i,j,k) = Readings(i,j,k)/average;
        end    
    end
end

matcharray = zeros(240,240);


for i = 1:10
    for j = 1:24
       for x = 1:10
            for y = 1:24
            match = 0;
                for z = 1:8
                    match = match + abs(Ratios(i,j,z) - golden_ratio(x,y,z));
                end
                matcharray((i-1)*24+j, (x-1)*24+y) = match;
            end
        end
    end
end

estimate = zeros(240,1);
errors  = zeros(240,1);
for i = 1:240
    mini = matcharray(1,i);
    mindex = 1;
    for j = 2:240
        if abs(matcharray(j,i)) < abs(mini)
            mini = matcharray(j,i);
            mindex = j;
        end
    end
    estimate(i) = mindex;
    errors(i) = round((estimate(i) - i)/24);
    errors(i) = errors(i) + (estimate(i) - i )- errors(i)*24;
end

correctcount = 0;
closecount = 0;
for i = 5:240
    if errors(i) == 0
        correctcount = correctcount + 1;
    end
    if errors(i) <= 2
        closecount = closecount + 1;
    end
end

Visual = zeros(10,24);
for i = 1:10
    for j = 1:24
        match = 0;
        for k = 1:8
             match = match + min(0,golden_ratio(i,j,k)- Ratios(i,j,k));
             %match = match + abs(oldratios(i,j,k)- Ratios(i,j,k));
        end
        if(abs(match) < 300000)
            Visual(i,j) = match;
        end
    end
end

ErrorVisual = zeros(10,24);

for i = 1:10
    for j = 1:24
        ErrorVisual(i,j) = errors((i-1)*24 + j);
    end
end
%hold on
surf(ErrorVisual);
% daspect([1 1 10]);

%hold off
% correctcount/235;
% closecount/235;