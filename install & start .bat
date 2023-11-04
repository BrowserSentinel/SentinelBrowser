@echo off
REM Install Python packages from requirements.txt

REM Check if Python is installed
python --version
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b 1
)

REM Install packages
pip install -r requirements.txt

REM Check the installation status
if %errorlevel% equ 0 (
    echo Packages installed successfully.
) else (
    echo Failed to install packages.
)
pause

python browser.py