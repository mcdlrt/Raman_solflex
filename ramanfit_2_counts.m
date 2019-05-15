clc
clear all
close all

od = cd;        % Original directory
%col=[ 'r' 'b' 'k' 'g' 'c' 'y' rand(1,3) rand(1,3) rand(1,3) rand(1,3) rand(1,3)];     % Color vector for the plots
col = {'k','b','r','g','y',[.5 .6 .7],[.8 .2 .6], rand(1,3), rand(1,3),rand(1,3),rand(1,3),rand(1,3)} ;
mark = [ '.' 'o' '+' '*' 'x' 's'];        % Mark vector for the plots
lines = char( '-' ,'--' ,':', '-.');       % Linestyle
%[start,peak,endd] = ginput(2);
%L = @(x,g,x0) (1/pi).*(0.5.*g./((x-x0).^2+(0.5.*g).^2)) ;
%[files,path] = uigetfile({'*.TXT'},'MultiSelect','on');        %
%Multiselect
width = 6;     % Width in inches
height = 4;    % Height in inches
alw = 0.75;    % AxesLineWidth
fsz = 11;      % Fontsize
lw = 1.3;      % LineWidth %1.3
msz = 3;       % MarkerSize
lcn = 'southeast'	; % Location
od = cd;        % origin directory
offset = 2;        % PlotOffset
continuer = 1 ;     % To continue or not
errX= 0.1 ;     % Horizontal error
i=1;        % Iteration variable
while continuer         % Main LOOP
    prompt = {'legend','shift ref','shift min', 'shift max'};       % Display for manual inputs
    dlg_title = 'Input';        % Input title
    num_lines = 1;      % Number of lines
    defans = {'' , '0','515','525'};        % Default answsers
    answer = inputdlg(prompt,dlg_title,num_lines,defans);       % input for main variables
    legendh(i)=answer(1);       % Legend for current file
    shift_ref(i)=cell2d(answer(2));     % Shift from reference to literature value
    shift_min=cell2d(answer(3));        % Min x axis value
    shift_max=cell2d(answer(4));        % Max x axis value
    
    [file,path] = uigetfile({'*.TXT'}) ;        % Open data file (.txt)
    fname{i}=file;        % Store filename
    cd (path)       % Goes to data folder
    data_raman = importdata(file,'\t',35);      % Importdata
    cd (od)     % original directory
    data_num = data_raman.data;     % Numerical data from structure
    shift = data_num(:,1);      % Shift (cm^-1) for x axis
    cts = data_num(:,2) ;       % Counts y axis
    if shift_ref(i)     % In case of reference shift from literrature
        shift=shift+shift_ref(i);
    end
    
    x=shift(shift>shift_min & shift<shift_max);     % Eliminate Value outside of study window
    ycts=cts(shift>shift_min & shift<shift_max);        % Eliminate Value outside of study window
    [ Y, P, RESNORM, RESIDUAL] = lorentzfit(x,ycts);        % Fit data to a lorentz law
    f_lorentz = @(x) P(1)./((x - P(2)).^2 + P(3)) + P(4);       % Fit function
    x_fit=shift_min : 0.001:shift_max ;     %  X Fit value
    y_fit=f_lorentz(x_fit);     % Y fit value
    [ymax, iymax]= max(y_fit);      % Value of raman peak and index
    peak_val(i) = ymax ; % Max intensitie
    base_line(i) = P(4) ; % Fit baseline
    peak(i)= x_fit(iymax);      % Position of peak
    FWMH(i)=2*sqrt(P(3));       % FWMH
    intT = data_raman.textdata(1) ;      % Integration time
    intT = char(intT) ;     % Char
    intT = str2num(intT(16:end)) ;       % Int time
    y_norm = y_fit./intT;       % Signal in count/second
    
    %-------------------------------
    % FIGURE
    %-------------------------------
    
    figure(1)
    xlabel('Raman shift (cm^{-1})') ; 
    ylabel('Counts/second') ; 
    pos = get(gcf, 'Position');
    set(gcf, 'Position', [pos(1) pos(2) width*100, height*100]); %<- Set size
    set(gca, 'FontSize', fsz, 'LineWidth', alw); %<- Set properties
    %h(i)=plot(x_fit,f_lorentz(x_fit),col(i),'linewidth',lw);    % Plot fit curve
    h(i)=plot(x_fit,y_norm,'linewidth',lw,'color',col{i});    % Plot fit curve

    hold on
    %plot(x,ycts,'.','MarkerSize',msz,'MarkerEdgeColor',col(i))      % Experimental data
    plot(x,ycts./intT,'o','MarkerSize',msz,'MarkerEdgeColor','k','MarkerFaceColor',col{i})
    %vline(peak,'k--',sprintf('%0.2f',peak(i)))     % Vertical line one the peak
    vline(peak,'k--')     % Vertical line one the peak
    %herrorbar(x_fit(iymax),y_fit(iymax),errX);
    % Set Tick Marks
    set(gca,'XTick',shift_min:shift_max);
    ax=gca;
    ax.YScale = 'log' ;
 
    
    
    %---------------------------------
    
    choice2 = questdlg('treat other files ?', ...       % Treat other files ?
        'continue', ...
        'Yes','No','No');
    % Handle response
    switch choice2
        case 'Yes',
            continuer = 1;      % New selection of files
            i=i+1;
            
            hold on
        case 'No',
            continuer = 0;      % End of script
    end
end         % Main loop
legend(h,legendh)       % Set legend

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
    grid on
    print(sprintf('%s.png',filename),'-dpng','-r600')
    fid=fopen(sprintf('%s.txt',filename),'a');
    fprintf(fid,'Filename ; Legend ; Peak ; FWMH ; Ref shift ; Base level ; Peak intensitie \n');
    for j=1:i
        fprintf(fid,'%s ; %s ; %0.3f ; %0.2f ; %0.2f ; %0.1f ; %0.1f \n',fname{j},char(legendh(j)),peak(j),FWMH(j),shift_ref(j),base_line(j),peak_val(j));
    end
    fclose(fid);
end

