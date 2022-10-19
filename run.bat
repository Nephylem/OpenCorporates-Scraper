@echo off

call env\Scripts\activate.bat
"python" "run.py"
call env\Scripts\deactivate.bat
pause