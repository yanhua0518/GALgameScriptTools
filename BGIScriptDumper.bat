if "%~1"=="" goto end
if not exist "%~1\" goto end
for %%i in (%1\*.*) do %~dp0\BGIScriptDumper.py %%~i