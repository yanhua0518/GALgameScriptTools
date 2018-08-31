@echo off
md script_packed
for %%i in (text\*.txt) do (
echo %%~i
BGIScriptRepacker.py script\%%~ni %%~i script_packed\%%~ni
)
echo Finished!
pause
