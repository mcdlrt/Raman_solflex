function nam=cell2d(sans)
%convert a cell to a double
if iscell(sans)
    if isempty(sans)
        nam=0;
    else
        nam=cell2mat(sans);
        nam=str2double(nam);
    end
    
else
    error(message('MATLAB:cellstr:InputClass'));
    
end