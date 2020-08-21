clear all

s = serialport("COM4",9600);
buffer = zeros(4,100);
fig4 = figure;
tiledlayout(2,2)
x = linspace(1,100,100);

while 1
    reading = readline(s);
    numbers = sscanf(reading, "%f");
    buffer(:,1) = [];
    buffer = [buffer,numbers];

    nexttile(1)
    Graph1 = plot(x, buffer(1,:),x, buffer(2,:),x, buffer(3,:),x, buffer(4,:));
    axis([0 100 -200 500])
    
    nexttile(2)
    bars = [buffer(1,99),buffer(2,99) ; buffer(3,99), buffer(4,99)];
    bar3(bars)
    axis([ 0 3 0 3 0 2000])
end


