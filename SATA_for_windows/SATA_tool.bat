@echo off

cd SATA_bin
REM start SATA tool
python3.exe SATA_execute_tool.py
REM first plot
python3.exe SATA_coord_zoom.py
python3.exe SATA_coord_sections.py
python3.exe SATA_last_ten_eqs.py
call combined_plots.bat
REM start the banner in background
start python3.exe SATA_close_banner.py &
REM refresh earthquake list and notify every 5 minutes
TIMEOUT /T 300 >nul REM wait 5 minutes

:CheckForFile REM check the existence of running file
IF EXIST "temp/running" (GOTO FoundIt) ELSE GOTO FinishTool

:FoundIt REM refresh the earthquakes search
python3.exe SATA_refresh.py REM check for a refresh of earthquake list
python3.exe SATA_coord_zoom.py
python3.exe SATA_coord_sections.py
python3.exe SATA_last_ten_eqs.py
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
exit
