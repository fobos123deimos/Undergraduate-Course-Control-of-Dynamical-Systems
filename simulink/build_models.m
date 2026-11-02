function build_models(overwrite_existing)
% Generate nominal models for original scenarios; requires MATLAB/Simulink.
% Existing files require explicit opt-in; loaded models are never closed.
if nargin < 1; overwrite_existing=false; end
if ~islogical(overwrite_existing) || ~isscalar(overwrite_existing)
    error('build_models:InvalidOption','overwrite_existing must be a scalar logical.');
end
destination=fullfile(fileparts(mfilename('fullpath')),'generated');
if ~exist(destination,'dir'); mkdir(destination); end
definitions={
    'thermal_sensor',1/15,conv([60,1],[12,1]),420;
    'ventilation_local',-40,[40,1],240;
    'platform_floor',[25.6,3200],[8,25.6,3200],10;
    'passive_notch',[1e-6,0,1],[1e-6,.001,1],.1;
    'motor_voltage',.1,[.0002,.0204,.05],8;
    'root_locus_K12',12,[1,8,12,12],20
};
% Check the complete batch before creating or replacing any model.
for index=1:size(definitions,1)
    name=['original_csd_' definitions{index,1}];
    if bdIsLoaded(name)
        error('build_models:LoadedModel','Model %s is already open. Save and close it deliberately before generation.',name);
    end
    if exist(fullfile(destination,[name '.slx']),'file') && ~overwrite_existing
        error('build_models:ExistingFile','Model %s already exists. Use build_models(true) only to replace saved outputs.',name);
    end
end
for index=1:size(definitions,1)
    name=['original_csd_' definitions{index,1}];
    new_system(name);
    add_block('simulink/Sources/Step',[name '/Input'],'Time','0','Position',[30,60,60,90]);
    add_block('simulink/Continuous/Transfer Fcn',[name '/Model'],'Numerator',mat2str(definitions{index,2},16),'Denominator',mat2str(definitions{index,3},16),'Position',[120,50,300,100]);
    add_block('simulink/Sinks/To Workspace',[name '/Output'],'VariableName','response','SaveFormat','Structure With Time','Position',[360,55,470,95]);
    add_line(name,'Input/1','Model/1'); add_line(name,'Model/1','Output/1');
    set_param(name,'StopTime',num2str(definitions{index,4}),'Solver','ode45','RelTol','1e-8','AbsTol','1e-10');
    save_system(name,fullfile(destination,[name '.slx'])); sim(name); close_system(name,0);
end
disp('Generated and simulated six nominal original-scenario models.');
end
