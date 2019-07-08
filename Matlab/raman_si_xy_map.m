clc
clear all
close all

od = cd;        % Original directory

continuer = 1 ;     % To continue or not
%errX= 0.1 ;     % Horizontal error

prompt = {'legend','shift ref','shift min', 'shift max','Refractive index of polymer'};       % Display for manual inputs
dlg_title = 'Input';        % Input title
num_lines = 1;      % Number of lines
defans = {'' , '519.9234','515','525','1'};        % Default answsers
answer = inputdlg(prompt,dlg_title,num_lines,defans);       % input for main variables
%legendh(i)=answer(1);       % Legend for current file
shift_ref = cell2d(answer(2));     % Shift from reference to literature value
shift_min=cell2d(answer(3));        % Min x axis value
shift_max=cell2d(answer(4));        % Max x axis value
npol = cell2d(answer(5));       % Refractive index of polymer


[file,path] = uigetfile({'*.TXT'}) ;        % Open data file (.txt)
fname=file;        % Store filename
cd (path)       % Goes to data folder
data_raman = importdata(file,'\t',34);      % Importdata %34 or 35
cd (od)     % original directory
data_num = data_raman.data;     % Numerical data from structure
x = unique(data_num(2:end,2));      %   X value in µm
y = unique(data_num(2:end,1));      % Y value in µm
x_s = numel(x) ; %  size of x vector
y_s = numel(y) ; % size of y vector



shift = data_num(1,3:end);      % Shift (cm^-1) for x axis
data_num = sortrows(data_num,2) ;       % Sort data according to x position on the sample

%cts = data_num(1:end-1,3:end);        % Counts
cts = data_num(2:end,3:end);        % Counts
x_fit=shift_min : 0.001:shift_max ;     %  X Fit value
shift_w=shift(shift>shift_min & shift<shift_max);     % Eliminate Value outside of study window
ycts=cts(:,shift>shift_min & shift<shift_max);        % Eliminate Value outside of study window

Nmax = numel(data_num(2:end,1));      % Number of spectra
for i = 1:Nmax
        [ Yf, P, RESNORM, RESIDUAL] = lorentzfit(shift_w,ycts(i,:));        % Fit data to a lorentz law
        f_lorentz = @(x) P(1)./((x - P(2)).^2 + P(3)) + P(4);       % Fit function
        P(4) = 0;       % Set baseline to 0
        cts_fit(i,:)=f_lorentz(x_fit);     % Y fit value
        [cts_max, iymax]= max(cts_fit(i,:));      % Value of raman peak and index
        peak_pos(i)= x_fit(iymax);      % Position of peak (cm-1)
        peak_value(i)=cts_max ;
        FWMH(i)=2*sqrt(abs(P(3)));
        res(i) = RESNORM ;
end


dW = peak_pos - shift_ref ;
epsSi = 100*(dW./(-733)) ; 
eps_2D = reshape(epsSi,y_s,x_s) ;
dW2D =reshape(dW,y_s,x_s) ;       % Transform dW in a matrix instead of an array
pV = reshape(peak_value,y_s,x_s);
FWHM = reshape(FWMH,y_s,x_s) ;
res = reshape(res,y_s,x_s) ;
[X,Y] = meshgrid(x,y);      % Meshgrid for contour plot

figure(1)
contourf(X.*1e-3,Y.*1e-3,eps_2D)
xlabel('mm')
ylabel('mm')
colorbar

figure(2)
imagesc(x.*1e-3,y.*1e-3,dW2D)
xlabel('mm')
ylabel('mm')
colorbar

figure(3)
surface(X.*1e-3,Y.*1e-3,pV,eps_2D)
xlabel('mm')
ylabel('mm')
zlabel('Intensity')
colorbar

figure(4)
surface(X.*1e-3,Y.*1e-3,pV,FWHM)
xlabel('mm')
ylabel('mm')
zlabel('Intensity')

figure(5)
imagesc(x.*1e-3,y.*1e-3,res)
xlabel('mm')
ylabel('mm')
colorbar

figure(6)
imagesc(x.*1e-3,y.*1e-3,eps_2D)
xlabel('x (mm)')
ylabel('y (mm)')
daspect([1 5 1])
colorbar
axis([-1 1 -10 10])
caxis([-0.2 0.2])
title('$\epsilon_{biaxil}$')
colormap jet

figure(7)
imagesc(x.*1e-3,y.*1e-3,FWHM)
xlabel('x (mm)')
ylabel('y (mm)')
daspect([1 5 1])
colorbar
axis([-1 1 -10 10])
caxis([1 4])
colormap jet
title('FWHM')

figure(8)
imagesc(x.*1e-3,y.*1e-3,dW2D)
xlabel('x (mm)')
ylabel('y (mm)')
daspect([1 5 1])
colorbar
axis([-1 1 -10 10])
caxis([-1 1])
colormap jet
title('Raman peak shift')

figure(9)
contourf(X.*1e-3,Y.*1e-3,eps_2D,20)
xlabel('x (mm)')
ylabel('y (mm)')
daspect([1 5 1])
colorbar
axis([-1 1 -10 10])
caxis([-0.2 0.2])
title('$\epsilon_{biaxil}$')
colormap jet

figure(10)
contourf(X.*1e-3,Y.*1e-3,FWHM)
xlabel('x (mm)')
ylabel('y (mm)')
daspect([1 5 1])
colorbar
axis([-1 1 -10 10])
caxis([1 4])
colormap jet
title('FWHM')

figure(11)
contourf(X.*1e-3,Y.*1e-3,dW2D)
xlabel('x (mm)')
ylabel('y (mm)')
daspect([1 5 1])
colorbar
axis([-1 1 -10 10])
caxis([-1 1])
colormap jet
title('Raman peak shift')