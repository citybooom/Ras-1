function f = boundadd(a,b,lower, upper)
    if(a + b <= upper)
        f = a + b;
    else
        f = lower + (a+b) - upper - 1;
    end
end

