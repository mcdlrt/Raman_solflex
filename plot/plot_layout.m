function plot_layout(h,grd,lgd,eq,fts,msz,lw,lcn)
% plot_layout(line handle,fts,msz,lw,lcn)
axs = gca ;
if ~exist('fts')
    fts = 15 ;
end

if ~exist('msz')
    msz = 6 ;
end

if ~exist('lw')
    lw=1.3 ;
end

if ~exist('lcn')
    lcn = 'northwest' ;
end

if exist('grd')
    if grd =='y'
        set(axs,'YGrid','on');
    elseif grd == 'x'
        set(axs,'XGrid','on');
    elseif grd == '1'
        grid on
    end
end




set(h,'linewidth',lw)
set(h,'markersize',msz)
set(axs,'fontsize',fts)
set(axs,'Color','none')
if exist('lgd')
    if exist('eq')
        set(lgd,'Interpreter','latex')
    end
    set(lgd,'Color','none')
    set(lgd,'location',lcn)
    set(lgd,'fontsize',fts-4)
end