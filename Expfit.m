clear all

s = serialport("COM4",9600);
buffer = zeros(4,100);
fig4 = figure;
% tiledlayout(2,2)
x = linspace(1,100,100);
x1 = (0:0.2:5)';
y1 = 2*exp(-0.2*x1) + 0.1*randn(size(x1));
f1 = fit(x1,y1,'exp1');
ten = linspace(1,10,10)';

while 1
    reading = readline(s);
    numbers = sscanf(reading, "%f");
    buffer(:,1) = [];
    buffer = [buffer,numbers];

%     nexttile(1)
%     Graph1 = plot(x, buffer(1,:),x, buffer(2,:),x, buffer(3,:),x, buffer(4,:));
%     axis([0 100 -200 2000])
%     
%     nexttile(2)
    y2 = buffer(1,91:100)';
    f1 = fit(ten,y2,'exp1');
    
    Graph2 =  plot(f1,ten,y2);
    %axis([ 0 3 0 3 0 2000])
end

