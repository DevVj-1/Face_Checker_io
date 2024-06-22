# @echo off

:: Open PowerShell and run the following commands

:: Navigate to "set-up" directory
cd "Manually-install"

:: Run the Visual Studio Build Tools installer
start /wait vs_BuildTools.exe

:: Check if vs_BuildTools.exe ran successfully
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to run vs_BuildTools.exe
    exit /b %ERRORLEVEL%
)

:: Navigate to "Step_2_4Download_boost_1_85_0" directory

curl -L -o boost_1_82_0.zip https://boostorg.jfrog.io/artifactory/main/release/1.82.0/source/boost_1_82_0.zip

powershell -Command "Expand-Archive -Path boost_1_82_0.zip"

cd boost_1_82_0


:: Run the Boost bootstrap.bat file
#start /wait bootstrap.bat
call bootstrap.bat

:: Navigate back to the root directory
cd ../../

:: Install Python dependencies
# powershell -Command "pip install -r requirements.txt"
pip install -r requirements.txt

:: Check if pip install ran successfully
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install Python requirements
    exit /b %ERRORLEVEL%
)

echo Setup completed successfully.


pause
