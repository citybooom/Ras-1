[X,Y] = meshgrid(1:100,1:100);
Z = rand(size(X));
tic
surf(X,Y,Z)
for i = 1:10
    surf(X,Y,Z);
end
t1 = toc;
tic
h = surf(X,Y,Z);
for i = 1:10
    Z = rand(size(X));
    h.ZData = Z;
end
t2 = toc;