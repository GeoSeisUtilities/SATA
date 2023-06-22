@echo off

REM installing GMT
curl -LO "https://github.com/GenericMappingTools/gmt/releases/download/6.4.0/gmt-6.4.0-win64.exe"
pause
start gmt-6.4.0-win64.exe
pause
REM installing python3
curl -LO "https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe"
pause
start python-3.11.4-amd64.exe
pause
REM installing python dependencies
pip install tk bs4 plyer geopy requests numpy pillow matplotlib
