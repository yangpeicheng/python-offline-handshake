function [c,ceq] = unitdisk(x,g)
    c = [];
    %a=x(1)^2 + x(2)^2 +x(3)^2-1
    %b=x(1)*g(1)+x(2)*g(2)+x(3)*g(3)
    ceq = [norm(x)-1,x(3)];
end