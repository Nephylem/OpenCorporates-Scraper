@echo off

mkdir output
"python" "get-pip.py"
pip install virtualenv
python -m virtualenv env
call env\Scripts\activate.bat
pip install selenium bs4 numpy pandas fake-useragent tqdm

@echo Env setup finished...
@echo Manually download the driver and extract it to working directory
@echo https://chromedriver.storage.googleapis.com/106.0.5249.61/chromedriver_win32.zip
pause