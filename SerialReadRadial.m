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

while 1
    
    hold on
    reading = readline(s);
    numbers = sscanf(reading, "%f");
  
    quadrents = [(numbers(15))- (numbers(11))- (numbers(2)) + (numbers(14)) , ...
                 (numbers(2))- (numbers(14))+ (numbers(1)) - (numbers(5)) , ...
                 -(numbers(1))+ (numbers(2))+ (numbers(8)) - (numbers(12)) , ...
                 -(numbers(8))+ (numbers(12))- (numbers(15)) + (numbers(11))];
    [most,pos] = max(quadrents);
    
    
    switch pos
        case 1
        case 2
        case 3
        case 4
    end

             
      
%     rectangle('Position',pos0,'Curvature',[1 1])
%     rectangle('Position',pos1,'Curvature',[1 1])
%     rectangle('Position',pos2,'Curvature',[1 1])
%     rectangle('Position',pos3,'Curvature',[1 1])
%     rectangle('Position',pos4,'Curvature',[1 1])
%     line([-2.5, 2.5], [0, 0])
% 
%     line([sin(pi/2)*-2.5,   sin(pi/2)*2.5], [cos(pi/2)*-2.5,    cos(pi/2)*2.5])
%     line([sin(pi)*-2.5,     sin(pi)*2.5],   [cos(pi)*-2.5,      cos(pi)*2.5])
% 
%     line([sin(pi*3/4)*-2.5, sin(pi*3/4)*-0.5],  [cos(pi*3/4)*-2.5,  cos(pi*3/4)*-0.5])
%     line([sin(pi/4)*0.5,    sin(pi/4)*2.5],     [cos(pi/4)*0.5,     cos(pi/4)*2.5])
%     line([sin(pi*3/4)*0.5,  sin(pi*3/4)*2.5],   [cos(pi*3/4)*0.5,   cos(pi*3/4)*2.5])
%     line([sin(pi/4)*-2.5,   sin(pi/4)*-0.5],    [cos(pi/4)*-2.5,    cos(pi/4)*-0.5])
% 
%     line([sin(pi*3/8)*-2.5, sin(pi*3/8)*-1.0],  [cos(pi*3/8)*-2.5,  cos(pi*3/8)*-1.0])
%     line([sin(pi*5/8)*1.0,  sin(pi*5/8)*2.5],   [cos(pi*5/8)*1.0,   cos(pi*5/8)*2.5])
%     line([sin(pi*7/8)*-2.5, sin(pi*7/8)*-1.0],  [cos(pi*7/8)*-2.5,  cos(pi*7/8)*-1.0])
%     line([sin(pi*1/8)*-1.0, sin(1/8*pi)*-2.5],  [cos(1/8*pi)*-1.0,  cos(1/8*pi)*-2.5])
%     line([sin(pi*5/8)*-2.5, sin(pi*5/8)*-1.0],  [cos(pi*5/8)*-2.5,  cos(pi*5/8)*-1.0])
%     line([sin(pi*3/8)*1.0,  sin(pi*3/8)*2.5],   [cos(pi*3/8)*1.0,   cos(pi*3/8)*2.5])
%     line([sin(pi*7/8)*2.5,  sin(pi*7/8)*1.0],   [cos(pi*7/8)*2.5,   cos(pi*7/8)*1.0])
%     line([sin(pi*1/8)*1.0,  sin(1/8*pi)*2.5],   [cos(1/8*pi)*1.0,   cos(1/8*pi)*2.5])
% 
%     angle = pi/8;
%     rad = 0.5;
%     
%     point = 0;
%     point = max(prob);
%     
%     
%     
%     t1 = [];
%     sc(1,:)  = [(2.25)*cos(pi*1/16),(2.25)*sin(pi*1/16), max(prob(1)*2, 1), [min(prob(1),255), max(255 - prob(1),0) 0]/255];            
%     for j = 0:2
%         for i = 1:16
%             if(i+j>0)
%                 %t1 = [t1 text((2.25-j*rad)*cos(pi*1/16+i*angle),(2.25-j*rad)*sin(pi*1/16+i*angle),num2str(prob(j*16+i)))];
%                 sc(j*16+i,:)  = [(2.25-j*rad)*cos(pi*1/16+i*angle) ,(2.25-j*rad)*sin(pi*1/16+i*angle), max(prob(j*16+i)*2, 1), [min(prob(j*16+i),255), max(255 - prob(j*16+i),0) 0]/255];
% %                if((prob(j*16+i)) == point && point > 30)
% %                     set(sc,'XData',(2.25-j*rad)*cos(pi*1/16+i*angle),'YData',(2.25-j*rad)*sin(pi*1/16+i*angle));
% %                     set(sc,'SizeData',point*10);
% %                     set(sc,'MarkerFaceColor',	[min(point,255) max(255 - point,0) 0]/255);
%                 %end
%             end
%         end
%     end
%     for i = 0:7
%             %t1 = [t1 text((0.75)*cos(pi*1/8+i*2*angle),(0.75)*sin(pi*1/8+i*2*angle),num2str(prob(48+i)))];
%             sc(49+i,:) = [(0.75)*cos(pi*1/8+i*2*angle) ,(0.75)*sin(pi*1/8+i*2*angle),max(prob(48+i)*2,1),[min(prob(48+i),255) max(255 - prob(48+i),0) 0]/255];
% %            if((prob(48+i)) == point && point > 30)
% %                 set(sc,'XData',((0.75)*cos(pi*1/8+i*2*angle)),'YData',(0.75)*sin(pi*1/8+i*2*angle));
% %                 set(sc,'SizeData',point*10);
% %                 set(sc,'MarkerFaceColor',	[min(point,255) max(255 - point,0) 0]/255);
%             %end
%     end
%     for i = 0:3 
%             %t1 = [t1 text((0.25)*cos(pi*1/4+i*4*angle),(0.25)*sin(pi*1/4+i*4*angle),num2str(prob(56+i)))];
%             sc(57+i,:) = [(0.25)*cos(pi*1/4+i*4*angle) ,(0.25)*sin(pi*1/4+i*4*angle),max(prob(56+i)*2,1),[min(prob(56+i),255) max(255 - prob(56+i),0) 0]/255];
% %            if((prob(56+i)) == point && point > 30)
% %                 set(sc,'XData',((0.25)*cos(pi*1/4+i*4*angle)),'YData',(0.25)*sin(pi*1/4+i*4*angle));
% %                 set(sc,'SizeData',point*10);
% %                 set(sc,'MarkerFaceColor',	[min(point,255) max(255 - point,0) 0]/255);
%             %end
%     end
%    
%     numbers;
%     map = scatter(sc(:,1),sc(:,2),sc(:,3),sc(:,4:6),'filled');
%     pause(0.1)
%     delete(map);
    %[numbers(5) numbers(9)]

    hold off
    
    
end


