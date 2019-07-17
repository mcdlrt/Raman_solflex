clc
close all
clear all
%pkg load signal %for octave
%graphics_toolkit ('gnuplot') % change toolkit for octave
%---------------------------------------
%definition of variables
%---------------------------------------
fontss=15; %font size
LW=2;%linewidth for plot, box and grid.
filename1='resultsMinMax.txt'; %name of output file
filename2='resultsAvgDiff.txt';
maxp=[];%Variables for minimum and maximum
minp=[];
hp=[];%figure handle
%---------------------------------------


%---------------------------------------------
%Files importation
%---------------------------------------------

[files,path] = uigetfile({'*.TXT;*.dat'},'MultiSelect','on');%open window to open only .dat files
cd (path) %go to directory

if iscell(files) %in case there is only one file
    n=size(files);%n number of files to plot
    n=n(2);%number of files selected
else
    n=1;
    files=cellstr(files);
end
%---------------------------------------------

for i=1:n%loop for files
    a=importdata(char(files(i)),' ' ,4); %import data from txt files with 4 header lines
    a=a.data; %data field
    
    %---------------------------------------------
    %%%%%%%%%%%%%%%%%%%%%%%%%%%% Results Variable %%%%%%%%%%%%%%%
    %---------------------------------------------
    avgdiff=[0];
    stddiff=[0];
    nbdiff=[0];
    minV=[0];
    maxV=[0];
    
    th=4.5;%sensitivity for peak detection
    pmax=0.9;% 90% of maximum(minimum) for median calculation
    %---------------------------------------------
    
    
    %---------------------------------------------
    %time in second and Current in nA
    %time step and axis limit
    %---------------------------------------------
    
    time=a(:,1)-a(1,1); %time in seconds
    y=a(:,2);%y axis data
    [dt,w]=size(time);
    dt=time(end)/dt; %time interval
    ym=min(y)-0.05*abs(min(y));
    yM=max(y)+0.05*abs(max(y));
    %---------------------------------------------
    %raw data display
    %---------------------------------------------
    figure(100+i)
    plot(time,y);
    
    
    %---------------------------------------------
    
    %---------------------------------------------
    %dialog box for analysis parameters
    %---------------------------------------------
    mOd=12;
    while mOd~=0 && mOd~=1
        prompt = {'median filter 0 or [20 30]','Difference(1) or average(0) of extrema','Choose anaylisis interval (1 or 0)','remove background ? (1 or 0)'};
        dlg_title = 'Input';
        num_lines = 1;
        defans = {'0' , '1','0','0'};
        answer = inputdlg(prompt,dlg_title,num_lines,defans);%,defaultans);
        mf=cell2mat(answer(1));
        mf=str2double(mf);
        p(1)=mf;
        mOd=cell2mat(answer(2));
        mOd=str2double(mOd);
        p(2)=mOd;
        start=cell2mat(answer(3));
        start=str2double(start);
        p(3)=start;
        bg=cell2mat(answer(4));
        bg=str2double(bg);
        p(4)=bg;
    end
    %---------------------------------------------
    
    
    %---------------------------------------------
    %starting time of analysis
    %---------------------------------------------
    jend=a(end,1);
    p(6)=time(end);
    if start ==1
        [start,endd] = ginput(2);
        jend=round(start(2)./dt);
        p(3)=start(1);
        p(6)=start(2);
        jstart=round(start(1)./dt);
        
        y=y(jstart+1:jend);
        time=time(jstart+1:jend);
    end
    
    
    
    
    %---------------------------------------------
    
    yo=y;%raw data after time start
    
    %---------------------------------------------
    %if mf >0 A global median filter is applied to the data
    %else just a local one to find extrema
    %---------------------------------------------
    if mf>0 % apply a median filter if parameter different from 0
        y =y(1)+medfilt1(y-y(1), mf);% median filter, mf is the vector lenght, the bigger, the smoother
    end
    %---------------------------------------------
    
    
    %---------------------------------------------
    %background removal
    %---------------------------------------------
    nlocsbg=[];
    thbg=4.5; %sensitivity for background removal
    while bg==1 && length(nlocsbg)<2
        nlocsbg=peakfinder(y,(max(y)-min(y))/thbg,max(y),-1,false);%find minima
        thbg=thbg+0.5;
    end
    if bg==1
        xx=interp1(time(nlocsbg),y(nlocsbg),time,'spline'); %intepolation of minima
        
        y=y-xx+median(xx); %interpolation curve of minima is removed to the signal and median is added to "center" it
    end
    
    
    
    %---------------------------------------------
    
    %---------------------------------------------
    %Extrema finding
    %---------------------------------------------
    nc=0;
    pc=0;
    nlocs=peakfinder(y,(max(y)-min(y))/th,max(y),-1,false);%find minima
    plocs=peakfinder(y,(max(y)-min(y))/th,min(y),1,false);%find maxima
    if ~isempty(nlocs)
        nc=1;
        navg=mean(y(nlocs));
        nstd=std(y(nlocs));
        nnb=length(nlocs);
    end
    if ~isempty(plocs)
        pc=1;
        pavg=mean(y(plocs));
        pstd=std(y(plocs));
        pnb=length(plocs);
    end
    %---------------------------------------------
    if ~mOd
        hf=figure(i);
        hold on
        hp=plot(time,yo,'b',time,y,'r');
        if nc && ~pc
            res=1;
            plot(time(nlocs),y(nlocs),'o');
            legend(hp,'raw signal','signal','minima')
            title(sprintf('average : %.2f  +- %.3f n=%d',navg,nstd,nnb)) %titles with average of difference of mean
        elseif ~nc && pc
            res=1;
            plot(time(plocs),y(plocs),'*');
            legend(hf,'raw signal','signal','maxima')
            title(sprintf('average : %.2f  +- %.3f n=%d',pavg,pstd,pnb)) %titles with average of difference of mean
        elseif nc && pc
            res=1;
            plot(time(nlocs),y(nlocs),'o',time(plocs),y(plocs),'*');
            legend(hp,'raw signal','signal','minima','maxima')
            title(sprintf('average : %.2f  +- %.3f n=%d and %.2f  +- %.3f n=%d',navg,nstd,nnb,pavg,pstd,pnb)) %titles with average of difference of mean
        else
            errordlg('no peak found')
            res=0;
        end
        if res
            sa=questdlg ('save results ? ');
            if sa(1)=='Y' && nc && pc
                name=strsplit(char(files(i)),'.');
                %print(char(name(1)), '-dpng', '-r600'); %<-Save as PNG with 600 DPI
                fid = fopen (filename1, 'a');%open or creat file
                fprintf(fid,'file name; average maxima; std; number ; average minima; std; number; gaussian filter\n');
                
                fprintf(fid,'%s; %f; %f; %d; %f; %f; %d; %d;\n',char(name(1)),pavg,pstd,pnb,navg,nstd,nnb,p(1)); %print results
                
                fclose (fid);%close file
            elseif sa(1)=='Y' && ~nc && pc
                name=strsplit(char(files(i)),'.');
                %print(char(name(1)), '-dpng', '-r600'); %<-Save as PNG with 600 DPI
                fid = fopen (filename1, 'a');%open or creat file
                fprintf(fid,'file name; average maxima; std; number; gaussian filter\n');
                
                fprintf(fid,'%s; %f; %f; %d; %d;\n',char(name(1)),pavg,pstd,pnb,p(1)); %print results
                
                fclose (fid);%close file
            elseif sa(1)=='Y' && nc && ~pc
                name=strsplit(char(files(i)),'.');
                %print(char(name(1)), '-dpng', '-r600'); %<-Save as PNG with 600 DPI
                fid = fopen (filename1, 'a');%open or creat file
                fprintf(fid,'file name; average minima; std; number; median filter\n');
                
                fprintf(fid,'%s; %f; %f; %d; %d;\n',char(name(1)),navg,nstd,nnb,p(1)); %print results
                
                fclose (fid);%close file
            end
        end
    elseif mOd
        if ~pc || ~nc
            errordlg('not enough peaks')
        else
            nb=min(pnb,nnb);
            diff=y(plocs(1:nb))-y(nlocs(1:nb));
            avgdiff=mean(diff);
            stddiff=std(diff);
            hf=figure(i);
            
            hp=plot(time(plocs),y(plocs),'bo',time(nlocs),y(nlocs),'bs',time,y,'r',time,yo,'-.k','Markersize',12,'linewidth',LW);
            xlabel('Time (s)','fontsize',fontss);%axis
            ylabel('Y axis ','fontsize',fontss);
            set(gca, 'linewidth',LW, 'fontsize', fontss,'ygrid','on')%box parameter and ygrid on
            title(sprintf('average : %.2f nA +- %.3f n=%d',avgdiff,stddiff,nb)) %titles with average of difference of mean
            %axis([0 a(end,1)-a(1,1) ym yM])
            
            h2=legend(hp,'Max','Min','Signal','Original signal','Location','EastOutside');%legend
            
            sa=questdlg ('save results ? ');
            if sa(1)=='Y'
                name=strsplit(char(files(i)),'.');
                print(char(name(1)), '-dpng', '-r600'); %<-Save as PNG with 600 DPI
                fid = fopen (filename2, 'a');%open or creat file
                fprintf(fid,'file name; average of difference; standard deviation; number of difference; median filter\n');
                
                fprintf(fid,'%s; %.3f; %.4f; %d; %.1f',char(name(1)),avgdiff,stddiff,nb,mf); %print results
                
                fclose (fid);%close file
            end
            
            
        end
    end
    
    
    
    
    %
    %     %---------------------------------------------
    %     %calculare the average of median max and min then make the difference
    %     %between the two, calculate the average and standard deviation
    %     %---------------------------------------------
    %     mintmp=squeeze(minp(i,:));%reduce vector dimension
    %     maxtmp=squeeze(maxp(i,:));
    %     mintmp=mintmp(mintmp~=0);%min and max ~=0(empty matrix is full of 0)
    %     maxtmp=maxtmp(maxtmp~=0);
    %     nbmin=size(mintmp);
    %     nbmax=size(maxtmp);
    %     nb=min(nbmin,nbmax);%minimum number of extrema
    %     nb=nb(1);
    %     diff=maxtmp(1:nb)-mintmp(1:nb);%differenc
    %     avgdiff=mean(diff);%average
    %     stddiff=std(diff);%standard deviation
    %     nbdiff=nb;
    %     %---------------------------------------------
    %
    
end
%---------------------------------------------
%Plot of signal, extrema, median and orginal signal
%---------------------------------------------
% hf=figure(i);
%
% hp=plot(time(jmax),maxtmp,'bo',time(jmin),mintmp,'bs',time,y,'r',time,medp,'b',time,Io,'-.k','Markersize',12,'linewidth',LW);
% xlabel('Time (s)','fontsize',fontss);%axis
% ylabel('Y axis (nA)','fontsize',fontss);
% set(gca, 'linewidth',LW, 'fontsize', fontss,'ygrid','on')%box parameter and ygrid on
% title(sprintf('average : %.2f nA +- %.3f n=%d',avgdiff,stddiff,nb)) %titles with average of difference of mean
% axis([0 a(end,1)-a(1,1) ym yM])
%
% h2=legend(hp,'Max','Min','Signal','Median','Original signal','Location','EastOutside');%legend
%
% %---------------------------------------------
%
% %---------------------------------------------
% %export data and plot
% %---------------------------------------------
% sa=questdlg ('save results ? ');
% if sa(1)=='Y'
%     name=strsplit(char(files(i)),'.');
%     print(char(name(1)), '-dpng', '-r600'); %<-Save as PNG with 600 DPI
%     fid = fopen (filename, 'a');%open or creat file
%     fprintf(fid,'file name; average of difference; standard deviation; number of difference; gaussian filter; %% of peak for median; background removal; time interval (s)\n');
%
%     fprintf(fid,'%s; %.3f; %.4f; %d; %.2f; %d; %d; %.2f; %d-%d\n',char(name(1)),avgdiff,stddiff,nbdiff,p(1),p(2),p(4),p(3),p(6)); %print results
%
%     fclose (fid);%close file
%
% end
% %---------------------------------------------




