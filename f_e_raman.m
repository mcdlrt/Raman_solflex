%[start,peak,endd] = ginput(2);
%L = @(x,g,x0) (1/pi).*(0.5.*g./((x-x0).^2+(0.5.*g).^2)) ;
%[files,path] = uigetfile({'*.TXT'},'MultiSelect','on');        %
%Multiselect
clear all

close all

width = 6;     % Width in inches
height = 4;    % Height in inches
alw = 0.75;    % AxesLineWidth
fsz = 11;      % Fontsize
lw = 1.3;      % LineWidth %1.3
msz = 3;       % MarkerSize
lcn = 'northwest'	; % Location
%buni = - 337 ;      % Coeff
sW = 5 ; %sample width in mm
sT = 0.23 ; %sample thickness in mm
[file,path] = uigetfile({'*.TXT'}) ;   %files name and path
cd (path)
imp=importdata(file,';');       % import data
val=imp.data;       % Values
f = val(:,1) ;  % Force in N
Rshift = val(:,2);      % Maximum raman shift (cm^-1)
fwhm = val(:,3);        % Full width at half maximum
cst = inputdlg({'silicon reference shift ? (0 if no ref)','Coeff raman'},'reference',1,{'0','-337'});        % Dialog box for reference

ref_shift = cell2d(cst(1));      % Convert from cell 2 double
buni=cell2d(cst(2)) ;
if ~ref_shift
    ref_shift = Rshift(1);      % If there is no given value reference will be first point
end
vsize = numel(f);       % vector size for errobar
dW = Rshift-ref_shift ;     % Delta shift in cm-1
errW = ones(vsize,1).*0.1 ;       % Errorbar for ramanshift
eps = (dW./(buni))*100 ;      % %Strain according to Peng et al. 2009 doi : 10.1063/1.3110184 uniaxial nstress along [110] for (100) wafer
errEps = (errW./(buni))*100;        % Error bar for strain
E = 169 ;       % Young modulus along <110> direction in GPa

sigma = eps.*E.*1e-3 ;        % Stress in MPa 

figure(1) % strain and raman shift
pos = get(gcf, 'Position');
set(gcf, 'Position', [pos(1) pos(2) width*100, height*100]); %<- Set size
set(gca, 'FontSize', fsz, 'LineWidth', alw); %<- Set properties
%ax.YLim = ([518 524]) ;

exp=errorbar(eps,f,(f.*0.05),'--.k','linewidth',lw);
hold on
exp2=herrorbar(eps,f,errEps,'.k');
exp2(1).LineWidth = lw;
exp2(2).LineWidth = lw;
ylabel('Force (N)') ;
xlabel('Strain (%)') ;

grid on 



hold on
fiton = inputdlg('Fit x first point :','Fit',1,{'0'});
fiton = cell2d(fiton);
if fiton
    pfit = polyfit(eps(1:fiton),f(1:fiton),1);       % linear fit
    %ffit=min(stress(1:fiton)):max(stress(1:fiton))+0.1;
    efit=eps(1):0.05:max(eps(1:fiton))+0.1;
    ffit=polyval(pfit,efit);
    fitp=plot(efit,ffit,'k','linewidth',lw);
    legend([exp fitp],{'Experimental values','Linear fit' },'location',lcn)
end

save=inputdlg({'Save ? (0/1)','Output filename'},'Save',1,{'1',''});        % Save menu
SoN=cell2d(save(1));        % Save or not
filename=cell2mat(save(2));     % PNG and TXT filename
if SoN      % Save data under a txt file and graph under a png
    % Here we preserve the size of the image when we save it.
    set(gcf,'InvertHardcopy','on');
    set(gcf,'PaperUnits', 'inches');
    papersize = get(gcf, 'PaperSize');
    left = (papersize(1)- width)/2;
    bottom = (papersize(2)- height)/2;
    myfiguresize = [left, bottom, width, height];
    set(gcf,'PaperPosition', myfiguresize);
    print(sprintf('%s.png',filename),'-dpng','-r800')
    
    
end

figure(2)
pos = get(gcf, 'Position');
set(gcf, 'Position', [pos(1) pos(2) width*100, height*100]); %<- Set size
set(gca, 'FontSize', fsz, 'LineWidth', alw); %<- Set properties

plot(eps,fwhm,'--ok')
xlabel('strain (%)')
ylabel('Raman peak FWHM (cm^{-1})')
ax=gca;
ax.YLim= [min(fwhm)-0.2 max(fwhm)+0.2];
grid on

save=inputdlg({'Save ? (0/1)','Output filename'},'Save',1,{'1',''});        % Save menu
SoN=cell2d(save(1));        % Save or not
filename=cell2mat(save(2));     % PNG and TXT filename
if SoN      % Save data under a txt file and graph under a png
    % Here we preserve the size of the image when we save it.
    set(gcf,'InvertHardcopy','on');
    set(gcf,'PaperUnits', 'inches');
    papersize = get(gcf, 'PaperSize');
    left = (papersize(1)- width)/2;
    bottom = (papersize(2)- height)/2;
    myfiguresize = [left, bottom, width, height];
    set(gcf,'PaperPosition', myfiguresize);
    print(sprintf('%s.png',filename),'-dpng','-r800')
    
    
end