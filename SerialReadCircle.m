clear all

% s = serialport("COM3",2000000);
figure

center = [0,0,0,0,0];
radii = [1,2,3,4,5];

pos0 = [-0.5 -0.5 1 1];
pos1 = [-1 -1 2 2];
pos2 = [-1.5 -1.5 3 3];
pos3 = [-2 -2 4 4];
pos4 = [-2.5 -2.5 5 5];

prob0a = zeros(60,1);
[prob0a(24),prob0a(40)] = deal(10);
[prob0a(8),prob0a(25),prob0a(41),prob0a(52)] = deal(8);
[prob0a(9),prob0a(10),prob0a(42),prob0a(53),prob0a(26),prob0a(58)] = deal(6);
[prob0a(39),prob0a(23),prob0a(51),prob0a(57)] = deal(4);
[prob0a(54),prob0a(44),prob0a(43),prob0a(27),prob0a(28),prob0a(11),prob0a(12),prob0a(7)] = deal(2);

[prob0a(38),prob0a(22),prob0a(37),prob0a(21)] = deal(-8);
[prob0a(6),prob0a(5),prob0a(50),prob0a(36)] = deal(-6);
[prob0a(20),prob0a(35),prob0a(19),prob0a(4)] = deal(-4);
[prob0a(3),prob0a(5),prob0a(34),prob0a(49),prob0a(18),prob0a(2)] = deal(-2);

prob0b = zeros(60,1);
[prob0b(39),prob0b(23)] = deal(10);
[prob0b(22),prob0b(38),prob0b(51),prob0b(7)] = deal(8);
[prob0b(5),prob0b(21),prob0b(37),prob0b(50),prob0b(57),prob0b(6)] = deal(6);
[prob0b(52),prob0b(40),prob0b(24),prob0b(58)] = deal(4);
[prob0b(4),prob0b(20),prob0b(36),prob0b(49),prob0b(35),prob0b(19),prob0b(3),prob0b(8)] = deal(2);

[prob0b(41),prob0b(25),prob0b(26),prob0b(42)] = deal(-8);
[prob0b(9),prob0b(53),prob0b(43),prob0b(10)] = deal(-6);
[prob0b(11),prob0b(27),prob0b(28),prob0b(44)] = deal(-4);
[prob0b(12),prob0b(13),prob0b(29),prob0b(45),prob0b(54)] = deal(-2);




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
% for j = 0:2
%     for i = 0:15
%         text((2.25-j*rad)*cos(pi*1/16+i*angle),(2.25-j*rad)*sin(pi*1/16+i*angle),num2str(j*16+i));
%     end
% end
% for i = 0:7
%         text((0.75)*cos(pi*1/8+i*2*angle),(0.75)*sin(pi*1/8+i*2*angle),num2str(48+i));
% end
% for i = 0:3 
%         text((0.25)*cos(pi*1/4+i*4*angle),(0.25)*sin(pi*1/4+i*4*angle),num2str(56+i));
% end

for j = 0:2
    for i = 0:15
        if(i+j>0)
            text((2.25-j*rad)*cos(pi*1/16+i*angle),(2.25-j*rad)*sin(pi*1/16+i*angle),num2str(prob0b(j*16+i)));
        end
    end
end
for i = 0:7
        text((0.75)*cos(pi*1/8+i*2*angle),(0.75)*sin(pi*1/8+i*2*angle),num2str(prob0b(48+i)));
end
for i = 0:4 
        text((0.25)*cos(pi*1/4+i*4*angle),(0.25)*sin(pi*1/4+i*4*angle),num2str(prob0b(56+i)));
end


