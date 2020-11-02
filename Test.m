square_ratios_alt = zeros(30,6);

ratios_3_add = zeros(6,1);
ratios_2_add = zeros(6,1);

for i = 1:6
    ratios_3_add(i) = mean((square_ratios(:,i)));
    ratios_2_add(i) = mean((square_ratios_4(:,i)));
end

for i = 1:6
  for j = 1:30
      square_ratios_alt(j,i) = ratios_2_add(i)-ratios_3_add(i) + square_ratios(j,i);
  end
end