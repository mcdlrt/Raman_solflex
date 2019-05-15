function y = lorentz(x,g,x0)
    y = (1/pi).*(0.5.*g)./((x-x0).^2+(0.5.*g).^2);
end
