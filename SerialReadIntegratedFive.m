clear all

s = serialport("COM3",9600);
s.FlowControl = "none";
buffer = zeros(16,100);
fig3 = figure;
axis([-2.5 2.5 -2.5 2.5]);
x = linspace(1,100,100);
center = [0,0,0,0,0];
radii = [1,2,3,4,5];

pos0 = [-0.5 -0.5 1 1];
pos1 = [-1 -1 2 2];
pos2 = [-1.5 -1.5 3 3];
pos3 = [-2 -2 4 4];
pos4 = [-2.5 -2.5 5 5];



prob0a = zeros(60,1);
[prob0a(10)] = deal(17);
[prob0a(26),prob0a(9),prob0a(11)] = deal(13);  
[prob0a(54),prob0a(27),prob0a(25),prob0a(8),prob0a(12)] = deal(11);
[prob0a(42)] = deal(13);
[prob0a(40),prob0a(24),prob0a(29),prob0a(59)] = deal(4);
[prob0a(28),prob0a(43),prob0a(41)] = deal(8);
[prob0a(53:54)] = deal(6);
[prob0a(44)] = deal(5);
[prob0a(58),prob0a(60)] = deal(3);
[prob0a(55),prob0a(57),prob0a(45)] = deal(2);


[prob0a(1:4)] = deal(-20);
[prob0a(14:16),prob0a(5:7)] = deal(-20);
[prob0a(19:23),prob0a(13)] = deal(-14);
[prob0a(30:32),prob0a(37:39)] = deal(-8);
[prob0a(33:36),prob0a(17:18),prob0a(46:48)] = deal(-6);
[prob0a(50),prob0a(51:52)] = deal(-2);


prob0e = zeros(60,1);

[prob0e(8:9)] = deal(15);
[prob0e(24:25)] = deal(10);
[prob0e(40:41)] = deal(8);
[prob0e(52:53)] = deal(6);
[prob0e(58:59)] = deal(4);
[prob0e(57),prob0e(60)] = deal(-4);


prob0b = zeros(60,1);
for i = 1:16
    prob0b(i) = prob0a(17-i);
end
for i = 17:32
    prob0b(i) = prob0a(16 + 33 - i);
end
for i = 33:48
    prob0b(i) = prob0a(32 + 49 - i);
end
for i = 49:56
    prob0b(i) = prob0a(48 + 57 - i);
end
for i = 57:60
    prob0b(i) = prob0a(56 + 61 - i);
end


prob3b = zeros(60,1);
for i = 1:15
    prob3b(boundadd(i,4,1,16)) = prob0a(i);
end
for i = 16:31
    prob3b(boundadd(i,4,17,32)) = prob0a(i);
end
for i = 32:47
    prob3b(boundadd(i,4,33,48)) = prob0a(i);
end
for i = 49:56
    prob3b(boundadd(i,2,49,56)) = prob0a(i);
end
for i = 57:60
    prob3b(boundadd(i,1,57,60)) = prob0a(i);
end

prob2c = zeros(60,1);
for i = 1:15
    prob2c(boundadd(i,8,1,16)) = prob0a(i);
end
for i = 16:31
    prob2c(boundadd(i,8,17,32)) = prob0a(i);
end
for i = 32:47
    prob2c(boundadd(i,8,33,48)) = prob0a(i);
end
for i = 49:56
    prob2c(boundadd(i,4,49,56)) = prob0a(i);
end
for i = 57:60
    prob2c(boundadd(i,2,57,60)) = prob0a(i);
end

prob1d = zeros(60,1);
for i = 1:16
    prob1d(boundadd(i,12,1,16)) = prob0a(i);
end
for i = 17:32
    prob1d(boundadd(i,12,17,32)) = prob0a(i);
end
for i = 33:48
    prob1d(boundadd(i,12,33,48)) = prob0a(i);
end
for i = 49:56
    prob1d(boundadd(i,6,49,56)) = prob0a(i);
end
for i = 57:60
    prob1d(boundadd(i,3,57,60)) = prob0a(i);
end

prob3c = zeros(60,1);
for i = 1:15
    prob3c(boundadd(i,4,1,16)) = prob0b(i);
end
for i = 16:31
    prob3c(boundadd(i,4,17,32)) = prob0b(i);
end
for i = 32:47
    prob3c(boundadd(i,4,33,48)) = prob0b(i);
end
for i = 49:56
    prob3c(boundadd(i,2,49,56)) = prob0b(i);
end
for i = 57:60
    prob3c(boundadd(i,1,57,60)) = prob0b(i);
end

prob2d = zeros(60,1);
for i = 1:15
    prob2d(boundadd(i,8,1,16)) = prob0b(i);
end
for i = 16:31
    prob2d(boundadd(i,8,17,32)) = prob0b(i);
end
for i = 32:47
    prob2d(boundadd(i,8,33,48)) = prob0b(i);
end
for i = 49:56
    prob2d(boundadd(i,4,49,56)) = prob0b(i);
end
for i = 57:60
    prob2d(boundadd(i,2,57,60)) = prob0b(i);
end

prob1a = zeros(60,1);
for i = 1:16
    prob1a(boundadd(i,12,1,16)) = prob0b(i);
end
for i = 17:32
    prob1a(boundadd(i,12,17,32)) = prob0b(i);
end
for i = 33:48
    prob1a(boundadd(i,12,33,48)) = prob0b(i);
end
for i = 49:56
    prob1a(boundadd(i,6,49,56)) = prob0b(i);
end
for i = 57:60
    prob1a(boundadd(i,3,57,60)) = prob0b(i);
end


prob1e = zeros(60,1);
for i = 1:16
    prob1e(boundadd(i,4,1,16)) = prob0e(i);
end
for i = 17:32
    prob1e(boundadd(i,4,17,32)) = prob0e(i);
end
for i = 33:48
    prob1e(boundadd(i,4,33,48)) = prob0e(i);
end
for i = 49:56
    prob1e(boundadd(i,2,49,56)) = prob0e(i);
end
for i = 57:60
    prob1e(boundadd(i,1,57,60)) = prob0e(i);
end

prob2e = zeros(60,1);
for i = 1:16
    prob2e(boundadd(i,8,1,16)) = prob0e(i);
end
for i = 17:32
    prob2e(boundadd(i,8,17,32)) = prob0e(i);
end
for i = 33:48
    prob2e(boundadd(i,8,33,48)) = prob0e(i);
end
for i = 49:56
    prob2e(boundadd(i,4,49,56)) = prob0e(i);
end
for i = 57:60
    prob2e(boundadd(i,2,57,60)) = prob0e(i);
end

prob3e = zeros(60,1);
for i = 1:16
    prob3e(boundadd(i,12,1,16)) = prob0e(i);
end
for i = 17:32
    prob3e(boundadd(i,12,17,32)) = prob0e(i);
end
for i = 33:48
    prob3e(boundadd(i,12,33,48)) = prob0e(i);
end
for i = 49:56
    prob3e(boundadd(i,6,49,56)) = prob0e(i);
end
for i = 57:60
    prob3e(boundadd(i,3,57,60)) = prob0e(i);
end


sc = zeros(60,6);
lines = axes;
line(lines,[-2.5, 2.5], [0, 0])

line(lines,[sin(pi/2)*-2.5,   sin(pi/2)*2.5], [cos(pi/2)*-2.5,    cos(pi/2)*2.5])
line(lines,[sin(pi)*-2.5,     sin(pi)*2.5],   [cos(pi)*-2.5,      cos(pi)*2.5])

line(lines,[sin(pi*3/4)*-2.5, sin(pi*3/4)*-0.5],  [cos(pi*3/4)*-2.5,  cos(pi*3/4)*-0.5])
line(lines,[sin(pi/4)*0.5,    sin(pi/4)*2.5],     [cos(pi/4)*0.5,     cos(pi/4)*2.5])
line(lines,[sin(pi*3/4)*0.5,  sin(pi*3/4)*2.5],   [cos(pi*3/4)*0.5,   cos(pi*3/4)*2.5])
line(lines,[sin(pi/4)*-2.5,   sin(pi/4)*-0.5],    [cos(pi/4)*-2.5,    cos(pi/4)*-0.5])

line(lines,[sin(pi*3/8)*-2.5, sin(pi*3/8)*-1.0],  [cos(pi*3/8)*-2.5,  cos(pi*3/8)*-1.0])
line(lines,[sin(pi*5/8)*1.0,  sin(pi*5/8)*2.5],   [cos(pi*5/8)*1.0,   cos(pi*5/8)*2.5])
line(lines,[sin(pi*7/8)*-2.5, sin(pi*7/8)*-1.0],  [cos(pi*7/8)*-2.5,  cos(pi*7/8)*-1.0])
line(lines,[sin(pi*1/8)*-1.0, sin(1/8*pi)*-2.5],  [cos(1/8*pi)*-1.0,  cos(1/8*pi)*-2.5])
line(lines,[sin(pi*5/8)*-2.5, sin(pi*5/8)*-1.0],  [cos(pi*5/8)*-2.5,  cos(pi*5/8)*-1.0])
line(lines,[sin(pi*3/8)*1.0,  sin(pi*3/8)*2.5],   [cos(pi*3/8)*1.0,   cos(pi*3/8)*2.5])
line(lines,[sin(pi*7/8)*2.5,  sin(pi*7/8)*1.0],   [cos(pi*7/8)*2.5,   cos(pi*7/8)*1.0])
line(lines,[sin(pi*1/8)*1.0,  sin(1/8*pi)*2.5],   [cos(1/8*pi)*1.0,   cos(1/8*pi)*2.5])
rectangle(lines,'Position',pos0,'Curvature',[1 1])
rectangle(lines,'Position',pos1,'Curvature',[1 1])
rectangle(lines,'Position',pos2,'Curvature',[1 1])
rectangle(lines,'Position',pos3,'Curvature',[1 1])
rectangle(lines,'Position',pos4,'Curvature',[1 1])
hold(lines,"on")

numbers = zeros(20,1);
numbersbuff = zeros(20,10);
while 1
    

    reading = readline(s);
    number = sscanf(reading, "%f");
    numbersbuff = [numbersbuff number];
    if(length(numbersbuff(1)) > 10)
        numbers = mean(numbersbuff(:,length(numbersbuff(1,:))-10:length(numbersbuff(1,:))));
    else 
        numbers = numbersbuff(:,length(numbersbuff(1,:)));
    end
        
%     prob = -(prob0a.*numbers(1) + prob0b.*numbers(5) + prob3b.*numbers(8) + prob3c.*numbers(12)... 
%     + prob2c.*numbers(11)*0.8 + prob2d.*numbers(15)*0.8 + prob1d.*numbers(14) + prob1a.*numbers(2) ...
%     + prob0d.*numbers(13) + prob1c.*numbers(10) + prob2b.*numbers(7)*0.8 + prob3a.*numbers(4)...
%     + prob0c.*numbers(9) + prob1b.*numbers(6)*0.8 + prob2a.*numbers(3) + prob3d.*numbers(16));

%      prob = -(prob0a.*numbers(1) + prob0b.*numbers(5) + prob3b.*numbers(8) + prob3c.*numbers(12)... 
%      + prob2c.*numbers(11) + prob2d.*numbers(15) + prob1d.*numbers(14) + prob1a.*numbers(2) ...
%      + prob0e.*numbers(17) + prob1e.*numbers(18) +prob2e.*numbers(19) + prob3e.*numbers(20));

    prob = prob0e.*numbers(17);
   

    angle = pi/8;
    rad = 0.5;

    t1 = [];
    sc(1,:)  = [(2.25)*cos(pi*1/16),(2.25)*sin(pi*1/16), max(prob(1)*2, 1), [min(prob(1),255), max(255 - prob(1),0) 0]/255];            
    for j = 0:2
        for i = 0:15
            %t1 = [t1 text((2.25-j*rad)*cos(pi*1/16+i*angle),(2.25-j*rad)*sin(pi*1/16+i*angle),num2str(prob(j*16+i)))];
            sc(j*16+i+1,:)  = [(2.25-j*rad)*cos(pi*1/16+i*angle) ,(2.25-j*rad)*sin(pi*1/16+i*angle), max(prob(j*16+i+1)*2, 1), [min(prob(j*16+i+1),255), max(255 - prob(j*16+i+1),0) 0]/255];
        end
    end
    for i = 0:7
            %t1 = [t1 text((0.75)*cos(pi*1/8+i*2*angle),(0.75)*sin(pi*1/8+i*2*angle),num2str(prob(48+i)))];
            sc(49+i,:) = [(0.75)*cos(pi*1/8+i*2*angle) ,(0.75)*sin(pi*1/8+i*2*angle),max(prob(48+i+1)*2,1),[min(prob(48+i+1),255) max(255 - prob(48+i+1),0) 0]/255];
    end
    for i = 0:3 
            %t1 = [t1 text((0.25)*cos(pi*1/4+i*4*angle),(0.25)*sin(pi*1/4+i*4*angle),num2str(prob(56+i)))];
            sc(57+i,:) = [(0.25)*cos(pi*1/4+i*4*angle) ,(0.25)*sin(pi*1/4+i*4*angle),max(prob(56+i+1)*2,1),[min(prob(56+i+1),255) max(255 - prob(56+i+1),0) 0]/255];
    end
   
    numbers;
    map = scatter(sc(:,1),sc(:,2),sc(:,3),sc(:,4:6),'filled');
    %map = scatter(sc(ind(1:5),1),sc(ind(1:5),2),sc(ind(1:5),3),sc(ind(1:5),4:6),'filled');
    %map = scatter(mean(sc(ind(1:5),1)),mean(sc(ind(1:5),2)),sc(ind(1),3),sc(ind(1),4:6),'filled');
    pause(0.1)
    delete(map);
    axis equal
       
    
end


