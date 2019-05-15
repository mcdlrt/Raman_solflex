clc
clear all
close all

od = cd;        % Original directory
%col=[ 'r' 'b' 'k' 'g' 'c' 'y'];     % Color vector for the plots
%mark = [ '.' 'o' '+' '*' 'x' 's'];        % Mark vector for the plots
%lines = char( '-' ,'--' ,':', '-.');       % Linestyle
%[start,peak,endd] = ginput(2);
%L = @(x,g,x0) (1/pi).*(0.5.*g./((x-x0).^2+(0.5.*g).^2)) ;
%[files,path] = uigetfile({'*.TXT'},'MultiSelect','on');        %
%Multiselect
width = 6;     % Width in inches
height = 4;    % Height in inches
alw = 0.75;    % AxesLineWidth
fsz = 11;      % Fontsize
lw = 1.3;      % LineWidth %1.3
msz = 10;       % MarkerSize
lcn = 'southeast'	; % Location
od = cd;        % origin directory
offset = 2;        % PlotOffset
continuer = 1 ;     % To continue or not
%errX= 0.1 ;     % Horizontal error

prompt = {'legend','shift ref','shift min', 'shift max','Refractive index of polymer'};       % Display for manual inputs
dlg_title = 'Input';        % Input title
num_lines = 1;      % Number of lines
defans = {'' , '0','515','525','1.5'};        % Default answsers
answer = inputdlg(prompt,dlg_title,num_lines,defans);       % input for main variables
%legendh(i)=answer(1);       % Legend for current file
shift_ref = cell2d(answer(2));     % Shift from reference to literature value
shift_min=cell2d(answer(3));        % Min x axis value
shift_max=cell2d(answer(4));        % Max x axis value
npol = cell2d(answer(5));       % Refractive index of polymer


[file,path] = uigetfile({'*.TXT'}) ;        % Open data file (.txt)
fname=file;        % Store filename
cd (path)       % Goes to data folder
data_raman = importdata(file,'\t',35);      % Importdata
cd (od)     % original directory
data_num = data_raman.data;     % Numerical data from structure
imax = numel(data_num(2:end,1));     % Number of sprectrum
shift = data_num(1,2:end);      % Shift (cm^-1) for x axis
cts = data_num(2:end,2:end);        % Counts
depth = data_num(2:end,1);      % Scan depth (µm)
if npol
    depth = depth.*npol;
end
if shift_ref     % In case of reference shift from literrature
    shift=shift+shift_ref;
end
x_fit=shift_min : 0.001:shift_max ;     %  X Fit value
x=shift(shift>shift_min & shift<shift_max);     % Eliminate Value outside of study window
ycts=cts(:,shift>shift_min & shift<shift_max);        % Eliminate Value outside of study window
figure(1)
pos = get(gcf, 'Position');
set(gcf, 'Position', [pos(1) pos(2) width*100, height*100]); %<- Set size
set(gca, 'FontSize', fsz, 'LineWidth', alw); %<- Set properties
set(gca,'XTick',shift_min:shift_max);


for i = 1:imax
    [ Yf, P, RESNORM, RESIDUAL] = lorentzfit(x,ycts(i,:));        % Fit data to a lorentz law
    f_lorentz = @(x) P(1)./((x - P(2)).^2 + P(3)) + P(4);       % Fit function
    cts_fit(i,:)=f_lorentz(x_fit);     % Y fit value
    [ymax, iymax]= max(cts_fit(i,:));      % Value of raman peak and index
    peak_pos(i)= x_fit(iymax);      % Position of peak
    peak_value(i)=ymax;
    FWMH(i)=2*sqrt(P(3));       % FWMH
    
    plot(x_fit,cts_fit(i,:),'k--')      % superpose grpahs
    hold on
    xlabel('Raman shift (cm^{-1})') ;
    ylabel('Counts') ;
end
%-------------------------------
% FIGURE
%-------------------------------

figure (2)      % Max vs distance

plot(depth,peak_value,'o') ; 
pos = get(gcf, 'Position');
set(gcf, 'Position', [pos(1) pos(2) width*100, height*100]); %<- Set size
set(gca, 'FontSize', fsz, 'LineWidth', alw); %<- Set properties
xlabel('Distance from surface(µm)') ; 
ylabel('Counts') ; 

%---------------------------------

figure(3)       % Surface plot
[X, Y]=meshgrid(x_fit,depth);
Z=cts_fit;
mesh(X,Y,Z);
xlabel('Raman shift (cm^{-1})')
ylabel('Distance from surface (µm)')
zlabel('counts')

figure(4)       % Countour plot with max line
contourf(X,Y,Z)
hold on
plot(peak_pos,depth,'.-')
xlabel('Raman shift (cm^{-1})')
ylabel('Distance from surface (µm)')
pos = get(gcf, 'Position');
set(gcf, 'Position', [pos(1) pos(2) width*100, height*100]); %<- Set size
set(gca, 'FontSize', fsz, 'LineWidth', alw); %<- Set properties
%h(i)=plot(x_fit,f_lorentz(x_fit),col(i),'linewidth',lw);    % Plot fit curve
set(gcf,'InvertHardcopy','on');
set(gcf,'PaperUnits', 'inches');
papersize = get(gcf, 'PaperSize');
left = (papersize(1)- width)/2;
bottom = (papersize(2)- height)/2;
myfiguresize = [left, bottom, width, height];
set(gcf,'PaperPosition', myfiguresize);
set(gca,'XTick',shift_min:shift_max);

%print('zscan2D.png','-dpng','-r600')

figure(5)       % MAx peak from substrate and max from trhin film
[pks,locs] = findpeaks(peak_value,'MinPeakProminence',20);
plot(x_fit,cts_fit(locs(1),:),'k--',x_fit,cts_fit(locs(2),:),'k:') ; 
[pks,locS1]=max(cts_fit(locs(1),:));
[pks,locS2]=max(cts_fit(locs(2),:));
xlabel('Raman shift (cm^{-1})')
ylabel('Counts')
legend(sprintf('Top : %0.2f cm^{-1} Distance : %0.1f',x_fit(locS1),depth(locs(1))),sprintf('Bulk : %0.2f cm^{-1} Distance : %0.1f',x_fit(locS2),depth(locs(2))));


% choice2 = questdlg('treat other files ?', ...       % Treat other files ?
%     'continue', ...
%     'Yes','No','No');
% % Handle response
% switch choice2
%     case 'Yes',
%         continuer = 1;      % New selection of files
%         i=i+1;
%         
%         hold on
%     case 'No',
%         continuer = 0;      % End of script
% end
% legend(h,legendh)       % Set legend
% 
% save=inputdlg({'Save ? (0/1)','Output filename'},'Save',1,{'1',''});        % Save menu
% SoN=cell2d(save(1));        % Save or not
% filename=cell2mat(save(2));     % PNG and TXT filename
% if SoN      % Save data under a txt file and graph under a png
%     % Here we preserve the size of the image when we save it.
%     set(gcf,'InvertHardcopy','on');
%     set(gcf,'PaperUnits', 'inches');
%     papersize = get(gcf, 'PaperSize');
%     left = (papersize(1)- width)/2;
%     bottom = (papersize(2)- height)/2;
%     myfiguresize = [left, bottom, width, height];
%     set(gcf,'PaperPosition', myfiguresize);
%     print(sprintf('%s.png',filename),'-dpng','-r600')
%     fid=fopen(sprintf('%s.txt',filename),'a');
%     fprintf(fid,'Filename ; Legend ; Peak ; FWMH ; Ref shift \n');
%     for j=1:i
%         fprintf(fid,'%s ; %s ; %0.3f ; %0.2f ; %0.2f \n',fname(j,:),char(legendh(j)),peak(j),FWMH(j),shift_ref(j));
%     end
%     fclose(fid);
% end
% 
