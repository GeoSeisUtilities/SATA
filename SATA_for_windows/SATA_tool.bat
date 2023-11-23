@echo off

echo Do not close this Window!

cd SATA_bin
set "nome_eseguibile=python.exe"
REM searching python.exe
for /f "delims=" %%i in ('where %nome_eseguibile%') do (
    echo %%i > py_temp
    set "py_temp=py_temp"
    for /F "delims=" %%x in (%py_temp%) do (
     set "py_temp=%%x"
)
    %py_temp% Test_py_exe.py 
)

set "py=py"
for /F "delims=" %%x in (%py%) do (
     set "py=%%x"
)
REM start SATA tool
%py% SATA_execute_tool.py
REM first plot
%py% SATA_coord_zoom.py
%py% SATA_coord_sections.py
%py% SATA_last_ten_eqs.py
call combined_plots.bat
REM start the banner in background
start %py% SATA_close_banner.py &
REM refresh earthquake list and notify every 5 minutes
TIMEOUT /T 300 >nul REM wait 5 minutes

:CheckForFile REM check the existence of running file
IF EXIST "temp/running" (GOTO FoundIt) ELSE GOTO FinishTool

:FoundIt REM refresh the earthquakes search
%py% SATA_refresh.py REM check for a refresh of earthquake list
%py% SATA_coord_zoom.py
%py% SATA_coord_sections.py
%py% SATA_last_ten_eqs.py
call combined_plots.bat REM plot new list
REM send notification
set "message=Last update: %date% %time%"
mshta "javascript:var sh=new ActiveXObject( 'WScript.Shell' ); sh.Popup( '%message%', 3, 'SATA update', 64 );close()"
TIMEOUT /T 300 >nul
GOTO CheckForFile

:FinishTool REM remove files and close
rmdir /s /q temp
del combined_plots.pdf
del cpt_file
del output3
del proiezione_output
del py
exit
