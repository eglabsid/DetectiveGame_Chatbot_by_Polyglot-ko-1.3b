@echo off


REM Python 설치 여부 확인
py --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not found in PATH. Please install Python and try again.
    exit /b 1
)

REM 가상 환경을 생성할 디렉토리 설정
set VENV_DIR=%~dp0venv
IF EXIST %VENV_DIR% (
    echo Skip Creating Python virtual enviroment Because %VENV_DIR% Exist ...
) else (
    REM 가상 환경 생성
    echo Creating Python virtual environment in %VENV_DIR%...
    py -m venv %VENV_DIR%
)


REM 가상 환경 생성 성공 여부 확인
if exist %VENV_DIR%\Scripts\activate (
    echo Virtual environment created successfully in %VENV_DIR%.
) else (
    echo Failed to create virtual environment.
    exit /b 1
)

REM 가상 환경 활성화
echo Activating the virtual environment...
call %VENV_DIR%\Scripts\activate

REM 가상 환경 활성화 확인
if "%VIRTUAL_ENV%"=="" (
    echo Failed to activate the virtual environment.
    exit /b 1
) else (
    echo Virtual environment activated successfully.
    echo Your virtual environment is now active. Run 'deactivate' to exit the virtual environment.
)
