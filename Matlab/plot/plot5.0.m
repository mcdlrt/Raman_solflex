%Use this script to plot V(t) data from Lecroy Wavesurfer 424 oscilloscope
%Multiple .dat files can be loaded at once
%Median filter can be applied via dialog box
%Scale is either automatic or manual (dialog box)


clc 
close all
clear all
pkg load signal % signal package 
graphics_toolkit ('gnuplot') % change toolkit (for octave)
fontss=25; %font size
LW=2;%linewidth for plot, box and grid.
%cd '/home/laurent/Dropbox/IMEP/resultats/bending test'

dir=uigetdir; % choose directory
cd (dir) %go to directory
mf = inputdlg ('median filter ? (0=no) '); %median filter parameter
mf=cell2mat(mf);
mf=str2double(mf);
as=questdlg ('autoscale ? '); %autoscale variable

if as(1) == 'N' % user set scale
    s = inputdlg ('Time (s) ? '); 
    s = str2double(cell2mat(s));
    Vy = inputdlg ('Voltage (mV) ?');
    Vy=str2double(cell2mat(Vy));
    
endif



files = uigetfile('*.dat','MultiSelect','on');%open window to open only .dat files
if iscell(files) %in case there is only one file
  n=size(files);%n number of files to plot
  n=n(2);%number of files selected
  else
  n=1;
  files=cellstr(files);
endif


for i=1:n %loop for ploting each file
  %fp=char(files(fi)); %file path into string
  a=load(char(files(i))); %load data from file
  t=a(:,1)-a(1,1);%time in s
  V=a(:,2).*1000;%voltage in mV
  if mf>0 % apply a median filter if parameter different from 0
    V = medfilt1 (real(V), mf);% median filter, mf is the vector lenght, the bigger, the smoother
  endif
  if as(1) == 'Y' % automatic scale
    s = max(t);% time x
    Vy = max(abs(V)) + 40; %voltage y
  endif
  hf=figure(i);%handle for plot
  sname='sample';%title prefix
  plot(t,V,'r','linewidth',LW  )%plot
  axis ([0 s -Vy Vy ])%([x_lo x_hi y_lo y_hi])
  xlabel('Time (s)','fontsize',fontss);%axis
  ylabel('Voltage (mV)','fontsize',fontss);
  set(gca, 'linewidth',LW, 'fontsize', fontss,'ygrid','on')%box parameter and ygrid on
  %title(sprintf('%s',char(files(i)))); %title
  print(sprintf('%s.png',char(files(i))), '-dpng', '-r600'); %<-Save as PNG with 600 DPI
endfor