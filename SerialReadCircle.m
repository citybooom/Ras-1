clear all

% s = serialport("COM3",2000000);

center = [0,0,0,0,0];
radii = [1,2,3,4,5];

pos0 = [-0.5 -0.5 1 1];
pos1 = [-1 -1 2 2];
pos2 = [-1.5 -1.5 3 3];
pos3 = [-2 -2 4 4];
pos4 = [-2.5 -2.5 5 5];

prob0a = zeros(60,1);
[prob0a(8:11)] = deal(10);
[prob0a(26),prob0a(42)] = deal(8);
[prob0a(43),prob0a(54),prob0a(27),prob0a(25),prob0a(41)] = deal(6);
[prob0a(40),prob0a(24),prob0a(53:54),prob0a(58),prob0a(59)] = deal(4);
[prob0a(55),prob0a(45),prob0a(44),prob0a(28),prob0a(29),prob0a(12),prob0a(13),prob0a(57),prob0a(60)] = deal(2);

[prob0a(5:7)] = deal(-8);
[prob0a(1:3),prob0a(14:16),prob0a(21:23)] = deal(-6);
[prob0a(36),prob0a(20),prob0a(30:32),prob0a(37:39),prob0a(17:18)] = deal(-4);
[prob0a(4),prob0a(50),prob0a(19),prob0a(3),prob0a(33:35),prob0a(46:48),prob0a(51:52)] = deal(-2);


prob0b = zeros(60,1);
for i = 1:15
    prob0b(i) = prob0a(17-i);
end
for i = 16:31
    prob0b(i) = prob0a(16 + 33 - i);
end
for i = 32:47
    prob0b(i) = prob0a(32 + 49 - i);
end
for i = 49:56
    prob0b(i) = prob0a(48 + 57 - i);
end
for i = 57:60
    prob0b(i) = prob0a(56 + 61 - i);
end

prob0d = zeros(60,1);

[prob0d(2:3),prob0d(18:19),prob0d(50:51)] = deal(-6);
[prob0d(4:9),prob0d(20:25),prob0d(34:41),prob0d(57:60),prob0d(49),prob0d(52),prob0d(53)] = deal(-4);
prob0d(54:56) = deal(-2);


prob0c = zeros(60,1);
for i = 1:15
    prob0c(i) = prob0d(17-i);
end
for i = 16:31
    prob0c(i) = prob0d(16 + 33 - i);
end
for i = 32:47
    prob0c(i) = prob0d(32 + 49 - i);
end
for i = 49:56
    prob0c(i) = prob0d(48 + 57 - i);
end
for i = 57:60
    prob0c(i) = prob0d(56 + 61 - i);
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
    prob2c(boundadd(i,8,1,16)) = prob0b(i);
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

% for i = 0:7
%         text((0.75)*cos(pi*1/8+i*2*angle),(0.75)*sin(pi*1/8+i*2*angle),num2str(48+i));
% end
% for i = 0:3 
%         text((0.25)*cos(pi*1/4+i*4*angle),(0.25)*sin(pi*1/4+i*4*angle),num2str(56+i));
% end


% for j = 0:2
%     for i = 0:15
%         text((2.25-j*rad)*cos(pi*1/16+i*angle),(2.25-j*rad)*sin(pi*1/16+i*angle),num2str(j*16+i+1));
%     end
% end
% for i = 0:7
%         text((0.75)*cos(pi*1/8+i*2*angle),(0.75)*sin(pi*1/8+i*2*angle),num2str(48+i+1));
% end
% for i = 0:3 
%         text((0.25)*cos(pi*1/4+i*4*angle),(0.25)*sin(pi*1/4+i*4*angle),num2str(56+i+1));
% end

fig = figure;
tiledlayout(2,2)

nexttile(1)

rectangle('Position',pos0,'Curvature',[1 1])
rectangle('Position',pos1,'Curvature',[1 1])
rectangle('Position',pos2,'Curvature',[1 1])
rectangle('Position',pos3,'Curvature',[1 1])
rectangle('Position',pos4,'Curvature',[1 1])
line([-2.5, 2.5], [0, 0])

line([sin(pi/2)*-2.5,   sin(pi/2)*2.5], [cos(pi/2)*-2.5,    cos(pi/2)*2.5])
line([sin(pi)*-2.5,     sin(pi)*2.5],   [cos(pi)*-2.5,      cos(pi)*2.5])

line([sin(pi*3/4)*-2.5, sin(pi*3/4)*-0.5],  [cos(pi*3/4)*-2.5,  cos(pi*3/4)*-0.5])
line([sin(pi/4)*0.5,    sin(pi/4)*2.5],     [cos(pi/4)*0.5,     cos(pi/4)*2.5])
line([sin(pi*3/4)*0.5,  sin(pi*3/4)*2.5],   [cos(pi*3/4)*0.5,   cos(pi*3/4)*2.5])
line([sin(pi/4)*-2.5,   sin(pi/4)*-0.5],    [cos(pi/4)*-2.5,    cos(pi/4)*-0.5])

line([sin(pi*3/8)*-2.5, sin(pi*3/8)*-1.0],  [cos(pi*3/8)*-2.5,  cos(pi*3/8)*-1.0])
line([sin(pi*5/8)*1.0,  sin(pi*5/8)*2.5],   [cos(pi*5/8)*1.0,   cos(pi*5/8)*2.5])
line([sin(pi*7/8)*-2.5, sin(pi*7/8)*-1.0],  [cos(pi*7/8)*-2.5,  cos(pi*7/8)*-1.0])
line([sin(pi*1/8)*-1.0, sin(1/8*pi)*-2.5],  [cos(1/8*pi)*-1.0,  cos(1/8*pi)*-2.5])
line([sin(pi*5/8)*-2.5, sin(pi*5/8)*-1.0],  [cos(pi*5/8)*-2.5,  cos(pi*5/8)*-1.0])
line([sin(pi*3/8)*1.0,  sin(pi*3/8)*2.5],   [cos(pi*3/8)*1.0,   cos(pi*3/8)*2.5])
line([sin(pi*7/8)*2.5,  sin(pi*7/8)*1.0],   [cos(pi*7/8)*2.5,   cos(pi*7/8)*1.0])
line([sin(pi*1/8)*1.0,  sin(1/8*pi)*2.5],   [cos(1/8*pi)*1.0,   cos(1/8*pi)*2.5])

angle = pi/8;
rad = 0.5;
for j = 0:2
    for i = 0:15
        if(i+j>0)
            text((2.25-j*rad)*cos(pi*1/16+i*angle),(2.25-j*rad)*sin(pi*1/16+i*angle),num2str(prob0a(j*16+i+1)));
        end
    end
end
for i = 0:7
        text((0.75)*cos(pi*1/8+i*2*angle),(0.75)*sin(pi*1/8+i*2*angle),num2str(prob0a(48+i+1)));
end
for i = 0:3 
        text((0.25)*cos(pi*1/4+i*4*angle),(0.25)*sin(pi*1/4+i*4*angle),num2str(prob0a(56+i+1)));
end

nexttile(2)

rectangle('Position',pos0,'Curvature',[1 1])
rectangle('Position',pos1,'Curvature',[1 1])
rectangle('Position',pos2,'Curvature',[1 1])
rectangle('Position',pos3,'Curvature',[1 1])
rectangle('Position',pos4,'Curvature',[1 1])
line([-2.5, 2.5], [0, 0])

line([sin(pi/2)*-2.5,   sin(pi/2)*2.5], [cos(pi/2)*-2.5,    cos(pi/2)*2.5])
line([sin(pi)*-2.5,     sin(pi)*2.5],   [cos(pi)*-2.5,      cos(pi)*2.5])

line([sin(pi*3/4)*-2.5, sin(pi*3/4)*-0.5],  [cos(pi*3/4)*-2.5,  cos(pi*3/4)*-0.5])
line([sin(pi/4)*0.5,    sin(pi/4)*2.5],     [cos(pi/4)*0.5,     cos(pi/4)*2.5])
line([sin(pi*3/4)*0.5,  sin(pi*3/4)*2.5],   [cos(pi*3/4)*0.5,   cos(pi*3/4)*2.5])
line([sin(pi/4)*-2.5,   sin(pi/4)*-0.5],    [cos(pi/4)*-2.5,    cos(pi/4)*-0.5])

line([sin(pi*3/8)*-2.5, sin(pi*3/8)*-1.0],  [cos(pi*3/8)*-2.5,  cos(pi*3/8)*-1.0])
line([sin(pi*5/8)*1.0,  sin(pi*5/8)*2.5],   [cos(pi*5/8)*1.0,   cos(pi*5/8)*2.5])
line([sin(pi*7/8)*-2.5, sin(pi*7/8)*-1.0],  [cos(pi*7/8)*-2.5,  cos(pi*7/8)*-1.0])
line([sin(pi*1/8)*-1.0, sin(1/8*pi)*-2.5],  [cos(1/8*pi)*-1.0,  cos(1/8*pi)*-2.5])
line([sin(pi*5/8)*-2.5, sin(pi*5/8)*-1.0],  [cos(pi*5/8)*-2.5,  cos(pi*5/8)*-1.0])
line([sin(pi*3/8)*1.0,  sin(pi*3/8)*2.5],   [cos(pi*3/8)*1.0,   cos(pi*3/8)*2.5])
line([sin(pi*7/8)*2.5,  sin(pi*7/8)*1.0],   [cos(pi*7/8)*2.5,   cos(pi*7/8)*1.0])
line([sin(pi*1/8)*1.0,  sin(1/8*pi)*2.5],   [cos(1/8*pi)*1.0,   cos(1/8*pi)*2.5])

angle = pi/8;
rad = 0.5;
for j = 0:2
    for i = 0:15
        if(i+j>0)
            text((2.25-j*rad)*cos(pi*1/16+i*angle),(2.25-j*rad)*sin(pi*1/16+i*angle),num2str(prob0b(j*16+i+1)));
        end
    end
end
for i = 0:7
        text((0.75)*cos(pi*1/8+i*2*angle),(0.75)*sin(pi*1/8+i*2*angle),num2str(prob0b(48+i+1)));
end
for i = 0:3 
        text((0.25)*cos(pi*1/4+i*4*angle),(0.25)*sin(pi*1/4+i*4*angle),num2str(prob0b(56+i+1)));
end

nexttile(3)

rectangle('Position',pos0,'Curvature',[1 1])
rectangle('Position',pos1,'Curvature',[1 1])
rectangle('Position',pos2,'Curvature',[1 1])
rectangle('Position',pos3,'Curvature',[1 1])
rectangle('Position',pos4,'Curvature',[1 1])
line([-2.5, 2.5], [0, 0])

line([sin(pi/2)*-2.5,   sin(pi/2)*2.5], [cos(pi/2)*-2.5,    cos(pi/2)*2.5])
line([sin(pi)*-2.5,     sin(pi)*2.5],   [cos(pi)*-2.5,      cos(pi)*2.5])

line([sin(pi*3/4)*-2.5, sin(pi*3/4)*-0.5],  [cos(pi*3/4)*-2.5,  cos(pi*3/4)*-0.5])
line([sin(pi/4)*0.5,    sin(pi/4)*2.5],     [cos(pi/4)*0.5,     cos(pi/4)*2.5])
line([sin(pi*3/4)*0.5,  sin(pi*3/4)*2.5],   [cos(pi*3/4)*0.5,   cos(pi*3/4)*2.5])
line([sin(pi/4)*-2.5,   sin(pi/4)*-0.5],    [cos(pi/4)*-2.5,    cos(pi/4)*-0.5])

line([sin(pi*3/8)*-2.5, sin(pi*3/8)*-1.0],  [cos(pi*3/8)*-2.5,  cos(pi*3/8)*-1.0])
line([sin(pi*5/8)*1.0,  sin(pi*5/8)*2.5],   [cos(pi*5/8)*1.0,   cos(pi*5/8)*2.5])
line([sin(pi*7/8)*-2.5, sin(pi*7/8)*-1.0],  [cos(pi*7/8)*-2.5,  cos(pi*7/8)*-1.0])
line([sin(pi*1/8)*-1.0, sin(1/8*pi)*-2.5],  [cos(1/8*pi)*-1.0,  cos(1/8*pi)*-2.5])
line([sin(pi*5/8)*-2.5, sin(pi*5/8)*-1.0],  [cos(pi*5/8)*-2.5,  cos(pi*5/8)*-1.0])
line([sin(pi*3/8)*1.0,  sin(pi*3/8)*2.5],   [cos(pi*3/8)*1.0,   cos(pi*3/8)*2.5])
line([sin(pi*7/8)*2.5,  sin(pi*7/8)*1.0],   [cos(pi*7/8)*2.5,   cos(pi*7/8)*1.0])
line([sin(pi*1/8)*1.0,  sin(1/8*pi)*2.5],   [cos(1/8*pi)*1.0,   cos(1/8*pi)*2.5])

angle = pi/8;
rad = 0.5;
for j = 0:2
    for i = 0:15
        if(i+j>0)
            text((2.25-j*rad)*cos(pi*1/16+i*angle),(2.25-j*rad)*sin(pi*1/16+i*angle),num2str(prob0c(j*16+i+1)));
        end
    end
end
for i = 0:7
        text((0.75)*cos(pi*1/8+i*2*angle),(0.75)*sin(pi*1/8+i*2*angle),num2str(prob0c(48+i+1)));
end
for i = 0:3 
        text((0.25)*cos(pi*1/4+i*4*angle),(0.25)*sin(pi*1/4+i*4*angle),num2str(prob0c(56+i+1)));
end

nexttile(4)

rectangle('Position',pos0,'Curvature',[1 1])
rectangle('Position',pos1,'Curvature',[1 1])
rectangle('Position',pos2,'Curvature',[1 1])
rectangle('Position',pos3,'Curvature',[1 1])
rectangle('Position',pos4,'Curvature',[1 1])
line([-2.5, 2.5], [0, 0])

line([sin(pi/2)*-2.5,   sin(pi/2)*2.5], [cos(pi/2)*-2.5,    cos(pi/2)*2.5])
line([sin(pi)*-2.5,     sin(pi)*2.5],   [cos(pi)*-2.5,      cos(pi)*2.5])

line([sin(pi*3/4)*-2.5, sin(pi*3/4)*-0.5],  [cos(pi*3/4)*-2.5,  cos(pi*3/4)*-0.5])
line([sin(pi/4)*0.5,    sin(pi/4)*2.5],     [cos(pi/4)*0.5,     cos(pi/4)*2.5])
line([sin(pi*3/4)*0.5,  sin(pi*3/4)*2.5],   [cos(pi*3/4)*0.5,   cos(pi*3/4)*2.5])
line([sin(pi/4)*-2.5,   sin(pi/4)*-0.5],    [cos(pi/4)*-2.5,    cos(pi/4)*-0.5])

line([sin(pi*3/8)*-2.5, sin(pi*3/8)*-1.0],  [cos(pi*3/8)*-2.5,  cos(pi*3/8)*-1.0])
line([sin(pi*5/8)*1.0,  sin(pi*5/8)*2.5],   [cos(pi*5/8)*1.0,   cos(pi*5/8)*2.5])
line([sin(pi*7/8)*-2.5, sin(pi*7/8)*-1.0],  [cos(pi*7/8)*-2.5,  cos(pi*7/8)*-1.0])
line([sin(pi*1/8)*-1.0, sin(1/8*pi)*-2.5],  [cos(1/8*pi)*-1.0,  cos(1/8*pi)*-2.5])
line([sin(pi*5/8)*-2.5, sin(pi*5/8)*-1.0],  [cos(pi*5/8)*-2.5,  cos(pi*5/8)*-1.0])
line([sin(pi*3/8)*1.0,  sin(pi*3/8)*2.5],   [cos(pi*3/8)*1.0,   cos(pi*3/8)*2.5])
line([sin(pi*7/8)*2.5,  sin(pi*7/8)*1.0],   [cos(pi*7/8)*2.5,   cos(pi*7/8)*1.0])
line([sin(pi*1/8)*1.0,  sin(1/8*pi)*2.5],   [cos(1/8*pi)*1.0,   cos(1/8*pi)*2.5])

angle = pi/8;
rad = 0.5;
for j = 0:2
    for i = 0:15
        if(i+j>0)
            text((2.25-j*rad)*cos(pi*1/16+i*angle),(2.25-j*rad)*sin(pi*1/16+i*angle),num2str(prob0d(j*16+i+1)));
        end
    end
end
for i = 0:7
        text((0.75)*cos(pi*1/8+i*2*angle),(0.75)*sin(pi*1/8+i*2*angle),num2str(prob0d(48+i+1)));
end
for i = 0:3 
        text((0.25)*cos(pi*1/4+i*4*angle),(0.25)*sin(pi*1/4+i*4*angle),num2str(prob0d(56+i+1)));
end

fig2 = figure;
rectangle('Position',pos0,'Curvature',[1 1])
rectangle('Position',pos1,'Curvature',[1 1])
rectangle('Position',pos2,'Curvature',[1 1])
rectangle('Position',pos3,'Curvature',[1 1])
rectangle('Position',pos4,'Curvature',[1 1])
line([-2.5, 2.5], [0, 0])

line([sin(pi/2)*-2.5,   sin(pi/2)*2.5], [cos(pi/2)*-2.5,    cos(pi/2)*2.5])
line([sin(pi)*-2.5,     sin(pi)*2.5],   [cos(pi)*-2.5,      cos(pi)*2.5])

line([sin(pi*3/4)*-2.5, sin(pi*3/4)*-0.5],  [cos(pi*3/4)*-2.5,  cos(pi*3/4)*-0.5])
line([sin(pi/4)*0.5,    sin(pi/4)*2.5],     [cos(pi/4)*0.5,     cos(pi/4)*2.5])
line([sin(pi*3/4)*0.5,  sin(pi*3/4)*2.5],   [cos(pi*3/4)*0.5,   cos(pi*3/4)*2.5])
line([sin(pi/4)*-2.5,   sin(pi/4)*-0.5],    [cos(pi/4)*-2.5,    cos(pi/4)*-0.5])

line([sin(pi*3/8)*-2.5, sin(pi*3/8)*-1.0],  [cos(pi*3/8)*-2.5,  cos(pi*3/8)*-1.0])
line([sin(pi*5/8)*1.0,  sin(pi*5/8)*2.5],   [cos(pi*5/8)*1.0,   cos(pi*5/8)*2.5])
line([sin(pi*7/8)*-2.5, sin(pi*7/8)*-1.0],  [cos(pi*7/8)*-2.5,  cos(pi*7/8)*-1.0])
line([sin(pi*1/8)*-1.0, sin(1/8*pi)*-2.5],  [cos(1/8*pi)*-1.0,  cos(1/8*pi)*-2.5])
line([sin(pi*5/8)*-2.5, sin(pi*5/8)*-1.0],  [cos(pi*5/8)*-2.5,  cos(pi*5/8)*-1.0])
line([sin(pi*3/8)*1.0,  sin(pi*3/8)*2.5],   [cos(pi*3/8)*1.0,   cos(pi*3/8)*2.5])
line([sin(pi*7/8)*2.5,  sin(pi*7/8)*1.0],   [cos(pi*7/8)*2.5,   cos(pi*7/8)*1.0])
line([sin(pi*1/8)*1.0,  sin(1/8*pi)*2.5],   [cos(1/8*pi)*1.0,   cos(1/8*pi)*2.5])

angle = pi/8;
rad = 0.5;

for j = 0:2
    for i = 0:15
        if(i+j>0)
            text((2.25-j*rad)*cos(pi*1/16+i*angle),(2.25-j*rad)*sin(pi*1/16+i*angle),num2str((j*16+i+1)));
        end
    end
end
for i = 0:7
        text((0.75)*cos(pi*1/8+i*2*angle),(0.75)*sin(pi*1/8+i*2*angle),num2str((48+i+1)));
end
for i = 0:3 
        text((0.25)*cos(pi*1/4+i*4*angle),(0.25)*sin(pi*1/4+i*4*angle),num2str((56+i+1)));
end


function f = boundadd(a,b,lower, upper)
    if(a + b <= upper)
        f = a + b;
    else
        f = lower + (a+b) - upper - 1;
    end
end
