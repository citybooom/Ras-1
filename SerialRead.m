clear all

s = serialport("COM3",2000000);
buffer = zeros(16,100);
fig = figure;
tiledlayout(2,2)
x = linspace(1,100,100);

while 1
    reading = readline(s);
    numbers = sscanf(reading, "%f");
    buffer(:,1) = [];
    buffer = [buffer,numbers];

    nexttile(1)
    Graph1 = plot(x, buffer(1,:),x, buffer(5,:),x, buffer(9,:),x, buffer(13,:));
    axis([0 100 -30 30])

    nexttile(2)
    Graph2 = plot(x, buffer(2,:),x, buffer(6,:),x, buffer(10,:),x, buffer(14,:));
    axis([0 100 -30 30])

    nexttile(3)
    Graph3 = plot(x, buffer(3,:),x, buffer(7,:),x, buffer(11,:),x, buffer(15,:));
    axis([0 100 -30 30])

    nexttile(4)
    Graph4 = plot(x, buffer(4,:),x, buffer(8,:),x, buffer(12,:),x, buffer(16,:));
    axis([0 100 -30 30])
    
    numbers(2)
    
end


