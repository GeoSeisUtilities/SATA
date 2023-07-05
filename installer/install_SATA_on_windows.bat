@echo off

REM installing python3
winget install python3
REM installing GMT
winget install gmt6
REM installing python dipendencies
winget install pip
where pip > pip
set "pip=pip"
for /F "delims=" %%x in (%pip%) do (
     set "pip=%%x"
)
%pip% install tk bs4 plyer geopy requests numpy pillow matplotlib
REM clear temporaneus variables
del pip
