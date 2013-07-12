echo off
set file=%1
for /f %%i in (host.txt) do ping -a -n 1 %%i | FIND /i "Pinging " >> result.txt

