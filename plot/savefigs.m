function savefigs(def)
%Function used to save a figure with the other function export_fig, this
%functions allows to choose a filename via a dialog box, def, transparencies, format
od = cd ; % Original directory
cd H:\matlab\output
% if ~exist('sd')
%     sd = od ; % export path = current directory
% else
%     cd (sd) % goes to indicated path to export fig
% end
if ~exist('def','var')
    def = 600;
end

% Construct a questdlg with three options
choice = questdlg('Export figure ?', ...
    'Export', ...
    'Yes (png)','Yes (png+eps)','No','Yes (png+eps)');
% Handle response
switch choice
    case 'Yes (png)'
        prompt = {'Enter file name'};
        dlg_title = 'Input';
        num_lines = 1;
        defaultans = {''};
        fname = inputdlg(prompt,dlg_title,num_lines,defaultans);
        export_fig(char(fname),'-png','-painters', '-transparent',sprintf('-r%d',def))
        
    case 'Yes (png+eps)'
        prompt = {'Enter file name'};
        dlg_title = 'Input';
        num_lines = 1;
        defaultans = {''};
        fname = inputdlg(prompt,dlg_title,num_lines,defaultans);
        export_fig(char(fname),'-png','-eps','-painters', '-transparent',sprintf('-r%d',def))
        
        
    case 'No'
end
cd (od)
        
end






