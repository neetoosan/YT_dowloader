@echo off
echo ========================================
echo YouTube Downloader - Build to EXE
echo ========================================
echo.

:: Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Failed to install PyInstaller
        pause
        exit /b 1
    )
)

:: Check if the Python script exists
if not exist "app.py" (
    echo Error: app.py not found in current directory
    echo Please make sure the Python script is in the same folder as this batch file
    pause
    exit /b 1
)

echo Building executable...
echo.

:: Create the executable
pyinstaller --onefile ^
    --windowed ^
    --name "Neetoosan_Downloader" ^
    --icon=app.ico ^
    --add-data "app.ico;." ^
    --hidden-import=kivy ^
    --hidden-import=kivy.core.window ^
    --hidden-import=kivy.core.text ^
    --hidden-import=kivy.core.image ^
    --hidden-import=yt_dlp ^
    app.py

if %errorlevel% neq 0 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo The executable has been created in the 'dist' folder
echo File: dist\Neetoosan_Downloader.exe
echo.
echo Cleaning up temporary files...
rmdir /s /q build 2>nul
del /q *.spec 2>nul

echo.
echo You can now run the executable without needing Python installed!
echo.
pause