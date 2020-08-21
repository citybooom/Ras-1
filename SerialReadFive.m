clear all

s = serialport("COM3",9600);
buffer = zeros(20,100);
fig4 = figure;   
tiledlayout(2,2)
x = linspace(1,100,100);

while 1
    reading = readline(s);
    numbers = sscanf(reading, "%f");
    buffer(:,1) = [];
    buffer = [buffer,numbers];

    nexttile(1)
    Graph1 = plot(x, buffer(1,:),x, buffer(5,:),x, buffer(17,:));
    axis([0 100 -5 5])

    nexttile(2)
    Graph2 = plot(x, buffer(14,:),x, buffer(2,:),x, buffer(18,:));
    axis([0 100 -5 5])

    nexttile(3)
    Graph3 = plot(x, buffer(11,:),x, buffer(15,:),x,buffer(19,:));
    axis([0 100 -5 5])

    nexttile(4)
    Graph4 = plot(x, buffer(8,:),x, buffer(12,:),x,buffer(20,:));
    axis([0 100 -5 5])
    
    
    drawnow
end


